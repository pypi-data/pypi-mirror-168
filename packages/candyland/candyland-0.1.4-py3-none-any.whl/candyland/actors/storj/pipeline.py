"""
    Appellation: pipeline
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
import subprocess


class Sleeve(object):
    application: str
    result: subprocess.CompletedProcess
    output: list

    def execute(self, *args):
        self.result = subprocess.run([self.application, *args], capture_output=True)
        return self

    def help(self, *args):
        self.execute("--help", *args)
        return self

    def lines(self):
        self.output = str(self.result.stdout).strip("b'").split("\\n")
        return self

    def __repr__(self): return "\n".join(self.lines().output)


class Storj(Sleeve):
    def __init__(self):
        self.application = 'uplink'

    def access(self, *args):
        self.execute("access", *args)
        return self

    def cp(self, *args):
        self.execute("cp", *args)
        return self

    def ls(self, *args):
        self.execute("ls", *args)
        return self

    def mb(self, *args):
        self.execute("mb", *args)
        return self

    def meta(self, *args):
        self.execute("meta", *args)
        return self

    def mv(self, *args):
        self.execute("mv", *args)
        return self

    def rb(self, *args):
        self.execute("rb", *args)
        return self

    def rm(self, *args):
        self.execute("rm", *args)
        return self

    def setup(self, *args):
        self.execute("setup", *args)
        return self

    def share(self, *args):
        self.execute("share", *args)
        return self

    def version(self):
        self.execute("version")
        return self


if __name__ == '__main__':
    print(Storj().help("meta"))
