from any_cli.chat.session import ChatSession
from any_cli.commands.base import BaseCommand
from any_cli.io.console import console


class HelpCommand(BaseCommand):
    name = "/help"

    description = "Show available commands"

    async def execute(self, session: ChatSession) -> bool:
        console.print("[bold]Commands[/bold]\n")

        console.print("/help - Show commands")
        console.print("/clear - Clear chat")
        console.print("exit - Quit")

        return True

