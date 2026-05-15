from abc import ABC, abstractmethod

from any_cli.chat.session import ChatSession


class BaseCommand(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(self, session: ChatSession) -> bool:
        pass

