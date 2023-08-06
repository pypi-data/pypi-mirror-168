from datetime import timedelta
from rich.progress import Progress
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
from tqdm import tqdm


class Pool:
    def __init__(self, *args, silent=False, **kwargs):
        self.silent = silent
        self._e = ProcessPoolExecutor(*args, **kwargs).__enter__()
        self._fs = []
        self._results = []
        self._exceptions = []
        self.pbar = None

    def submit(self, tasks):
        self.bar = tqdm(tasks, total=len(tasks), desc="Submitting") if not self.silent else None
        self._fs = set([self._e.submit(f, *args, **kwargs) for f, args, kwargs in tasks])
        self.bar.set_description("Processing") if not self.silent else None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            f = as_completed(self._fs).__next__()
            res, e = f._result, f._exception
            self._results.append(res)
            self._exceptions.append(e)
            self._fs = self._fs.difference([f])
            self.bar.update(1) if not self.silent else None
            return res, e
        except StopIteration:
            self._e = None
            raise StopIteration

class ProcessPoolExecutorBar:
    def __init__(self):
        self._results = []
        self._exceptions = []
        self.t0 = None
        self.N = None

    def submit(self, tasks, *args, **kwargs):
        self.N = len(tasks)
        with Progress() as progress:
            task1 = progress.add_task("[red]Sending context...", total=self.N)
            with ProcessPoolExecutor(*args, **kwargs) as e:
                fs = [e.submit(*t) for t in tasks]
                for k, f in enumerate(as_completed(fs)):
                    self.t0 = self.t0 if self.t0 is not None else time.time()
                    _exception = f.exception()
                    if _exception is None:
                        self._results.append(f.result())
                    else:
                        self._results.append(None)
                    self._exceptions.append(_exception)
                    progress.tasks[0].description = f"{self.description_left(k)} | {self.description_right(k)}"
                    progress.update(task1, advance=1, refresh=True)

    def description_right(self, k):
        try:
            return f"[red]Processing {k}/{self.N}"
        except:
            return f"[red]Processing ?/?"

    def description_left(self, k):
        time_elapsed = int(time.time()-self.t0)
        try:
            return f"[blue]{timedelta(seconds=time_elapsed)} {format(k/time_elapsed, '.2f')}it/s"
        except:
            return f"[blue] ? it/s"
