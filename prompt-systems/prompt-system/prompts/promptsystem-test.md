---
description: Validate an agent system before submission — checks file structure, frontmatter conventions, prompt quality, and simulates platform installs
---

Test and validate an agent system against the agentically registry standards.

I'll run a structured checklist covering structure, frontmatter, prompt quality, skill quality, and platform install simulation — then save results to `memory/in-progress/<name>/test-results.md`.

---

**Input**: Optionally provide the agent system name (e.g., `/promptsystem:test my-agent`). If omitted, I'll detect from `prompt-systems/` or ask.

---

## Steps

### 1. Locate the agent system

If name provided, verify `prompt-systems/<name>/` exists.

If no name:
- List directories in `prompt-systems/`
- Exclude well-known non-agent directories (`README.md`, etc.)
- If one candidate, use it and announce
- If multiple, ask the user which one to test
- If none, say: "No agent systems found in `prompt-systems/`. Run `/promptsystem:build` first."

---

### 2. Structure check

Use the TodoWrite tool to track each check. Verify required files and prompt/skill/memory conventions, then report exact failures with suggestions.

---

### 3. Prompt quality review

For each prompt file, evaluate clarity of inputs, concreteness of steps, handling of missing inputs, and next-step guidance.

---

### 4. Skill quality review

For each `SKILL.md`, validate frontmatter and whether the description is specific enough for auto-invocation.

---

### 5. Install simulation

Map `prompts/` and `skills/` to each platform's install destinations and flag collisions or naming issues.

---

### 6. Optional: live install test

Offer to run `agentically create <name>` in a temp dir if the CLI is available.

---

### 7. Save test results

Create `memory/in-progress/<name>/test-results.md` with a structured report and verdict.

---

### 8. Report and next steps

If all checks pass: "All checks passed! Run `/promptsystem:submit <name>` to prepare your registry PR." Otherwise provide issues and guidance to fix them.
