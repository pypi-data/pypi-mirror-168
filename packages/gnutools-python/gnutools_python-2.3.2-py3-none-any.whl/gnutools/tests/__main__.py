import os

from gnutools.fs import parent
from gnutools.tests.functional import test_imports

if __name__ == "__main__":
    test_imports(parent(os.path.realpath(__file__), level=2))
