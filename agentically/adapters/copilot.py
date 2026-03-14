"""GitHub Copilot platform adapter."""

from __future__ import annotations

from pathlib import Path

from agentically.adapters.base import PlatformAdapter


class CopilotAdapter(PlatformAdapter):
    name = "copilot"
    platform_dir = ".github"
    prompts_subdir = "prompts"

    def prompt_dest(self, prompts_base: Path, stem: str) -> Path:
        return prompts_base / f"{stem}.prompt.md"


_adapter = CopilotAdapter()
