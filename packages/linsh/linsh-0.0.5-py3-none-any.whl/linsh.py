import argparse
import subprocess


class LinSH(str):
    def __init__(self, init: str):
        self.init = init

    def __or__(self, command: str):
        """ | """
        self.init = f"{self.init} | {command}"
        return self

    def __gt__(self, other):
        """ > """
        sub_obj = subprocess.run(self.init, shell=True, universal_newlines=True, stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
        # return None, but directly print stdout and stderr
        if other is None:
            subprocess.run(self.init, shell=True, universal_newlines=True)
        # return (stderr + stdout), but not print
        elif other is Ellipsis:
            return sub_obj
        # only return stdout, not print
        elif other == 1:
            return sub_obj.stdout
        # only return stderr, not print
        elif other == 2:
            return sub_obj.stderr

    def __and__(self, other):
        """ & """
        sub_obj = subprocess.Popen(self.init, shell=True, universal_newlines=True, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)

        # return None, but directly print stdout and stderr
        if other is None:
            subprocess.Popen(self.init, shell=True, universal_newlines=True)

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

for index, value in enumerate(args._, start=1):
    globals()[f"_{index}"] = value
    ___.append(f"_{index}")

for index, value in enumerate(args._, start=-len(args._)):
    globals()[f"__{-index}"] = value
    ___.append(f"__{-index}")

globals()["__"] = args._

# __all__ = list(globals())
__all__ = ___ + ["__"] + ["___"]
