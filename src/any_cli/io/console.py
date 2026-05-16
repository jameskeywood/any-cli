from rich.console import Console
from rich.markdown import Markdown


console = Console()


def print_markdown(text: str) -> None:
    """Prints the given text as markdown to the console."""
    console.print(Markdown(text))


