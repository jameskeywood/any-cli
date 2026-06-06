import json
from typing import Any

from groq import Groq

from any_cli.clients.base import BaseClient
from any_cli.config import settings
from any_cli.models.messages import Message
from any_cli.models.responses import ChatResponse, ToolCall
from any_cli.models.limits import ModelLimits
from any_cli.tools.base import BaseTool


class GroqClient(BaseClient):
    provider = "groq"

    def __init__(self) -> None:
        self.client = Groq(api_key=settings.groq_api_key)

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------
    def _tools(self, tools: list[BaseTool] | None) -> list[dict]:
        if not tools:
            return []

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

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------
    def _message_to_dict(self, message: Message) -> dict:
        """
        Convert internal Message → Groq/OpenAI format
        """

        if message.role == "user":
            return {
                "role": "user",
                "content": message.content or "",
            }

        if message.role == "assistant":
            msg = {
                "role": "assistant",
                "content": message.content or "",
            }

            # Attach tool calls if present in metadata (future-proofing)
            if message.metadata and message.metadata.get("tool_calls"):
                msg["tool_calls"] = message.metadata["tool_calls"]

            return msg

        if message.role == "tool":
            meta = message.metadata or {}

            return {
                "role": "tool",
                "tool_call_id": meta.get("tool_call_id"),
                "name": meta.get("tool_name"),
                "content": message.content or "",
            }

        # fallback safety
        return {
            "role": "user",
            "content": message.content or "",
        }

    def _messages(self, messages: list[Message]) -> list[dict]:
        return [self._message_to_dict(m) for m in messages]

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------
    async def chat(
        self,
        model: str,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> ChatResponse:

        response = self.client.chat.completions.create(
            model=model,
            messages=self._messages(messages),
            tools=self._tools(tools),
            tool_choice="auto",
            temperature=0.2,
        )

        choice = response.choices[0]
        message = choice.message

        # --------------------------------------------------------------
        # TOOL CALL PARSING
        # --------------------------------------------------------------
        tool_calls: list[ToolCall] = []

        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:

                tool_calls.append(
                    ToolCall(
                        id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments or "{}"),
                        raw={
                            "id": call.id,
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    )
                )

        # --------------------------------------------------------------
        # RESPONSE TEXT
        # --------------------------------------------------------------
        content = message.content if message.content else None

        return ChatResponse(
            content=content,
            tool_calls=tool_calls,
            provider=self.provider,
            model=model,
        )


    def get_available_models(self) -> list[str]:
        return ["openai/gpt-oss-120b"]


    def get_model_limits(self, model: str) -> ModelLimits:
        return ModelLimits(
            requests_per_minute=30,
            requests_per_day=1000,
            tokens_per_minute=8000,
            tokens_per_day=200000)
