---
description: Design a new agent system — interview the user, map workflows to prompts/skills/memory, and produce a spec ready for building
---

Design a new agent system for the agentically registry.

I'll interview you about the workflow you want to automate, then produce a structured spec (`memory/in-progress/<name>/spec.md`) that the build step can turn directly into files.

---

**Input**: Optionally provide a name or description after the command (e.g., `/agentsystem:design code-reviewer` or `/agentsystem:design something that reviews PRs`). If nothing is provided, I'll ask.

---

## Steps

### 1. Gather intent

If the user hasn't described what they want to build, ask (open-ended — use AskUserQuestion if available):

> "What do you want your agent system to do? Describe the workflow or problem it solves in plain terms."

Understand at a minimum:
- The core repeatable task or workflow
- Who runs it (developer, team lead, CI, etc.)
- Whether it needs any external CLIs, APIs, or tools

**Do NOT proceed without a clear answer to what the agent system does.**

---

### 2. Derive and confirm the name

From the description, suggest a kebab-case name (e.g., `pr-reviewer`, `deploy-helper`, `doc-writer`).

Rules:
- Kebab-case only (lowercase, hyphens)
- 2–4 words, descriptive and specific
- Avoid generics: no `agent`, `system`, `tool`, `helper` alone

Confirm with the user:
> "I'll name this `<suggested-name>`. Does that work, or would you like a different name?"

Wait for confirmation before continuing.

---

### 3. Map the workflow

Ask the user:
> "Walk me through what this agent would do, step by step. Start from 'user opens their editor' and go through to 'task is done'."

For each step they describe, classify it:

| Step type                 | What it means                       | Becomes           |
| ------------------------- | ----------------------------------- | ----------------- |
| User kicks off a workflow | The user types a command or trigger | A **prompt** file |
| Background behavior       | AI applies knowledge automatically  | A **skill** file  |
| State that persists       | Info needed across sessions         | **Memory** entry  |

Ask follow-up questions for anything unclear:
- "Does the user explicitly trigger this step, or does the AI do it automatically?"
- "Does the agent need to remember anything between sessions?"
- "What CLIs or external tools does this step need?"

---

### 4. Design each prompt

For each user-invokable step, pin down:
- **Filename**: `<agentname>-<commandname>.md`
  - The part before the first `-` becomes the namespace in Claude (e.g., `review-start.md` → `/review:start`)
  - Keep the namespace consistent across all prompts in this agent system
- **Description**: One sentence — what it does AND when to invoke it
- **Inputs**: What argument or context does the user provide? What if it's missing?
- **Key steps**: 4–8 numbered steps the AI will follow
- **Exit / next step**: What does the user do after? (suggest the next prompt in the chain)

Write these up clearly before moving on.

---

### 5. Design each skill

For each persistent behavior or background knowledge:
- **Folder name**: kebab-case (e.g., `validate`, `format-output`)
- **Description**: One sentence — when should AI auto-apply this skill?
- **Content type**: Is this reference knowledge? A reusable sub-procedure? Domain rules?

---

### 6. Design memory layout

Ask: "What state does this agent need to remember between sessions?"

Common patterns:
- `config.yaml` — user configuration and project context (set once, read often)
- `<records>/` — directory for work-in-progress tracking (e.g., one file per in-flight item)
- `<notes>.md` — accumulated knowledge the AI builds up over time

Design the minimum needed. Don't over-engineer.

---

### 7. Write the spec

Create `memory/in-progress/<name>/spec.md` with this structure:

```markdown
# Agent System Spec: <name>

## Purpose
<One paragraph: what it does, who uses it, why it's useful>

## Target User
<Who runs these prompts? In what context?>

## Workflow Overview
1. <Step 1>
2. <Step 2>
...

## Prompts

| Filename  | Claude command | Description   | Required inputs | Key steps |
| --------- | -------------- | ------------- | --------------- | --------- |
| <file.md> | `/prefix:cmd`  | <description> | <inputs>        | <summary> |

## Skills

| Folder name | Description   | Auto-invocation trigger |
| ----------- | ------------- | ----------------------- |
| <name>      | <description> | <when AI should use it> |

## Memory Structure

| Path          | Type        | Purpose                    |
| ------------- | ----------- | -------------------------- |
| `config.yaml` | Config      | <what the user configures> |
| `<path>/`     | Working dir | <what gets stored here>    |

## Platform Notes
<Any platform-specific considerations, e.g., "Requires X CLI on PATH">

## Open Questions
<Anything still unclear that needs answering before building>
```

---

### 8. Confirm and hand off

Show the spec to the user. Ask:

> "Does this capture what you had in mind? Any changes before I build it?"

If they want changes, update the spec and ask again.

Once confirmed, say:

> "Spec saved to `memory/in-progress/<name>/spec.md`. Run `/agentsystem:build <name>` to generate all the files."
