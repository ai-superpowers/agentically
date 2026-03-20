# Quick Start

This guide walks you through discovering and installing an agent system from end to end. You need agentically installed — see [Installation](installation.md) if you haven't done that yet.

## 1. Browse available agent systems

```bash
agentically explore
```

This opens the community registry in your browser and prints the current list of available agent systems in your terminal:

```
Opening registry: https://github.com/ai-superpowers/agentically/tree/main/prompt-systems

3 agent system(s) available:
  • prompt-system
  • ...
```

## 2. Create a project directory

```bash
mkdir my-project
cd my-project
```

## 3. Install an agent system

```bash
agentically create prompt-system
```

agentically auto-detects your coding platform (Copilot, Claude, Kiro, Cursor) from files in the current directory and asks you to confirm before writing any files:

```
Apply a platform adaptation?
  1. claude
  2. copilot  (detected)
  3. cursor
  4. kiro
  5. skip

Enter number [2]:
```

Press **Enter** to accept the detected platform, or type another number.

## 4. Supply a platform explicitly (optional)

Skip the prompt by passing `--platform`:

```bash
agentically create prompt-system --platform copilot
```

```
✓ Installed prompt-system
  Platform: copilot
  Files written (6):
    .github/prompts/promptsystem-build.prompt.md
    .github/prompts/promptsystem-design.prompt.md
    ...
```

## 5. Start using the agent system

The installed prompt and skill files are now in your project. Open your AI coding tool and invoke the prompts — for example, in GitHub Copilot Chat: `/promptsystem-build`.

## Options reference

| Flag         | Short | Description                                             |
| ------------ | ----- | ------------------------------------------------------- |
| `--platform` | `-p`  | Set the platform: `copilot`, `claude`, `kiro`, `cursor` |
| `--yes`      | `-y`  | Skip all confirmation prompts                           |
| `--force`    | `-f`  | Overwrite existing files without asking                 |

See [Install an Agent System](../guides/create.md) for a full guide including conflict resolution.
