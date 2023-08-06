"""
    Appellation: message
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
from candyland.core.utils import clock
from pydantic import BaseModel


class Message(BaseModel):
    message: str
    timestamp: str = clock.timestamp()
