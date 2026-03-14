"""Shared base class for all platform adapters.

Agent systems are installed verbatim by the ``use`` command, so all folders
(``memory/``, ``agents/``, etc.) are already in place at *cwd* when the
adapter runs.  The adapter's only responsibility is to copy the two
platform-agnostic folders into their platform-specific locations:

  * ``prompts/*.md``        →  ``<platform_dir>/<prompts_subdir>/``
  * ``skills/<name>/SKILL.md``  →  ``<platform_dir>/<skills_subdir>/<name>/SKILL.md``

To add a new platform:
  1. Create ``agentically/adapters/<platform>.py``.
  2. Subclass ``PlatformAdapter``, set ``name``, ``platform_dir``,
     ``prompts_subdir``; override ``prompt_dest`` if your platform uses a
     different filename convention.
  3. Add ``_adapter = MyAdapter(); adapt = _adapter.adapt`` at module level.
  4. Register it in ``agentically/adapters/__init__.py``.
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

console = Console()


class PlatformAdapter:
    """Base for platform-specific post-install adapters.

    Required class attributes
    -------------------------
    name : str
        Platform identifier used in log messages, e.g. ``"cursor"``.
    platform_dir : str
        Root config directory relative to cwd, e.g. ``".cursor"``.
    prompts_subdir : str
        Subdirectory under ``platform_dir`` for prompt files.

    Optional class attribute
    ------------------------
    skills_subdir : str
        Subdirectory under ``platform_dir`` for skill folders.
        Defaults to ``"skills"``.
    """

    name: str
    platform_dir: str
    prompts_subdir: str
    skills_subdir: str = "skills"

    def adapt(self, cwd: Path, agent_name: str, written: list[Path]) -> None:
        """Copy ``prompts/`` and ``skills/`` into the platform config directories.

        All other directories present in *cwd* (e.g. ``memory/``, ``agents/``)
        are already in place from the install step and are left untouched.
        """
        platform_root = cwd / self.platform_dir
        self._copy_prompts(cwd / "prompts", platform_root / self.prompts_subdir, cwd)
        self._copy_skills(cwd / "skills", platform_root / self.skills_subdir, cwd)

    def prompt_dest(self, prompts_base: Path, stem: str) -> Path:
        """Return the destination path for a prompt file given its *stem*.

        Default: ``<prompts_base>/<stem>.md``.  Override for platforms that
        use a different naming convention (e.g. ``.prompt.md`` suffix or a
        subfolder split on ``-``).
        """
        return prompts_base / f"{stem}.md"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _copy_prompts(self, prompts_dir: Path, prompts_base: Path, cwd: Path) -> None:
        if not prompts_dir.is_dir():
            return
        for prompt_file in sorted(prompts_dir.glob("*.md")):
            dest = self.prompt_dest(prompts_base, prompt_file.stem)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(prompt_file.read_bytes())
            console.print(f"  [dim]({self.name}) Created {dest.relative_to(cwd)}[/dim]")

    def _copy_skills(self, skills_dir: Path, skills_base: Path, cwd: Path) -> None:
        if not skills_dir.is_dir():
            return
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                target = skills_base / skill_dir.name
                target.mkdir(parents=True, exist_ok=True)
                dest = target / "SKILL.md"
                dest.write_bytes(skill_md.read_bytes())
                console.print(
                    f"  [dim]({self.name}) Created {dest.relative_to(cwd)}[/dim]"
                )
