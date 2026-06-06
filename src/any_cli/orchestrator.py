from __future__ import annotations

from typing import Any

from any_cli.chat.agent import Agent
from any_cli.chat.session import ChatSession
from any_cli.clients.registry import get_client
from any_cli.config import settings
from any_cli.models.limits import ModelLimits


class AgentOrchestrator:
    """
    Responsible for:

    - Initialising configured provider clients
    - Building a model registry
    - Creating chat agents
    """

    def __init__(self) -> None:
        self.clients = self._initialise_clients()

        self.agent_registry = self.build_registry(
            self.clients,
        )

    def _initialise_clients(self) -> dict[str, Any]:
        """
        Initialise all configured provider clients.
        """

        clients: dict[str, Any] = {}

        for provider in settings.provider_api_keys:
            try:
                clients[provider] = get_client(
                    provider=provider,
                )

            except Exception as exc:
                print(
                    f"Failed to initialise provider "
                    f"'{provider}': {exc}"
                )

        return clients

    def build_registry(
        self,
        clients: dict[str, Any],
    ) -> dict[str, dict[str, ModelLimits]]:
        """
        Build registry structure:

        {
            provider: {
                model_name: ModelLimits
            }
        }
        """

        registry: dict[str, dict[str, ModelLimits]] = {}

        for provider, client in clients.items():
            try:
                models = client.get_available_models()

            except Exception as exc:
                print(
                    f"Failed to load models for "
                    f"'{provider}': {exc}"
                )

                continue

            registry[provider] = {}

            for model_name in models:
                try:
                    limits = client.get_model_limits(
                        model_name,
                    )

                    registry[provider][model_name] = limits

                except Exception as exc:
                    print(
                        f"Failed to load limits for "
                        f"'{provider}/{model_name}': {exc}"
                    )

        return registry

    def create_agent(
        self,
        provider: str,
        model: str,
    ) -> Agent:
        """
        Create a configured chat agent.
        """

        client = self.clients[provider]

        session = ChatSession()

        return Agent(
            client=client,
            session=session,
            model=model,
        )
