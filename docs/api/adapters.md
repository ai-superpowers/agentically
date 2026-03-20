# Adapters

The `agentically.adapters` package provides platform-specific file routing for the `create` command. Each supported coding platform has a dedicated adapter subclass that maps agent-relative paths to the correct installed locations on disk.

## Module: `agentically.adapters`

::: agentically.adapters
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"

---

## Base class: `agentically.adapters.base`

`PlatformAdapter` is the abstract base that all platform adapters subclass. It implements the `dest_for` routing method and the overridable `prompt_dest` hook.

::: agentically.adapters.base
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"

---

## Platform adapter modules

### Copilot — `agentically.adapters.copilot`

Routes files into `.github/`. Prompt files are renamed `<stem>.prompt.md`.

::: agentically.adapters.copilot
    options:
      show_source: false
      filters:
        - "!^_"

### Claude — `agentically.adapters.claude`

Routes files into `.claude/`. Prompt filenames are split on the first `-`: `myagent-apply` → `.claude/commands/myagent/apply.md`.

::: agentically.adapters.claude
    options:
      show_source: false
      filters:
        - "!^_"

### Cursor — `agentically.adapters.cursor`

Routes files into `.cursor/`. Prompt files keep their original stem: `<stem>.md`.

::: agentically.adapters.cursor
    options:
      show_source: false
      filters:
        - "!^_"

### Kiro — `agentically.adapters.kiro`

Routes files into `.kiro/`. Prompt files are renamed `<stem>.prompt.md`.

::: agentically.adapters.kiro
    options:
      show_source: false
      filters:
        - "!^_"

---

## File routing reference

The `dest_for(cwd, agent_name, rel_path)` method on any adapter applies these rules in order:

| Agent-relative path | Destination                                           |
| ------------------- | ----------------------------------------------------- |
| `prompts/<stem>.md` | `<platform_dir>/<prompts_subdir>/<prompt_dest(stem)>` |
| `skills/<rest>`     | `<platform_dir>/skills/<rest>`                        |
| `memory/<rest>`     | `<platform_dir>/memory/<rest>`                        |
| `README.md`         | `<platform_dir>/<agent-name>-README.md`               |
| anything else       | `<platform_dir>/<rel_path>`                           |

See [Platform Adapters concept page](../concepts/platform-adapters.md) for a comparison table and instructions on adding a new platform.
