from any_cli.models.messages import Message


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

    def add_tool_message(self, content: str) -> None:
        self.messages.append(
            Message(
                role="tool",
                content=content,
            )
        )

    def clear(self) -> None:
        self.messages.clear()

