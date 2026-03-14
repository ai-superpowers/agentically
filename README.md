# agentically

A CLI that gives developers a single place to discover and install community-maintained AI agent systems.

## Install

```bash
pip install agentically
```

## Commands

### `agentically explore`

Opens the community registry in your browser so you can browse available agent systems.

```bash
agentically explore
```

### `agentically use <name>`

Downloads the named agent system from the registry into your current working directory.

```bash
mkdir my-project
cd my-project
agentically use example-agent
```

Options:

| Flag                | Description                                                                     |
| ------------------- | ------------------------------------------------------------------------------- |
| `--platform` / `-p` | Apply platform-specific adaptations after install (`copilot`, `claude`, `kiro`) |
| `--yes` / `-y`      | Skip the large-install confirmation prompt                                      |
| `--force` / `-f`    | Overwrite existing files without prompting                                      |

### Platform adaptation

```bash
# GitHub Copilot — adds content to .github/copilot-instructions.md
agentically use example-agent --platform copilot

# Claude Code — creates or appends to CLAUDE.md
agentically use example-agent --platform claude

# Kiro — creates .kiro/steering/<name>.md
agentically use example-agent --platform kiro
```

The CLI will also auto-detect your platform if you have existing config files (`.github/copilot-instructions.md`, `CLAUDE.md`, `.kiro/`).

## Workflow

```bash
mkdir new-project
cd new-project
agentically explore          # browse the registry
agentically use some-agent   # install an agent system
```

After installing, the agent system's prompt and instruction files will be available in your project for use with your AI coding tool of choice.

## Configuration

Override the registry location via environment variables (useful for forks or local testing):

```bash
export AGENTICALLY_ORG=my-org
export AGENTICALLY_REPO=my-hub
export AGENTICALLY_BRANCH=main
```

## Contributing an Agent System

See [CONTRIBUTING.md](CONTRIBUTING.md) to add your own agent system to the registry.
