from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from any_cli.models.messages import Message
from any_cli.models.responses import ChatResponse
from any_cli.tools.base import BaseTool


class BaseClient(ABC):
    provider: str
    model: str

    @abstractmethod
    async def chat(
        self,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> ChatResponse:
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> AsyncGenerator[str, None]:
        pass
