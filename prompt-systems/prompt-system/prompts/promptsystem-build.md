---
description: Build all agent system files from a spec — creates prompt files, skill definitions, memory structure, and README in prompt-systems/<name>/
---

Build a complete agent system from a design spec.

I'll read the spec from `memory/in-progress/<name>/spec.md` and generate every file needed for a valid agentically registry entry.

---

**Input**: Optionally provide the agent system name (e.g., `/promptsystem:build my-agent`). If omitted, I'll list available specs in `memory/in-progress/` and ask you to pick one.

---

## Steps

### 1. Load the spec

If a name is provided, read `memory/in-progress/<name>/spec.md`.

If no name provided:
- List the directories in `memory/in-progress/`
- If exactly one exists, use it and announce: "Using spec for `<name>`."
- If multiple exist, ask the user to choose
- If none exist, say: "No specs found. Run `/promptsystem:design` first to create one."

Parse the spec to extract:
- Agent system name
- Purpose and target user
- Prompts list (filename, description, inputs, steps)
- Skills list (folder name, description, trigger)
- Memory structure

---

### 2. Create the directory scaffold

Use the TodoWrite tool to track progress.

Create this structure (announce each directory as you set it up):

```
prompt-systems/<name>/
  prompts/
  skills/
  memory/
  README.md
```

---

### 3. Build each prompt file

For each prompt in the spec, create `prompt-systems/<name>/prompts/<filename>.md`.

**Every prompt file must include:**

```markdown
---
description: <one-line description — what it does and when to invoke it>
---

<Short intro paragraph: what this command does>

**Input**: <What argument or context does the user provide? What happens if missing?>

---

## Steps

### 1. <Step title>
<Concrete instructions. Include specific tools (AskUserQuestion, TodoWrite, file reads, CLI commands).>

### 2. <Step title>
...
```

**Quality bar for each prompt:**
- Steps must be specific and executable — no vague instructions like "do the analysis"
- Include decision branches: "If X, then Y; otherwise Z"
- Specify file paths explicitly (use the agentically layout: `prompt-systems/<name>/prompts/`, etc.)
- Name CLI commands exactly as the user would type them
- End with a clear "next step" that chains to the next prompt in the workflow, e.g.:
  > "Run `/promptsystem:test <name>` to validate the files you just created."

Write out each prompt file fully — don't leave placeholder text.

---

### 4. Build each skill file

For each skill in the spec, create `prompt-systems/<name>/skills/<skill-name>/SKILL.md`.

**Every SKILL.md must include this exact frontmatter:**

```yaml
---
name: <agent-name>-<skill-name>
description: <one-line description — specific enough that the AI knows when to auto-invoke it>
license: MIT
compatibility: <e.g., "No external dependencies." or "Requires X CLI on PATH.">
metadata:
  author: community
  version: "1.0"
---
```

---

### 5. Build the memory structure

For each memory path from the spec:
- Create directories
- For empty directories that need to exist, add a `.gitkeep` or a brief `README.md`
- Create `memory/config.yaml` with an appropriate `context` block

---

### 6. Build the README

Create `prompt-systems/<name>/README.md` using the standard template. End with:

> "All files written to `prompt-systems/<name>/`. Run `/promptsystem:test <name>` to validate the structure and quality before submitting."

---

### 7. Final summary

List every file created in a clean tree view and check off each item from the spec.
