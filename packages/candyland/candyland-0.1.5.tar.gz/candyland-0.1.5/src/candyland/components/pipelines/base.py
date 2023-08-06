"""
    Appellation: base
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
import subprocess


def commands_from_dict(**kwargs):
    return [
        i[j] for i in [("--" + k, v) for k, v in kwargs.items()] for j in range(len(i))
    ]


class Sleeve(object):
    result: subprocess.CompletedProcess

    def __init__(self, application: str):
        self.application: str = application

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def execute(self, *args, **kwargs):
        self.result = subprocess.run(
            [self.application, *args, *commands_from_dict(**kwargs)],
            capture_output=True,
        )
        return self

    def help(self, *args):
        return self.execute("--help", *args)

    def lines(self):
        return str(self.result.stdout).strip("b'").split("\\n")

    def __repr__(self):
        return "\n".join(self.lines())
