---
name: agentsystem-design
description: Design and spec a new agentically agent system. Use when the user wants to plan, architect, or think through what prompts/skills/memory an agent system should have before building it.
license: MIT
compatibility: No external dependencies.
metadata:
  author: community
  version: "1.0"
---

Design agent systems for the agentically registry.

## When to use this skill

Invoke when the user:
- Wants to create a new agent system and is not sure where to start
- Is trying to structure prompts and skills for a workflow they've described
- Needs help deciding what should be a prompt vs. a skill vs. memory
- Is iterating on a spec and wants structural feedback
- Asks "how should I organize my agent system?"

## The agentically format

Every agent system in the registry follows this layout:

```
agents/<name>/
  prompts/        ← user-invokable AI commands (.md files with YAML frontmatter)
  skills/         ← persistent AI behaviors (<skill-name>/SKILL.md)
  memory/         ← agent runtime state (config.yaml, working directories)
  README.md       ← required: describes the agent system
```

Platform install destinations (via `agentically create <name> --platform <p>`):

| Platform | `prompts/<stem>.md` → | `skills/<s>/SKILL.md` → |
|----------|-----------------------|------------------------|
| cursor   | `.cursor/commands/<stem>.md` | `.cursor/skills/<s>/SKILL.md` |
| copilot  | `.github/prompts/<stem>.prompt.md` | `.github/skills/<s>/SKILL.md` |
| claude   | `.claude/commands/<prefix>/<cmd>.md` (split on first `-`) | `.claude/skills/<s>/SKILL.md` |
| kiro     | `.kiro/prompts/<stem>.prompt.md` | `.kiro/skills/<s>/SKILL.md` |

## Prompts vs. skills vs. memory

**Create a prompt (prompts/*.md) when:**
- The user explicitly triggers a workflow with a command
- There is a multi-step process to guide from start to finish
- The step requires gathering input from the user before proceeding

**Create a skill (skills/<name>/SKILL.md) when:**
- The AI should automatically apply behavior whenever relevant
- It's reusable knowledge or a sub-procedure used by multiple prompts
- No explicit user command is needed to trigger it

**Create a memory entry when:**
- State must survive between separate sessions
- Configuration is set once and read repeatedly
- Work-in-progress tracking is needed across days

## Naming conventions

**Prompt filenames:** `<prefix>-<command>.md`
- The part before the first `-` becomes the namespace in Claude
- Example: `review-start.md` → `/review:start` in Claude
- All prompts in one agent system should share the same `<prefix>`
- Prefix should match (or be a short form of) the agent system name

**Skill folder names:** descriptive, kebab-case
- Example: `validate`, `format-output`, `analyze-diff`

**Agent system names:** kebab-case, 2–4 words, specific
- Good: `pr-reviewer`, `test-generator`, `deploy-helper`
- Avoid: `agent`, `my-agent`, `system`, `helper` alone

## Required frontmatter

**Prompt file:**
```yaml
---
description: One-line description — what it does AND when to invoke it
---
```

**SKILL.md:**
```yaml
---
name: <agent-name>-<skill-name>
description: One-line description specific enough to trigger auto-invocation
license: MIT
compatibility: <"No external dependencies." or list of requirements>
metadata:
  author: <author or "community">
  version: "1.0"
---
```

## Design interview questions

When helping a user design an agent system, work through:

1. **What workflow?** — What repeatable task does this automate? Walk me through it from trigger to completion.
2. **Who triggers what?** — Which steps does the user explicitly kick off? (→ prompts) Which happen automatically? (→ skills)
3. **What persists?** — What state does the agent need to remember between sessions? (→ memory)
4. **What tools?** — Does the agent need specific CLIs, APIs, or external services?
5. **Which platforms?** — cursor, copilot, claude, kiro, or all of them?

## Spec format

A complete design spec lives at `memory/in-progress/<name>/spec.md` and includes:
- Purpose and target user
- Workflow overview (numbered steps)
- Prompts table (filename, description, inputs, key steps)
- Skills table (folder, description, auto-invocation trigger)
- Memory structure (path, type, purpose)
- Platform notes and open questions
