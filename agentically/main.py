"""CLI entry point for agentically."""

from __future__ import annotations

import importlib.metadata
from typing import Optional

import typer
from rich.console import Console

from agentically.commands.explore import explore_command
from agentically.commands.use import use_command

app = typer.Typer(
    name="agentically",
    help=(
        "Discover and install AI agent systems from the community registry.\n\n"
        "Run [bold]agentically explore[/bold] to browse available agent systems,\n"
        "then [bold]agentically use <name>[/bold] to install one."
    ),
    no_args_is_help=True,
    rich_markup_mode="rich",
)

_console = Console(stderr=True)


def _version_callback(value: bool) -> None:
    if value:
        version = importlib.metadata.version("agentically")
        typer.echo(f"agentically {version}")
        raise typer.Exit()


@app.callback()
def _main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Discover and install AI agent systems from the community registry."""


# Register subcommands
app.command("explore")(explore_command)
app.command("use")(use_command)
