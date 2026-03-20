# Browse Agent Systems

The `agentically explore` command opens the community registry in your browser and lists all available agent systems in your terminal.

## Usage

```bash
agentically explore
```

## What it does

1. Fetches the list of agent system names from the GitHub registry API (or returns a cached result if the cache is less than one hour old).
2. Opens the registry URL in your default browser so you can read README files and explore each agent system's contents.
3. Prints the list of available agent system names to your terminal.

## Example output

```
Opening registry: https://github.com/ai-superpowers/agentically/tree/main/prompt-systems

3 agent system(s) available:
  • prompt-system
  • typescript-strict
  • security-first

Run agentically create <name> to install one.
```

## Offline or network errors

If the GitHub API is unreachable, `explore` prints an error message and the registry URL so you can open it manually:

```
Network error: <details>
Check your connection. Registry is at: https://github.com/...
```

## Caching

Agent system names are cached in a temporary file for **one hour** to avoid hitting the GitHub API on every run. To force a fresh fetch, delete the cache file:

```bash
# Linux / macOS
rm /tmp/agentically_listing_cache.json

# Windows PowerShell
Remove-Item $env:TEMP\agentically_listing_cache.json
```

## Next step

Once you've found an agent system you want, install it with:

```bash
agentically create <name>
```

See [Install an Agent System](create.md) for the full guide.
