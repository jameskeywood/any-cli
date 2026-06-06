# io/select.py

from __future__ import annotations

from typing import TypeAlias

from rich.prompt import Prompt

from any_cli.io.console import console
from any_cli.models.limits import ModelLimits

Registry: TypeAlias = dict[str, dict[str, ModelLimits]]


def _prompt_for_selection(
    title: str,
    options: list[str],
) -> str:
    """
    Prompt the user to select an item from a numbered list.
    """

    if not options:
        raise ValueError(f"No options available for '{title}'")

    console.print(f"\n[bold]{title}[/bold]\n")

    for index, option in enumerate(options, start=1):
        console.print(f"{index}. {option}")

    while True:
        raw_value = Prompt.ask(
            "\nSelect option",
            default="1",
        )

        try:
            selected_index = int(raw_value) - 1

            if 0 <= selected_index < len(options):
                return options[selected_index]

        except ValueError:
            pass

        console.print(
            "[red]Invalid selection. Please try again.[/red]"
        )


def select_provider(registry: Registry) -> str:
    """
    Prompt the user to select a provider.
    """

    provider_names = list(registry.keys())

    return _prompt_for_selection(
        title="Available Providers",
        options=provider_names,
    )


def select_model(
    registry: Registry,
    provider: str,
) -> str:
    """
    Prompt the user to select a model for a provider.
    """

    models = registry[provider]
    model_names = list(models.keys())

    return _prompt_for_selection(
        title="Available Models",
        options=model_names,
    )
