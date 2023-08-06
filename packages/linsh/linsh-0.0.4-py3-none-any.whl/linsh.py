import argparse
import subprocess as sp

class LinSH(str):
    def __init__(self, init: str):
        self.init = init

    def __or__(self, command: str):
        """ | """
        self.init = f"{self.init} | {command}"
        return self

    def __neg__(self):
        """ - """
        sp.run(self.init, shell=True)

    def __gt__(self, other):
        sub_obj = sp.run(self.init, shell=True, encoding="utf-8", stderr=sp.PIPE, stdout=sp.PIPE)

        """ > """
        # return None, but directly print stdout and stderr
        if other is None:
            sp.run(self.init, shell=True, encoding="utf-8")
        # return (stderr + stdout), but not print
        elif other is Ellipsis:
            return sub_obj
        # only return stdout, not print
        elif other == 1:
            return sub_obj.stdout
        # only return stderr, not print
        elif other == 2:
            return sub_obj.stderr

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
__all__ = ___ + ["__"] + ["___"] + ["LinSH"]