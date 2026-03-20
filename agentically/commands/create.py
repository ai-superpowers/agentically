"""agentically create — install an agent system into the current directory."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import requests
import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from agentically._config import REGISTRY_ORG, REGISTRY_REPO, REGISTRY_BRANCH

_API_BASE = (
    f"https://api.github.com/repos/{REGISTRY_ORG}/{REGISTRY_REPO}"
)
_RAW_BASE = (
    f"https://raw.githubusercontent.com/{REGISTRY_ORG}/{REGISTRY_REPO}"
    f"/{REGISTRY_BRANCH}"
)
_HEADERS = {"Accept": "application/vnd.github+json"}
_LARGE_THRESHOLD = 50

_console = Console()


def _get_agent_files(name: str) -> list[dict]:
    """Return all blob entries under prompt-systems/<name>/ via the recursive trees API."""
    resp = requests.get(
        f"{_API_BASE}/git/trees/{REGISTRY_BRANCH}?recursive=1",
        headers=_HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    prefix = f"prompt-systems/{name}/"
    return [
        item
        for item in resp.json().get("tree", [])
        if item["path"].startswith(prefix) and item["type"] == "blob"
    ]


def _download_file(path: str) -> bytes:
    """Download a single file from the raw GitHub URL."""
    url = f"{_RAW_BASE}/{path}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.content


def _prompt_platform(detected: str | None) -> str | None:
    """Interactively ask the user to choose a platform adaptation to apply.

    Shows a numbered list of supported platforms plus a 'skip' option.
    The auto-detected platform (if any) is offered as the default.
    Returns the chosen platform name, or None if the user chose to skip.
    """
    from agentically.adapters import SUPPORTED_PLATFORMS

    choices = sorted(SUPPORTED_PLATFORMS) + ["skip"]
    default_index = (
        choices.index(detected) + 1
        if detected in choices
        else len(choices)  # "skip"
    )

    _console.print("\n[bold]Apply a platform adaptation?[/bold]")
    for i, choice in enumerate(choices, 1):
        detected_tag = " [dim](detected)[/dim]" if choice == detected else ""
        _console.print(f"  {i}. {choice}{detected_tag}")

    while True:
        raw = Prompt.ask(
            "\nEnter number",
            default=str(default_index),
            show_default=True,
        ).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            selection = choices[int(raw) - 1]
            break
        _console.print(f"[yellow]Please enter a number between 1 and {len(choices)}.[/yellow]")

    return None if selection == "skip" else selection


def create_command(
    name: str = typer.Argument(..., help="Name of the agent system to install."),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Skip confirmation prompts."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing files without prompting."
    ),
    platform: Optional[str] = typer.Option(
        None,
        "--platform",
        "-p",
        help="Platform adaptation to apply after install (cursor, copilot, claude, kiro).",
    ),
) -> None:
    """Install an agent system into the current directory."""
    from agentically.adapters import SUPPORTED_PLATFORMS, detect_platform, get_adapter

    # Validate --platform early so the user gets feedback before any download
    if platform and platform not in SUPPORTED_PLATFORMS:
        _console.print(f"[red]Unknown platform:[/red] {platform!r}")
        _console.print(
            f"Supported values: {', '.join(sorted(SUPPORTED_PLATFORMS))}"
        )
        raise typer.Exit(1)

    # Fetch file list
    try:
        files = _get_agent_files(name)
    except requests.RequestException as exc:
        _console.print(f"[red]Network error:[/red] {exc}")
        _console.print("Check your connection and try again.")
        raise typer.Exit(1)

    if not files:
        _console.print(f"[red]Agent system not found:[/red] {name!r}")
        _console.print(
            "Run [bold]agentically explore[/bold] to see available agent systems."
        )
        raise typer.Exit(1)

    # Large-install guard
    if len(files) > _LARGE_THRESHOLD and not yes:
        _console.print(
            f"[yellow]Warning:[/yellow] This agent system contains "
            f"{len(files)} files."
        )
        if not Confirm.ask("Continue with download?"):
            raise typer.Exit(0)

    cwd = Path.cwd()

    # Determine platform before writing any files so we route directly into
    # the platform folder — no staging step, safe to stack agent systems.
    active_platform = platform  # from --platform flag (already validated)
    if active_platform is None:
        detected = detect_platform(cwd)
        if yes:
            active_platform = detected  # silent auto-detect; may be None
        else:
            active_platform = _prompt_platform(detected)

    adapter = get_adapter(active_platform) if active_platform else None

    prefix = f"prompt-systems/{name}/"
    written: list[Path] = []
    skipped: list[Path] = []

    for entry in files:
        rel_path = Path(entry["path"][len(prefix):])
        dest = adapter.dest_for(cwd, name, rel_path) if adapter else cwd / rel_path
        display_path = dest.relative_to(cwd)

        # Conflict check
        if dest.exists() and not force:
            if not Confirm.ask(
                f"[yellow]Conflict:[/yellow] [bold]{display_path}[/bold] already exists. Overwrite?"
            ):
                skipped.append(display_path)
                continue

        # Download
        try:
            content = _download_file(entry["path"])
        except requests.RequestException as exc:
            _console.print(f"[red]Failed to download {rel_path}:[/red] {exc}")
            raise typer.Exit(1)

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        written.append(display_path)

    # Summary
    _console.print(f"\n[bold green]✓ Installed {name}[/bold green]")
    if active_platform:
        _console.print(f"  Platform: {active_platform}")
    if written:
        _console.print(f"  Files written ({len(written)}):")
        for p in written:
            _console.print(f"    {p}")
    if skipped:
        _console.print(f"  [dim]Skipped ({len(skipped)}):[/dim]")
        for p in skipped:
            _console.print(f"    [dim]{p}[/dim]")
    if not active_platform:
        _console.print(
            "\n[dim]No platform selected. "
            "Re-run with [bold]--platform <platform>[/bold] to install into a platform folder.[/dim]"
        )
