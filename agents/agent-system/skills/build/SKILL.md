---
name: agentsystem-build
description: Build agentically agent system files from a spec. Use when writing prompt files, SKILL.md files, README, or memory config for an agent system under agents/<name>/.
license: MIT
compatibility: No external dependencies.
metadata:
  author: community
  version: "1.0"
---

Build the files for an agentically agent system from a design spec.

## When to use this skill

Invoke when the user:
- Has a spec or clear description and wants to generate agent system files
- Is writing a prompt file and needs the correct format and quality bar
- Is writing a SKILL.md and needs the correct frontmatter
- Is building a README for a new agent system
- Needs to create a `memory/config.yaml` with the right structure

## File creation checklist

When building a complete agent system, create:

```
agents/<name>/
  prompts/                     ← one file per user-invokable command
    <prefix>-<command>.md
  skills/                      ← one folder per persistent behavior
    <skill-name>/
      SKILL.md
  memory/
    config.yaml                ← project context for the AI
    <working-dirs>/            ← subdirs for in-progress state
  README.md                    ← required: description and usage
```

## Prompt file format

Every prompt file must follow this structure:

```markdown
---
description: <one-line: what it does AND when to invoke it>
---

<Short intro: what this command does in 1-2 sentences.>

**Input**: <What the user provides. What happens if it's missing.>

---

## Steps

### 1. <Step title>
<Concrete action with specific tools, file paths, CLI commands.>

### 2. <Step title>
...

### N. <Completion step>
<What to display. What to suggest next.>
> "Run `/prefix:next-command` to continue."
```

**Prompt quality rules:**
- Steps are numbered and concrete — no vague instructions
- Every ambiguous case has an "if X then Y" branch
- Missing input cases are handled explicitly (ask or explain how to obtain it)
- File paths use the agentically layout (`agents/<name>/`, `memory/in-progress/`, etc.)
- CLI commands are spelled out exactly as the user types them
- Ends with a clear next-step that chains to the next prompt in the workflow

## SKILL.md format

```yaml
---
name: <agentname>-<skillname>
description: <specific enough for auto-invocation — explains when AI should use it>
license: MIT
compatibility: <"No external dependencies." or list of CLIs/packages needed>
metadata:
  author: <author or "community">
  version: "1.0"
---
```

**Skill body structure:**
- `## When to use this skill` — explicit triggers (user says X, context involves Y)
- `## <Core content>` — the knowledge, rules, or procedure itself
- Self-contained: the skill must be useful without reading any other file

## README format

```markdown
# <name>

<2–3 sentence hook: what it does and why it's useful.>

## What It Does
<One paragraph from the user's perspective.>

## Structure
<Directory tree with inline comments.>

## Usage
\`\`\`bash
agentically create <name>
\`\`\`

agentically create <name> --platform cursor
agentically create <name> --platform copilot
agentically create <name> --platform claude
agentically create <name> --platform kiro

## Prompts Reference
| File | Claude command | Description |
|------|---------------|-------------|

## Typical Workflow
/<prefix>:cmd1   ← what step 1 does
/<prefix>:cmd2   ← what step 2 does
```

## memory/config.yaml format

```yaml
# <Agent system name> configuration

context: |
  <Everything the AI needs to know about this project:
   - What the agent system does
   - File layout conventions
   - Naming rules
   - Any project-level context>
```

## Common mistakes to avoid

- Placeholder text left in files (`TODO`, `<insert here>`, `FIXME`)
- Frontmatter missing the `description` field in prompts
- SKILL.md missing `name`, `description`, or `license`
- Prompt steps that are too abstract ("analyze the code" with no specifics)
- Inconsistent prefix across prompt filenames in the same agent system
- Absolute paths hardcoded to the author's machine
- Secrets or credentials in memory files
