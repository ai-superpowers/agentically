"""Claude Code platform adapter.

Note on prompt naming: the first ``-`` in a prompt filename is used as a
folder separator so ``opsx-apply.md`` → ``.claude/commands/opsx/apply.md``.
"""

from __future__ import annotations

from pathlib import Path

from agentically.adapters.base import PlatformAdapter


class ClaudeAdapter(PlatformAdapter):
    name = "claude"
    platform_dir = ".claude"
    prompts_subdir = "commands"

    def prompt_dest(self, prompts_base: Path, stem: str) -> Path:
        """Split on first '-': ``myagent-apply`` → ``commands/myagent/apply.md``."""
        if "-" in stem:
            idx = stem.index("-")
            return prompts_base / stem[:idx] / f"{stem[idx + 1:]}.md"
        return prompts_base / f"{stem}.md"


_adapter = ClaudeAdapter()
