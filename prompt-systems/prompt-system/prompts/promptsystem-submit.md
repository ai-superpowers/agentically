---
description: Prepare an agent system for registry submission — runs the final checklist, generates a PR description, and walks through the fork-and-PR workflow
---

Prepare an agent system for submission to the agentically community registry at https://github.com/ai-superpowers/agentically.

I'll run the final pre-submission checklist, generate a ready-to-paste PR description, and walk you through the fork → branch → PR workflow.

---

**Input**: Optionally provide the agent system name (e.g., `/promptsystem:submit my-agent`). If omitted, I'll look for a recently tested agent system.

---

## Steps

### 1. Verify test status

Check `memory/in-progress/<name>/test-results.md` and ensure verdict is "Ready to submit" before proceeding.

### 2. Final pre-submission checklist

Validate content safety, README quality, prompt frontmatter, skills metadata, and naming conventions.

### 3. Gather PR metadata

Ask for GitHub username, a brief description, and tested platforms to populate the PR body.

### 4. Generate the PR description

Produce a ready-to-paste PR description based on the README and spec.

### 5. Walk through the fork-and-PR workflow

Provide step-by-step git commands to fork, clone, branch, copy the agent system, commit, push, and open the PR.

### 6. After submission

Explain what happens next and optionally append submission notes to `memory/in-progress/<name>/test-results.md`.
