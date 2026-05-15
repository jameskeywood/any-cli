from any_cli.clients.base import BaseClient
from any_cli.clients.gemini_client import GeminiClient
from any_cli.clients.openai_client import OpenAIClient


CLIENTS: dict[str, type[BaseClient]] = {
    "openai": OpenAIClient,
    "gemini": GeminiClient,
}


def get_client(
    provider: str,
    model: str,
) -> BaseClient:
    client_class = CLIENTS.get(provider)

    if client_class is None:
        raise ValueError(f"Unknown provider: {provider}")

    return client_class(model=model)

