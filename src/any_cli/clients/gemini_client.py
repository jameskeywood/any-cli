from collections.abc import AsyncGenerator

import httpx

from any_cli.clients.base import BaseClient
from any_cli.config import settings
from any_cli.models.messages import Message
from any_cli.models.responses import ChatResponse
from any_cli.tools.base import BaseTool


class GeminiClient(BaseClient):
    provider = "gemini"

    def __init__(self, model: str = "gemini-2.5-flash") -> None:
        self.model = model

    def _build_contents(
        self,
        messages: list[Message],
    ) -> list[dict]:
        contents = []

        for message in messages:
            role = "user"

            if message.role == "assistant":
                role = "model"

            contents.append(
                {
                    "role": role,
                    "parts": [
                        {
                            "text": message.content,
                        }
                    ],
                }
            )

        return contents

    async def chat(
        self,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> ChatResponse:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        payload = {
            "contents": self._build_contents(messages),
        }

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

        params = {
            "key": settings.gemini_api_key,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                params=params,
                json=payload,
            )

        response.raise_for_status()

        data = response.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]

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
        response = await self.chat(messages, tools)

        yield response.content

