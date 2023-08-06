"""
    Appellation: fs
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
import os
from pydantic import BaseModel


def try_extend_path(root: str = os.path.expanduser("~"), path: str = None) -> str:
    try:
        return os.path.join(root, path)
    except TypeError:
        return root


class IndexedFolder(BaseModel):
    root: str
    dirs: list
    files: list


class Filer(object):
    source: str
    target: str = None

    def __init__(self, source: str = os.path.expanduser("~")):
        self.source = source

    def set_target(self, target: str):
        self.target = target
        return self

    def walk(self, target: str = None):
        if target:
            self.set_target(target)
        return [
            IndexedFolder(root=r, dirs=ds, files=fs)
            for r, ds, fs in os.walk(try_extend_path(self.source, self.target))
        ]
