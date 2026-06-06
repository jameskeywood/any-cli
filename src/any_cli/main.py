import asyncio

import typer

from any_cli.orchestrator import AgentOrchestrator
from any_cli.chat.agent import Agent
from any_cli.chat.session import ChatSession
from any_cli.clients.registry import get_client
from any_cli.commands.registry import get_command
from any_cli.config import settings
from any_cli.io.console import console, print_markdown
from any_cli.io.prompt import get_user_input
from any_cli.io.select import select_provider, select_model


app = typer.Typer()


async def run_chat() -> None:
    agent_orchestrator = AgentOrchestrator()

    registry = agent_orchestrator.agent_registry

    # use the agent registry to provide a selection of
    # model options available to the user

    provider = select_provider(registry)
    model = select_model(registry, provider)

    agent = agent_orchestrator.create_agent(provider, model)
 
    console.print(f"[green]Provider:[/] {provider}")
    console.print(f"[green]Model:[/] {model}\n")
    console.print("[dim]/help for commands[/dim]\n")

    while True:
        user_input = await get_user_input()

        if user_input in {"exit", "quit"}:
            break

        if user_input.startswith("/"):
            cmd = get_command(user_input)
            if cmd:
                await cmd.execute(session)
            else:
                console.print("[red]Unknown command[/red]")
            continue

        # check limits somehow before running agent.run

        result = await agent.run(user_input)
        print_markdown(result)

@app.command()
def chat() -> None:
    asyncio.run(run_chat())


if __name__ == "__main__":
    app()

