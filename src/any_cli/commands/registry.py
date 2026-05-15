from any_cli.commands.base import BaseCommand
from any_cli.commands.clear import ClearCommand
from any_cli.commands.help import HelpCommand


COMMANDS: dict[str, BaseCommand] = {
    "/clear": ClearCommand(),
    "/help": HelpCommand(),
}


def get_command(command: str) -> BaseCommand | None:
    return COMMANDS.get(command)

