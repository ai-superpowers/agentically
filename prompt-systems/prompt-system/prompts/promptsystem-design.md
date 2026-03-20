---
description: Design a new agent system — interview the user, map workflows to prompts/skills/memory, and produce a spec ready for building
---

Design a new agent system for the agentically registry.

I'll interview you about the workflow you want to automate, then produce a structured spec (`memory/in-progress/<name>/spec.md`) that the build step can turn directly into files.

---

**Input**: Optionally provide a name or description after the command (e.g., `/promptsystem-design code-reviewer` or `/promptsystem-design something that reviews PRs`). If nothing is provided, I'll ask.

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

For each step they describe, classify it as a prompt, skill, or memory as described in the templates.

---

### 4. Design each prompt

For each user-invokable step, pin down:
- **Filename**: `<agentname>-<commandname>.md`
- **Description**: One sentence — what it does AND when to invoke it
- **Inputs**: What argument or context does the user provide? What if it's missing?
- **Key steps**: 4–8 numbered steps the AI will follow
- **Exit / next step**: What does the user do after? (suggest the next prompt in the chain)

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
- `config.yaml` — user configuration and project context
- `<records>/` — directory for work-in-progress tracking
- `<notes>.md` — accumulated knowledge the AI builds up over time

---

### 7. Write the spec

Create `memory/in-progress/<name>/spec.md` with the spec template and show it to the user for confirmation.

---

### 8. Confirm and hand off

Say: "Spec saved to `memory/in-progress/<name>/spec.md`. Run `/promptsystem:build <name>` to generate all the files."
