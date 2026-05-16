from google import genai
from google.genai import types

from any_cli.clients.base import BaseClient
from any_cli.config import settings
from any_cli.models.messages import Message
from any_cli.models.responses import ChatResponse, ToolCall
from any_cli.tools.base import BaseTool


class GeminiClient(BaseClient):
    provider = "gemini"

    def __init__(self, model: str = "gemini-3-flash-preview") -> None:
        self.model = model
        self.client = genai.Client(api_key=settings.gemini_api_key)

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------
    def _tools(self, tools: list[BaseTool] | None) -> list[types.Tool]:
        if not tools:
            return []

        # IMPORTANT FIX:
        # Each tool must become its own Tool object
        return [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=tool.schema,
                    )
                ]
            )
            for tool in tools
        ]

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------
    def _message_to_content(self, message: Message) -> types.Content:
        if message.role == "assistant":
            return types.Content(
                role="model",
                parts=[types.Part(text=message.content or "")],
            )

        if message.role == "user":
            return types.Content(
                role="user",
                parts=[types.Part(text=message.content or "")],
            )

        # We do NOT support "tool" role in Gemini SDK
        # Tool results must be converted into function_response parts
        if message.role == "tool":
            metadata = message.metadata or {}

            tool_name = metadata.get("tool_name")
            tool_call_id = metadata.get("tool_call_id")

            return types.Content(
                role="user",
                parts=[
                    types.Part.from_function_response(
                        name=tool_name,
                        response={"result": message.content},
                        # ❌ DO NOT PASS id — SDK does not support it
                    )
                ],
            )

        # fallback safety
        return types.Content(
            role="user",
            parts=[types.Part(text=message.content or "")],
        )

    def _contents(self, messages: list[Message]) -> list[types.Content]:
        return [self._message_to_content(m) for m in messages]

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------
    async def chat(
        self,
        messages: list[Message],
        tools: list[BaseTool] | None = None,
    ) -> ChatResponse:

        config = types.GenerateContentConfig(
            tools=self._tools(tools),
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True,
            ),
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=self._contents(messages),
            config=config,
        )

        candidate = response.candidates[0].content

        tool_calls: list[ToolCall] = []
        text_parts: list[str] = []

        for part in candidate.parts:
            # ---------------------------
            # FUNCTION CALL
            # ---------------------------
            fc = getattr(part, "function_call", None)
            if fc:
                tool_calls.append(
                    ToolCall(
                        id=fc.id,
                        name=fc.name,
                        arguments=dict(fc.args or {}),
                        raw={
                            "id": fc.id,
                            "name": fc.name,
                            "args": dict(fc.args or {}),
                        },
                    )
                )
                continue

            # ---------------------------
            # TEXT OUTPUT
            # ---------------------------
            text = getattr(part, "text", None)
            if text:
                text_parts.append(text)

        return ChatResponse(
            content="\n".join(text_parts).strip() or None,
            tool_calls=tool_calls,
            provider=self.provider,
            model=self.model,
        )
