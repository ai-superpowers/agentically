# Install an Agent System

The `agentically create` command downloads an agent system from the registry into your current directory, optionally routing its files into the correct layout for your coding platform.

## Basic usage

```bash
agentically create <name>
```

Replace `<name>` with the name of any agent system listed by `agentically explore`.

## Step-by-step walkthrough

### 1. Navigate to your project

```bash
mkdir my-project
cd my-project
```

### 2. Run create

```bash
agentically create prompt-system
```

### 3. Choose a platform adaptation

agentically scans the current directory for known platform signals and offers a numbered menu:

```
Apply a platform adaptation?
  1. claude
  2. copilot  (detected)
  3. cursor
  4. kiro
  5. skip

Enter number [2]:
```

Press **Enter** to accept the auto-detected platform, or type a number and press Enter. Choose **skip** to install files at the project root without any routing.

### 4. Confirm large installs

If the agent system contains more than 50 files, agentically asks for confirmation before downloading:

```
Warning: This agent system contains 62 files.
Continue with download? [y/N]:
```

### 5. Review the summary

```
✓ Installed prompt-system
  Platform: copilot
  Files written (6):
    .github/prompts/promptsystem-build.prompt.md
    .github/prompts/promptsystem-test.prompt.md
    .github/skills/build/SKILL.md
    .github/skills/test/SKILL.md
    .github/memory/config.yaml
    .github/prompt-system-README.md
```

## Options

| Flag                | Short | Description                                                                      |
| ------------------- | ----- | -------------------------------------------------------------------------------- |
| `--platform <name>` | `-p`  | Platform to route files for: `copilot`, `claude`, `kiro`, `cursor`               |
| `--yes`             | `-y`  | Accept all prompts non-interactively (large-install guard, platform auto-detect) |
| `--force`           | `-f`  | Overwrite existing files without per-file confirmation                           |

### Specify the platform explicitly

```bash
agentically create prompt-system --platform claude
```

### Non-interactive install

```bash
agentically create prompt-system --platform copilot --yes
```

### Overwrite existing files

```bash
agentically create prompt-system --platform copilot --force
```

## Conflict resolution

If a destination file already exists and `--force` was **not** passed, agentically prompts for each conflict:

```
Conflict: .github/prompts/promptsystem-build.prompt.md already exists. Overwrite? [y/N]:
```

Answer `n` (or press Enter) to skip that file. Skipped files are listed in the summary:

```
  Skipped (1):
    .github/prompts/promptsystem-build.prompt.md
```

## Stacking multiple agent systems

Because each file is routed directly into the platform directory using the agent system's name as a folder prefix for README files, and prompts/skills land in shared subdirectories, you can safely run `create` multiple times:

```bash
agentically create prompt-system --platform copilot
agentically create security-first --platform copilot
```

Files from different agent systems do not overwrite each other as long as their prompt filenames differ.

## See also

- [Registry](../concepts/registry.md) — how the registry is structured
- [Platform Adapters](../concepts/platform-adapters.md) — file routing rules per platform
- [Commands API Reference](../api/commands.md) — `create_command` signature and internals
