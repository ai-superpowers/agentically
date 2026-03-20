# Registry

The agentically registry is a GitHub repository that hosts community-maintained AI agent systems. Understanding how it is structured helps you contribute new agent systems and configure agentically for forks or private registries.

## What the registry is

The registry lives at [`ai-superpowers/agentically`](https://github.com/ai-superpowers/agentically) on GitHub. Every agent system is a named subdirectory under `prompt-systems/`:

```
prompt-systems/
  prompt-system/
    README.md
    prompts/
    skills/
    memory/
  my-agent/
    README.md
    ...
```

When you run `agentically explore`, the CLI queries the GitHub Contents API for the list of subdirectories under `prompt-systems/` and displays them. When you run `agentically create <name>`, it fetches every file blob under `prompt-systems/<name>/` using the recursive Git Trees API and downloads them to your local project.

## Registry API calls

| Operation          | Endpoint                                                     |
| ------------------ | ------------------------------------------------------------ |
| List agent systems | `GET /repos/{org}/{repo}/contents/prompt-systems`            |
| Fetch file tree    | `GET /repos/{org}/{repo}/git/trees/{branch}?recursive=1`     |
| Download a file    | `GET raw.githubusercontent.com/{org}/{repo}/{branch}/{path}` |

The listing is cached in a temporary file for one hour (`TTL = 3600 s`) so repeated `explore` calls don't hit the GitHub API on every run.

## Environment variable overrides

You can point agentically at a different GitHub repository — useful for forks, private registries, or local testing:

| Variable             | Default          | Description                                             |
| -------------------- | ---------------- | ------------------------------------------------------- |
| `AGENTICALLY_ORG`    | `ai-superpowers` | GitHub organisation or user that owns the registry repo |
| `AGENTICALLY_REPO`   | `agentically`    | Repository name                                         |
| `AGENTICALLY_BRANCH` | `main`           | Branch to read from                                     |

```bash
export AGENTICALLY_ORG=my-org
export AGENTICALLY_REPO=my-hub
export AGENTICALLY_BRANCH=main

agentically explore   # now reads from my-org/my-hub
```

## Agent system structure

An agent system directory may contain any files. The `agentically create` command downloads everything under `prompt-systems/<name>/` verbatim. The optional `--platform` flag then routes each file to the correct subdirectory for the target coding platform via a [Platform Adapter](platform-adapters.md).

The following subdirectory names carry special routing meaning when a platform adapter is active:

| Subdirectory  | Routed to                               |
| ------------- | --------------------------------------- |
| `prompts/`    | Platform's prompt/commands folder       |
| `skills/`     | Platform's skills folder                |
| `memory/`     | Platform's memory folder                |
| `README.md`   | `<platform_dir>/<agent-name>-README.md` |
| anything else | `<platform_dir>/<original path>`        |

See [Platform Adapters](platform-adapters.md) for routing details per platform.
