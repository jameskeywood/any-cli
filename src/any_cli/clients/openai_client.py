from collections.abc import AsyncGenerator

import httpx

from any_cli.clients.base import BaseClient
from any_cli.config import settings
from any_cli.models.messages import Message
from any_cli.models.responses import ChatResponse
from any_cli.tools.base import BaseTool


class OpenAIClient(BaseClient):
    provider = "openai"

    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.model = model

    def _build_tools(
        self,
        tools: list[BaseTool] | None,
    ) -> list[dict] | None:
        if not tools:
            return None

        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.schema,
                },
            }
            for tool in tools
        ]

    async def chat(
        self,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> ChatResponse:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "tools": self._build_tools(tools),
        }

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
            )

        response.raise_for_status()

        data = response.json()

        content = data["choices"][0]["message"].get("content", "")

        return ChatResponse(
            content=content,
            provider=self.provider,
            model=self.model,
        )

    async def stream_chat(
        self,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> AsyncGenerator[str, None]:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "stream": True,
            "tools": self._build_tools(tools),
        }

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue

                    data = line.removeprefix("data: ")

                    if data == "[DONE]":
                        break

                    try:
                        chunk = httpx.Response(
                            200,
                            content=data,
                        ).json()

                        delta = chunk["choices"][0]["delta"]

                        content = delta.get("content")

                        if content:
                            yield content

                    except Exception:
                        continue
