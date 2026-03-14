# Contributing to agentically

Thank you for wanting to contribute! The fastest way to contribute is to add a new agent system to the registry.

## Adding an Agent System

### 1. Clone the repository

```bash
git clone https://github.com/ai-superpowers/agentically.git
cd agentically
```

### 2. Create a folder for your agent system

```bash
mkdir agents/my-agent-system
```

Use a descriptive **kebab-case** name (e.g., `typescript-strict`, `test-driven-dev`, `security-first`).

### 3. Add your files

At minimum, include a `README.md`:

```
agents/my-agent-system/
  README.md          ← required: describe what your agent system does
  /prompts           ← recommended: core instructions for AI assistants
  /skills			 ← recommended:  skills for AI assistants
  /memory			 ← optional:  memory structures for AI assistants
  ...                ← any other files your agent system needs
```

**README.md must include:**
- What the agent system does
- How to use the agent system
- What files it installs
- Example usage with `agentically create <name>`

### 4. Keep it platform-agnostic

Agent systems in this registry should work regardless of the user's coding platform (Copilot, Claude, Kiro, etc.). The `agentically` CLI handles platform-specific adaptations via `--platform`.

If your agent system is inherently platform-specific, document this clearly in your `README.md`.

### 5. Open a Pull Request

Push your branch and open a PR against `main`. Include:
- A brief description of what your agent system does
- Any special usage instructions

Maintainers will review and merge it. Once merged, your agent system is immediately available via:

```bash
agentically create my-agent-system
```


## Questions?

Open a GitHub issue if you have questions or want to discuss an idea before building it.
