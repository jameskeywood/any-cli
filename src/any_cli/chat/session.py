from any_cli.models.messages import Message
from any_cli.models.tools import ToolCall


class ChatSession:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def add_user_message(self, content: str) -> None:
        self.messages.append(
            Message(
                role="user",
                content=content,
            )
        )

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(
            Message(
                role="assistant",
                content=content,
            )
        )

    def add_tool_message(
        self,
        tool_call: ToolCall,
        result: str,
    ) -> None:
        self.messages.append(
            Message(
                role="tool",
                content=result,
                metadata={
                    "tool_name": tool_call.name,
                    "tool_call_id": tool_call.id,
                },
            )
        )

    def clear(self) -> None:
        self.messages.clear()
