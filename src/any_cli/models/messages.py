from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str | None = None
    metadata: dict[str, Any] | None = None
