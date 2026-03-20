# Configuration

agentically reads its registry location from environment variables. Override these to point the CLI at a fork, a private registry, or a local test repository.

## Environment variables

| Variable             | Default          | Description                                                   |
| -------------------- | ---------------- | ------------------------------------------------------------- |
| `AGENTICALLY_ORG`    | `ai-superpowers` | GitHub organisation or user that owns the registry repository |
| `AGENTICALLY_REPO`   | `agentically`    | Repository name                                               |
| `AGENTICALLY_BRANCH` | `main`           | Branch to read agent systems from                             |

All three variables are read at import time from `agentically._config`. If a variable is not set, the default value is used.

## Example: using a fork

```bash
export AGENTICALLY_ORG=my-org
export AGENTICALLY_REPO=my-hub
export AGENTICALLY_BRANCH=main

agentically explore
agentically create my-custom-agent
```

## Example: local testing with a branch

```bash
export AGENTICALLY_ORG=my-github-username
export AGENTICALLY_REPO=agentically
export AGENTICALLY_BRANCH=feature/new-agent

agentically create new-agent --platform copilot
```

!!! note
    Environment variables must be set in the shell session before running agentically. They are not persisted between sessions.
