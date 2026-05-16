from pydantic import BaseModel
from any_cli.models.tools import ToolCall


class ChatResponse(BaseModel):
    content: str | None = None
    tool_calls: list[ToolCall] = []
    provider: str
    model: str
