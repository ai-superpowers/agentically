"""Platform adapters — direct-placement file routing per coding platform.

To add a new platform adapter:
  1. Create ``agentically/adapters/<platform>.py`` with a ``PlatformAdapter``
     subclass and a module-level ``_adapter = MyAdapter()``.
  2. Import ``_adapter`` here and add it to ``_ADAPTERS``.
  3. Add the platform name to ``SUPPORTED_PLATFORMS``.
"""

from __future__ import annotations

from pathlib import Path

from agentically.adapters.base import PlatformAdapter
from agentically.adapters.claude import _adapter as _claude_adapter
from agentically.adapters.copilot import _adapter as _copilot_adapter
from agentically.adapters.cursor import _adapter as _cursor_adapter
from agentically.adapters.kiro import _adapter as _kiro_adapter

# Supported platform identifiers and their adapter instances.

SUPPORTED_PLATFORMS: frozenset[str] = frozenset({"claude", "copilot", "cursor", "kiro"})

_ADAPTERS: dict[str, PlatformAdapter] = {
    "claude": _claude_adapter,
    "copilot": _copilot_adapter,
    "cursor": _cursor_adapter,
    "kiro": _kiro_adapter,
}


def get_adapter(platform: str) -> PlatformAdapter:
    """Return the ``PlatformAdapter`` instance for *platform*."""
    return _ADAPTERS[platform]


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
