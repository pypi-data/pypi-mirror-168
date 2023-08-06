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

        # return None, but directly print stdout and stderr
        # Note:
        # (for no break pipe) don't use universal_newlines=True
        # (for no break pipe) don't use encoding="utf-8"
        if other is None:
            only_return_code_obj = subprocess.run(self.init, shell=True)
            return only_return_code_obj.returncode
        else:
            sub_obj = subprocess.run(self.init, shell=True, universal_newlines=True, stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)

            # return (stderr + stdout), but not print
            if other is Ellipsis:
                return sub_obj
            # only return stdout, not print
            elif other == 1:
                return sub_obj.stdout
            # only return stderr, not print
            elif other == 2:
                return sub_obj.stderr

    def __and__(self, other):
        """ & """
        # return None, but directly print stdout and stderr
        if other is None:
            subprocess.Popen(self.init, shell=True)

        else:
            sub_obj = subprocess.Popen(self.init, shell=True, universal_newlines=True, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)

            # return (stderr + stdout), but not print
            if other is Ellipsis:
                return sub_obj
            # only return stdout, not print
            elif other == 1:
                return sub_obj.stdout
            # only return stderr, not print
            elif other == 2:
                return sub_obj.stderr