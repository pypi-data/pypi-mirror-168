import argparse

parser = argparse.ArgumentParser(description='', usage='python ___.py _ _ _ ...')
parser.add_argument('_', type=str, nargs='+')
args = parser.parse_args()

___ = []

for index, value in  enumerate(args._, start=1):
    globals()[f"_{index}"] = value
    ___.append(f"_{index}")

for index, value in  enumerate(args._, start=-len(args._)):
    globals()[f"__{-index}"] = value
    ___.append(f"__{-index}")

globals()["__"] = args._

# __all__ = list(globals())
__all__ = ___ + ["__"] + ["___"]