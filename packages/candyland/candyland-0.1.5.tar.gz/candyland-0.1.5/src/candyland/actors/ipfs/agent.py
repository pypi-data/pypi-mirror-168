"""
    Appellation: agent
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
from candyland.components.pipelines import Sleeve


class IpfsAgent(object):
    def __init__(self):
        self.sleeve = Sleeve("ipfs")

    def add(self, *args):
        return self.sleeve("add", *args)

    def cat(self, *args):
        return self.sleeve("cat", *args)

    def ls(self, *args):
        return self.sleeve("ls", *args)

    def new(self):
        return self.sleeve("init")


if __name__ == "__main__":
    print(IpfsAgent().sleeve.help())
