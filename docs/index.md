# agentically

A CLI that gives developers a single place to discover and install community-maintained AI agent systems.

Agent systems are named collections of AI prompt, skill, and memory files. `agentically` connects you to a community registry of these systems and installs them directly into your project — adapting file layouts automatically for your coding platform of choice (GitHub Copilot, Claude Code, Kiro, Cursor, and others).

## Key features

- **Discover** — browse all available agent systems in the community registry with `agentically explore`.
- **Install** — download any agent system into your project with `agentically create <name>`.
- **Platform-aware** — automatically routes files into the right directories for Copilot, Claude, Kiro, or Cursor via `--platform`.
- **Composable** — stack multiple agent systems in the same project without overwriting each other.

## Quick start

```bash
pip install agentically
agentically explore          # browse the registry
agentically create prompt-system --platform copilot
```

See [Getting Started](getting-started/installation.md) to install and run your first agent system.
