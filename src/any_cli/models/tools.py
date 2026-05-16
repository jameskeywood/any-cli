from typing import Any

from pydantic import BaseModel


class ToolCall(BaseModel):
    id: str | None = None
    name: str
    arguments: dict[str, Any]
    raw: dict[str, Any] | None = None
