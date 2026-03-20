---
name: promptsystem-build
description: Build agentically agent system files from a spec. Use when writing prompt files, SKILL.md files, README, or memory config for an agent system under prompt-systems/<name>/.
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
prompt-systems/<name>/
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

Every prompt file must follow this structure (see templates in prompts/):

... (same guidance as other SKILL.md files) ...
