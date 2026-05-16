from pydantic import BaseModel, Field
from any_cli.models.tools import ToolCall


class ChatResponse(BaseModel):
    content: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    provider: str
    model: str
