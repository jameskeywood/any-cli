from any_cli.commands.base import BaseCommand
from any_cli.commands.clear import ClearCommand


COMMANDS: dict[str, BaseCommand] = {
    "/clear": ClearCommand(),
}


def get_command(command: str) -> BaseCommand | None:
    return COMMANDS.get(command)

