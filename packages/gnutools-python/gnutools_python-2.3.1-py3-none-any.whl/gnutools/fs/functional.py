import os
import subprocess


def list_folders(root):
    """
    List the folders from a root path
    :param root:
    :return:
    """
    commands = ["find", os.path.realpath(root), "-type", "d"]
    results = subprocess.check_output(commands)
    return results.decode().split("\n")[1:]


def parent(path, level=1, sep="/", realpath=False):
    """
    Get the parent of a file or a directory

    :param path:
    :param level:
    :param sep:
    :return list:
    """
    path = os.path.realpath(path) if realpath else path

    def dir_parent(path, level=1):
        return sep.join(path.split(sep)[:-level])

    return (
        [dir_parent(_path) for _path in path]
        if type(path) == list
        else dir_parent(path, level)
    )


def replace_dir(dir_path):
    """
    Create a folder if it doesnt exist and remove its content

    :param dir_path:
    :return:
    """
    os.makedirs(dir_path, exist_ok=True)
    os.system("rm -r {}".format(dir_path))
    os.makedirs(dir_path, exist_ok=True)


def name(file, level=-1):
    """
    Get the name of a file and remove the extension
    :param file:
    :return string:
    """
    if file.split("/")[-1].__contains__("."):
        output = file.split("/")[-1]
        output = ".".join(output.split(".")[:level])
    else:
        output = file.split("/")[-1]
    return output


def check_files(dir, ext):
    """
    Check if files exist and have a non null size

    :param dir:
    :param ext:
    :return list:
    """
    files_audio_ids = [
        name(file) for file in os.listdir(dir) if ".{}".format(ext) in file
    ]
    files_audio_ids = [
        name(file)
        for file in files_audio_ids
        if os.path.getsize("{}/{}.{}".format(dir, file, ext)) > 0
    ]
    return ["{}/{}.{}".format(dir, file, ext) for file in files_audio_ids]


def contain_filter(file, filters=None):
    """
    Check if a file contains one or many of the substrings specified in filters

    :param file:
    :param filters:
    :return bool:
    """
    if filters is None:
        return True
    for filter in filters:
        if len(file.split(filter)) >= 2:
            return True
    return False


def contain_ext(file, exts=None):
    """
    Check if a file contains a specific extension in a list of extensions

    :param file: file to scan
    :param exts: list of extensions
    :return bool:
    """
    if exts is None:
        return True
    return extension(file) in exts


def find_in_file(file, text):
    try:
        matches = []
        for k, line in enumerate(open(file, "r").readlines()):
            if len(line.split(text)) > 1:
                matches.append(k)
        return (matches, file) if len(matches) > 0 else None
    except:
        pass


def listparents(*args, **kwargs):
    return list(set([parent(f) for f in listfiles(*args, **kwargs)]))


def listfiles(root, patterns=[], excludes=[], exlude_hidden=False):
    """
    Similar to os.listdir but with more options in the search and a specific pattern

    :param root:
    :param patterns:
    :return:
    """

    def string_contains(text, patterns):
        for pattern in patterns:
            if text.__contains__(pattern):
                return True
        return False

    def fitler(file):
        try:
            assert len(file) > 0
            assert not file.__contains__("/.") if exlude_hidden else True
            assert not string_contains(file, excludes) if len(excludes) > 0 else True
            assert string_contains(file, patterns) if len(patterns) > 0 else True
            return True
        except AssertionError:
            return False

    commands = ["find", "-L", os.path.realpath(root)]
    results = subprocess.check_output(commands)
    files = results.decode().split("\n")[1:]
    files = [file for file in files if fitler(file)]
    return files


def ext(f):
    """
    Return the extension of a file

    :param f:
    :return string:
    """
    splits = f.split("/")[-1].split(".")
    return splits[1] if len(splits) == 2 else ""


def extension(f):
    """
    Return the extension of a file

    :param f:
    :return string:
    """
    return ext(f)


def path2modules(root):
    """
    Return the list of python modules from a library specific by its path.

    :param root:
    :return:
    """

    def path2module(m):
        try:
            module = m.split(lib_name)[-1].replace("/", ".")[1:]
            return f"{lib_name}.{module}" if not module=="" else lib_name
        except IndexError:
            return lib_name

    lib_name = name(root)
    modules = set([parent(file) for file in listfiles(root, [".py"])])
    modules = set(
        [path2module(m) for m in modules if not m.__contains__("__pycache__")]
    )
    modules = sorted(modules)
    return modules


def load_config(file):
    from gnutools.utils.functional import load_yaml

    return load_yaml(file)
