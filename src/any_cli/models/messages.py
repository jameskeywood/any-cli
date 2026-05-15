from typing import Literal

from pydantic import BaseModel


Role = Literal[
    "system",
    "user",
    "assistant",
    "tool",
]


class Message(BaseModel):
    role: Role
    content: str
