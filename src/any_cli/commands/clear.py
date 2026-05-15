from any_cli.chat.session import ChatSession
from any_cli.commands.base import BaseCommand
from any_cli.io.console import console


class ClearCommand(BaseCommand):
    name = "/clear"

    description = "Clear the current chat session"

    async def execute(self, session: ChatSession) -> bool:
        session.clear()

        console.print("[green]Chat cleared[/green]")

        return True

