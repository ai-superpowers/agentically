"""Kiro platform adapter."""

from __future__ import annotations

from pathlib import Path

from agentically.adapters.base import PlatformAdapter


class KiroAdapter(PlatformAdapter):
    name = "kiro"
    platform_dir = ".kiro"
    prompts_subdir = "prompts"

    def prompt_dest(self, prompts_base: Path, stem: str) -> Path:
        return prompts_base / f"{stem}.prompt.md"


_adapter = KiroAdapter()
adapt = _adapter.adapt
