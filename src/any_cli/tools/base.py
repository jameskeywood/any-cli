from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str
    description: str
    schema: dict

    @abstractmethod
    async def execute(self, arguments: dict) -> str:
        pass

