from any_cli.clients.base import BaseClient
from any_cli.chat.session import ChatSession
from any_cli.models.responses import ToolCall
from any_cli.tools.registry import TOOLS


class Agent:
    def __init__(
        self,
        client: BaseClient,
        session: ChatSession,
        model: str
    ) -> None:
        self.client = client
        self.session = session
        self.model = model

    async def _execute_tool(
        self,
        call: ToolCall,
    ) -> str:
        tool = TOOLS.get(call.name)

        if not tool:
            return f"Unknown tool: {call.name}"

        return await tool.execute(call.arguments)

    async def run(
        self,
        user_input: str,
    ) -> str:
        self.session.add_user_message(user_input)

        while True:
            response = await self.client.chat(
                self.model,
                self.session.messages,
                tools=list(TOOLS.values()),
            )

            # Execute tool calls
            if response.tool_calls:
                for call in response.tool_calls or []:
                    if not call.name:
                        return "Invalid tool call: missing name"

                    result = await self._execute_tool(call)

                    self.session.add_tool_message(
                        tool_call=call,
                        result=result,
                    )

                continue

            # Final assistant response
            final = response.content or ""

            self.session.add_assistant_message(final)

            return final
