import argparse
import subprocess as sp

def init():
    parser = argparse.ArgumentParser(description='', usage='python ___.py _ _ _ ...')
    parser.add_argument('_', type=str, nargs='+')
    args = parser.parse_args()

    available_variable_names = []
    for index, value in  enumerate(args._, start=1):
        exec(f"_{index}='{value}'", globals())  # inner func, must be globals
        available_variable_names.append(f"_{index}")

    for index, value in  enumerate(args._, start=-len(args._)):
        exec(f"__{-index}='{value}'", globals())  # inner func, must be globals
        available_variable_names.append(f"__{-index}")

    exec(f"__={args._}", globals())  # inner func, must be globals
    return available_variable_names

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
        # # only return stdout, not print
        elif other == 1:
            return sub_obj.stdout
        # # only return stderr, not print
        elif other == 2:
            return sub_obj.stderr