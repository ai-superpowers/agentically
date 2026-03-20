# Prompt Systems Registry

This directory is the community registry for `agentically`. Each subdirectory is a **prompt system** that developers can discover and install with the `agentically` CLI.

## Directory Structure

```
prompt-systems/
  my-prompt-system/           ← each folder is one prompt system
    prompts/                 ← recommended: prompt/command files for AI tools
      my-command.md
      ...
    skills/                  ← recommended: agent skills
      my-skill/
        SKILL.md
      ...
    memory/                  ← optional: agent-internal working state
    README.md                ← required: describes what the prompt system does
```

### Why this structure?

The `prompts/` and `skills/` layout is a platform-agnostic standard. When users
run `agentically create <name> --platform <platform>`, the CLI maps these directories
to the right locations for each tool:

| Platform  | `prompts/*.md` becomes            | `skills/<s>/SKILL.md` becomes |
| --------- | --------------------------------- | ----------------------------- |
| `cursor`  | `.cursor/commands/*.md`           | `.cursor/skills/<s>/SKILL.md` |
| `claude`  | `.claude/commands/<pre>/<suf>.md` | `.claude/skills/<s>/SKILL.md` |
| `kiro`    | `.kiro/prompts/*.prompt.md`       | `.kiro/skills/<s>/SKILL.md`   |
| `copilot` | `.github/prompts/*.prompt.md`     | `.github/skills/<s>/SKILL.md` |

> **Note on Claude command naming:** for prompts, the first `-` in the filename is
> used as a folder separator. `my-command.md` → `.claude/commands/my/command.md`.

## Legacy Format (backward compatible)

Prompt systems that don't use `prompts/` or `skills/` directories still work.
In that case, adapters fall back to looking for `instructions.md` or `README.md`
and placing the content in the platform's primary instruction file.

## Adding Your Prompt System

1. Fork this repository.
2. Create a new folder under `prompt-systems/` with a kebab-case name (e.g., `prompt-systems/my-prompt-system/`).
3. Add your files following the structure above.
4. Open a Pull Request — maintainers will review and merge it into the registry.

## Naming Guidelines

- Use kebab-case: `my-great-prompt`
- Be descriptive but concise
- Avoid generic names like `prompt` or `system`

## Questions?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full contribution guide.
