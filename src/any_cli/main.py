import asyncio

import typer

from any_cli.chat.agent import Agent
from any_cli.chat.session import ChatSession
from any_cli.clients.registry import get_client
from any_cli.commands.registry import get_command
from any_cli.config import settings
from any_cli.io.console import console
from any_cli.io.prompt import get_user_input
from any_cli.io.streaming import stream_to_console


app = typer.Typer()


async def run_chat(
    provider: str,
    model: str,
) -> None:
    client = get_client(
        provider=provider,
        model=model,
    )

    session = ChatSession()

    agent = Agent(
        client=client,
        session=session,
    )

    console.print(
        f"[bold green]Provider:[/] {provider}"
    )

    console.print(
        f"[bold green]Model:[/] {model}"
    )

    console.print(
        "[dim]Type /help for commands[/dim]\n"
    )

    while True:
        user_input = await get_user_input()

        if user_input.strip() in {"exit", "quit"}:
            break

        if user_input.startswith("/"):
            command = get_command(user_input)

            if command is None:
                console.print(
                    "[red]Unknown command[/red]"
                )

                continue

            await command.execute(session)

            continue

        session.add_user_message(user_input)

        stream = await agent.stream_response()

        content = await stream_to_console(
            console,
            stream,
        )

        session.add_assistant_message(content)


@app.command()
def chat(
    provider: str = settings.default_provider,
    model: str = settings.default_model,
) -> None:
    asyncio.run(
        run_chat(
            provider=provider,
            model=model,
        )
    )


if __name__ == "__main__":
    app()

