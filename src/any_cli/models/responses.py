from pydantic import BaseModel


class ChatResponse(BaseModel):
    content: str
    provider: str
    model: str
