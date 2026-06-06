from any_cli.clients.base import BaseClient
from any_cli.clients.gemini_client import GeminiClient
from any_cli.clients.groq_client import GroqClient


CLIENTS: dict[str, type[BaseClient]] = {
    "gemini": GeminiClient,
    "groq": GroqClient
}


def get_client(provider: str) -> BaseClient:
    client_class = CLIENTS.get(provider)

    if client_class is None:
        raise ValueError(f"Unknown provider: {provider}")

    return client_class()
