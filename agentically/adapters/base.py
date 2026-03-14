"""Shared base class for all platform adapters.

The ``dest_for`` method maps every agent-relative path directly to its final
installed location inside ``<platform_dir>/``:

  * ``prompts/*.md``            →  ``<platform_dir>/<prompts_subdir>/…``
  * ``skills/<name>/SKILL.md``  →  ``<platform_dir>/<skills_subdir>/<name>/SKILL.md``
  * ``memory/**``               →  ``<platform_dir>/memory/**``
  * ``README.md``               →  ``<platform_dir>/<agent-name>-README.md``

Files are written directly to these destinations by the ``create`` command, so
stacking multiple agent systems is safe: prompts and skills are appended into
the same folder without overwriting each other.

To add a new platform:
  1. Create ``agentically/adapters/<platform>.py``.
  2. Subclass ``PlatformAdapter``, set ``name``, ``platform_dir``,
     ``prompts_subdir``; override ``prompt_dest`` if your platform uses a
     different filename convention (e.g. ``.prompt.md`` suffix or a
     subfolder split on ``-``).
  3. Add ``_adapter = MyAdapter()`` at module level.
  4. Register it in ``agentically/adapters/__init__.py``.
"""

from __future__ import annotations

from pathlib import Path


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

    def dest_for(self, cwd: Path, agent_name: str, rel_path: Path) -> Path:
        """Map an agent-relative *rel_path* to its final installed location.

        Mapping rules:

        - ``prompts/<stem>.md``  → ``<platform_dir>/<prompts_subdir>/…`` (via ``prompt_dest``)
        - ``skills/<rest>``      → ``<platform_dir>/<skills_subdir>/<rest>``
        - ``memory/<rest>``      → ``<platform_dir>/memory/<rest>``
        - ``README.md``          → ``<platform_dir>/<agent_name>-README.md``
        - anything else          → ``<platform_dir>/<rel_path>``
        """
        parts = rel_path.parts
        platform_root = cwd / self.platform_dir
        if parts[0] == "prompts" and rel_path.suffix == ".md":
            return self.prompt_dest(platform_root / self.prompts_subdir, rel_path.stem)
        if parts[0] == "skills":
            return platform_root / self.skills_subdir / Path(*parts[1:])
        if parts[0] == "memory":
            return platform_root / "memory" / Path(*parts[1:])
        if len(parts) == 1 and parts[0] == "README.md":
            return platform_root / f"{agent_name}-README.md"
        return platform_root / rel_path

    def prompt_dest(self, prompts_base: Path, stem: str) -> Path:
        """Return the destination path for a prompt file given its *stem*.

        Default: ``<prompts_base>/<stem>.md``.  Override for platforms that
        use a different naming convention (e.g. ``.prompt.md`` suffix or a
        subfolder split on ``-``).
        """
        return prompts_base / f"{stem}.md"
