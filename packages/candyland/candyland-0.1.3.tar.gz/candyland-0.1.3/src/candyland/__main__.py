"""
    Appellation: __main__
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
from pydantic import BaseModel, BaseSettings
from typing import List, Optional


class AppSettings(BaseModel):
    authors: Optional[List[str]]
    mode: str = "development"
    name: str
    token: str

    def slug(self) -> str:
        return self.name.lower()


class Settings(BaseSettings):
    application: AppSettings


class Application(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class CommandLineInterface(Application):
    def run(self):
        pass


if __name__ == "__main__":
    from candyland.components.messages import Message

    print(Message(message="Welcome to candyland!"))
