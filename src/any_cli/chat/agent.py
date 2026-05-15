from any_cli.clients.base import BaseClient
from any_cli.chat.session import ChatSession
from any_cli.tools.registry import get_tools


class Agent:
    def __init__(
        self,
        client: BaseClient,
        session: ChatSession,
    ) -> None:
        self.client = client
        self.session = session
        self.tools = get_tools()

    async def stream_response(self):
        return self.client.stream_chat(
            messages=self.session.messages,
            tools=self.tools,
        )

