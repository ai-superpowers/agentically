# Commands

The `agentically.commands` package contains the implementation of each CLI subcommand. Two commands are registered: `explore` and `create`.

## Module: `agentically.commands.explore`

`explore_command` fetches the list of available agent systems from the registry and opens the registry URL in the user's browser.

::: agentically.commands.explore
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"

---

## Module: `agentically.commands.create`

`create_command` downloads an agent system from the registry and writes its files to disk, optionally routing through a platform adapter.

::: agentically.commands.create
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"

---

## Command signatures

### `agentically explore`

```
agentically explore
```

No arguments or options. Opens the registry and prints available agent system names.

### `agentically create`

```
agentically create <name> [OPTIONS]
```

| Argument / Option   | Type   | Default  | Description                                                         |
| ------------------- | ------ | -------- | ------------------------------------------------------------------- |
| `name`              | `str`  | required | Name of the agent system to install                                 |
| `--platform` / `-p` | `str`  | `None`   | Platform adaptation to apply: `copilot`, `claude`, `kiro`, `cursor` |
| `--yes` / `-y`      | `bool` | `False`  | Skip all confirmation prompts                                       |
| `--force` / `-f`    | `bool` | `False`  | Overwrite existing files without asking                             |

See [Install an Agent System](../guides/create.md) for a full usage guide.
