# CLI Application

The `agentically.main` module defines the root Typer application and wires up all subcommands. It is the package's public entry point — the `agentically` console script installed by pip points here.

## Module: `agentically.main`

::: agentically.main
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"

---

## Module: `agentically` (package)

The package `__init__.py` exports the Typer `app` object for programmatic use.

::: agentically
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"

---

## Console script

The `agentically` command is registered in `pyproject.toml` as:

```toml
[project.scripts]
agentically = "agentically.main:app"
```

Running `agentically --help` displays the top-level help; running `agentically <command> --help` shows help for that subcommand.

```bash
agentically --help
agentically create --help
agentically explore --help
```

## Version flag

Pass `--version` / `-v` to print the installed package version and exit:

```bash
agentically --version
# → agentically 0.3.0
```
