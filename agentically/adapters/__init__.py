"""Platform adapters — post-install file adaptations per coding platform.

To add a new platform adapter:
  1. Create ``agentically/adapters/<platform>.py`` with a ``PlatformAdapter``
     subclass and a module-level ``adapt = _adapter.adapt``.
  2. Import the ``adapt`` function here and add it to ``_ADAPTERS``.
  3. Add the platform name to ``SUPPORTED_PLATFORMS``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from agentically.adapters.base import PlatformAdapter
from agentically.adapters.claude import adapt as _claude_adapt
from agentically.adapters.copilot import adapt as _copilot_adapt
from agentically.adapters.cursor import adapt as _cursor_adapt
from agentically.adapters.kiro import adapt as _kiro_adapt

# Supported platform identifiers and their adapter functions.
# Each adapter signature: (cwd: Path, agent_name: str, written: list[Path]) -> None
AdapterFn = Callable[[Path, str, list[Path]], None]

SUPPORTED_PLATFORMS: frozenset[str] = frozenset({"claude", "copilot", "cursor", "kiro"})

_ADAPTERS: dict[str, AdapterFn] = {
    "claude": _claude_adapt,
    "copilot": _copilot_adapt,
    "cursor": _cursor_adapt,
    "kiro": _kiro_adapt,
}


def adapt(platform: str, cwd: Path, agent_name: str, written: list[Path]) -> None:
    """Apply the platform-specific adapter for the given platform."""
    _ADAPTERS[platform](cwd, agent_name, written)


def detect_platform(cwd: Path) -> str | None:
    """Best-effort detection of the active coding platform from filesystem signals."""
    if (cwd / ".cursor").is_dir():
        return "cursor"
    if (
        (cwd / ".github" / "copilot-instructions.md").exists()
        or (cwd / ".github" / "prompts").is_dir()
    ):
        return "copilot"
    if (cwd / "CLAUDE.md").exists() or (cwd / ".claude").is_dir():
        return "claude"
    if (cwd / ".kiro").is_dir():
        return "kiro"
    return None
