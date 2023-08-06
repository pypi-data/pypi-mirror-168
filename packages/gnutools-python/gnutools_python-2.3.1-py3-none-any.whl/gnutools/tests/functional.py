from gnutools.fs import path2modules


def test_imports(root):
    print(root)
    """
    Test import functions from a librory

    :param root:
    :return:
    """
    def try_import(m):
        try:
            exec(f'from {m} import *')
            print(f"=1= TEST PASSED : {m}")
            return True
        except Exception as e:
            print(f"=0= TEST FAILED : {m} ({e})")
            return False
    return [try_import(m) for m in path2modules(root)]


