"""agentically explore — browse the agent systems registry."""

from __future__ import annotations

import json
import time
import tempfile
import webbrowser
from pathlib import Path

import requests
import typer
from rich.console import Console

from agentically._config import REGISTRY_ORG, REGISTRY_REPO, REGISTRY_BRANCH

REGISTRY_URL = (
    f"https://github.com/{REGISTRY_ORG}/{REGISTRY_REPO}"
    f"/tree/{REGISTRY_BRANCH}/prompt-systems"
)
_API_URL = (
    f"https://api.github.com/repos/{REGISTRY_ORG}/{REGISTRY_REPO}"
    f"/contents/prompt-systems"
)
_CACHE_FILE = Path(tempfile.gettempdir()) / "agentically_listing_cache.json"
_CACHE_TTL = 3600  # 1 hour

_console = Console()


def _load_cache() -> list[str] | None:
    """Return cached agent names if the cache is fresh, else None."""
    if not _CACHE_FILE.exists():
        return None
    try:
        data = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
        if time.time() - data.get("timestamp", 0) < _CACHE_TTL:
            return data["agents"]
    except (json.JSONDecodeError, KeyError, OSError):
        pass
    return None


def _save_cache(agents: list[str]) -> None:
    try:
        _CACHE_FILE.write_text(
            json.dumps({"timestamp": time.time(), "agents": agents}),
            encoding="utf-8",
        )
    except OSError:
        pass  # Cache write is best-effort


def _fetch_agent_names() -> list[str]:
    """Return the list of available agent system names from the registry."""
    cached = _load_cache()
    if cached is not None:
        return cached

    resp = requests.get(
        _API_URL,
        timeout=10,
        headers={"Accept": "application/vnd.github+json"},
    )
    resp.raise_for_status()
    names = [item["name"] for item in resp.json() if item["type"] == "dir"]
    _save_cache(names)
    return names


def explore_command() -> None:
    """Browse available agent systems in the community registry."""
    try:
        agent_names = _fetch_agent_names()
    except requests.RequestException as exc:
        _console.print(f"[red]Network error:[/red] {exc}")
        _console.print(
            "Check your connection. Registry is at: "
            f"[link={REGISTRY_URL}]{REGISTRY_URL}[/link]"
        )
        raise typer.Exit(1)

    _console.print(f"[bold]Opening registry:[/bold] {REGISTRY_URL}")
    opened = webbrowser.open(REGISTRY_URL)
    if not opened:
        _console.print(
            f"[yellow]Could not open browser.[/yellow] Visit: {REGISTRY_URL}"
        )

    if agent_names:
        _console.print(
            f"\n[bold]{len(agent_names)} agent system(s) available:[/bold]"
        )
        for name in agent_names:
            _console.print(f"  • {name}")
        _console.print(
            "\nRun [bold]agentically create <name>[/bold] to install one."
        )
    else:
        _console.print(
            "\n[dim]No agent systems found in the registry yet.[/dim]"
        )
