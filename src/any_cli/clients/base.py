from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from any_cli.models.messages import Message
from any_cli.models.responses import ChatResponse
from any_cli.models.limits import ModelLimits
from any_cli.tools.base import BaseTool


class BaseClient(ABC):
    provider: str

    @abstractmethod
    async def chat(
        self,
        model: str,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> ChatResponse:
        pass

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """
        Return models available for the current API key.
        """
        pass

    @abstractmethod
    def get_model_limits(
        self,
        model: str,
    ) -> ModelLimits:
        """
        Return limits for a specific model.
        """
        pass
