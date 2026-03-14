"""Cursor platform adapter."""

from __future__ import annotations

from agentically.adapters.base import PlatformAdapter


class CursorAdapter(PlatformAdapter):
    name = "cursor"
    platform_dir = ".cursor"
    prompts_subdir = "commands"
    # Default prompt_dest (stem + ".md") is correct for Cursor.


_adapter = CursorAdapter()
