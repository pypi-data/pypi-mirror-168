import pandas as pd
from itertools import product
from gnutools.utils import id_generator
from tabulate import tabulate
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

score = "score"

class Grid:
    def __init__(self):
        self.results = dict()
        self.df = None

    def setup(self, config):
        keys = list(config.keys())
        self.__kwargs = dict()
        self.columns = list(config.keys()) + [score]
        for exp in product(*list(config.values())):
            args = dict([(k, exp[j]) for j, k in enumerate(keys)])
            id = id_generator()
            args.update({"id": id})
            self.__kwargs[id] = args

    def run(self, func, config, columns, limit=10, ascending=False):
        _columns = list()
        with ProcessPoolExecutor() as e:
            conns = []
            for id, conn in self.__kwargs.items():
                conn.update(config)
                self.results[id] = {"kwargs": conn}
                _columns = list(conn.keys())
                conns.append(conn)

            fs = [e.submit(func, **conn) for conn in conns]
            for f in tqdm(as_completed(fs), total=len(fs), desc="Grid processing"):
                assert f._exception is None
                self.report(**f._result)

            df = pd.DataFrame.from_records([list(s["kwargs"].values()) + [s[score]] for s in self.results.values()],
                                           columns= _columns + [score])
            df = df.filter(columns + [score])
            self.df = df
            df = df.sort_values(by=score, ascending=ascending)
            df = df.head(limit)
            return tabulate(df, headers=self.columns, tablefmt="grid")

    def report(self, score, id, **kwargs):
        self.results[id].update({"score": score, "_result": kwargs})
        del self.__kwargs[id]

