---
description: Prepare an agent system for registry submission — runs the final checklist, generates a PR description, and walks through the fork-and-PR workflow
---

Prepare an agent system for submission to the agentically community registry at https://github.com/ai-superpowers/agentically.

I'll run the final pre-submission checklist, generate a ready-to-paste PR description, and walk you through the fork → branch → PR workflow.

---

**Input**: Optionally provide the agent system name (e.g., `/agentsystem:submit my-agent`). If omitted, I'll look for a recently tested agent system.

---

## Steps

### 1. Verify test status

Check `memory/in-progress/<name>/test-results.md`.

- If the file exists and verdict is **"Ready to submit"**: proceed.
- If the file exists but verdict is **"Needs fixes"**: say:
  > "The last test run found unresolved issues. Run `/agentsystem:test <name>` first, fix any failures, then re-run this command."
  Stop here.
- If the file does not exist: say:
  > "No test results found. Run `/agentsystem:test <name>` before submitting."
  Stop here.

---

### 2. Final pre-submission checklist

Read every file in `agents/<name>/` and check the following. Mark each ✅ PASS or ❌ FAIL:

**Content safety:**
- [ ] No API keys, tokens, passwords, or secrets anywhere
- [ ] No absolute paths hardcoded to the author's machine
- [ ] No references to internal/private systems or company-specific tooling (without disclosure)

**README quality:**
- [ ] H1 title is the agent system name (kebab-case, readable)
- [ ] "What It Does" section is at least 2 sentences and actually explains the value
- [ ] Usage section has the `agentically create <name>` command
- [ ] At least 2 platform examples (`--platform cursor`, etc.)
- [ ] Prompts reference table is present and accurate

**Prompt files:**
- [ ] Every `.md` in `prompts/` has a `description` in its YAML frontmatter
- [ ] No placeholder text (`TODO`, `FIXME`, `<insert here>`, etc.)
- [ ] Steps use consistent style (all numbered, no mixing bullets and numbers at the same level)

**Skill files (if any):**
- [ ] Every `SKILL.md` has `name`, `description`, and `license` in frontmatter
- [ ] `license` is a valid SPDX identifier (e.g., `MIT`, `Apache-2.0`)
- [ ] No placeholder text in any skill body

**Naming:**
- [ ] Agent system folder name is kebab-case and unique (check: doesn't duplicate an existing entry in `agents/`)
- [ ] Prompt filenames match the pattern `<prefix>-<command>.md`
- [ ] All prompts share the same `<prefix>` (consistent namespace)

If any check fails, list all failures and ask the user to fix them before continuing.

---

### 3. Gather PR metadata

Ask (use AskUserQuestion if available):

1. **Your GitHub username**: "What is your GitHub username? This will appear in the commit and PR."
2. **Brief description**: "In 1–2 sentences, what does this agent system do for the person who installs it?" (used in PR body)
3. **Tested platforms**: "Which platforms did you test the install on?" (cursor / copilot / claude / kiro / none formally)

---

### 4. Generate the PR description

Produce a ready-to-paste PR description. Read the README and spec to fill in the tables:

```markdown
## New Agent System: `<name>`

### What it does
<2–3 sentences from the README "What It Does" section>

### Prompts

| File        | Claude command | Description                    |
| ----------- | -------------- | ------------------------------ |
| `<file.md>` | `/prefix:cmd`  | <description from frontmatter> |

### Skills

| Skill          | Description                             |
| -------------- | --------------------------------------- |
| `<skill-name>` | <description from SKILL.md frontmatter> |

### Tested on
- [x/space] cursor
- [x/space] copilot
- [x/space] claude
- [x/space] kiro

### Checklist
- [x] README explains purpose and usage
- [x] All prompts have `description` frontmatter
- [x] All skills have required frontmatter (`name`, `description`, `license`)
- [x] No secrets or hardcoded paths
- [x] Agent system name is unique in the registry
```

Show this to the user and say: "Copy this for your PR description."

---

### 5. Walk through the fork-and-PR workflow

Guide the user step by step:

**a. Fork the registry (if not already done)**

> Go to https://github.com/ai-superpowers/agentically and click "Fork" to create your own copy.

**b. Clone your fork**

```bash
git clone https://github.com/<your-username>/agentically.git
cd agentically
```

**c. Create a branch**

```bash
git checkout -b add-<name>
```

**d. Copy your agent system into the fork**

```bash
# Run this from your project root (where agents/<name>/ lives)
cp -r agents/<name> <path-to-cloned-fork>/agents/<name>
```

**e. Review what you're committing**

```bash
cd <path-to-cloned-fork>
git status
git diff --stat
```

Check the output — make sure only your new agent system files appear. Nothing else should be modified.

**f. Commit and push**

```bash
git add agents/<name>
git commit -m "feat: add <name> agent system"
git push origin add-<name>
```

**g. Open the pull request**

> Go to your fork on GitHub. You'll see a "Compare & pull request" banner. Click it.
> Paste the PR description generated in Step 4.
> Submit the PR to the `main` branch of `ai-superpowers/agentically`.

---

### 6. After submission

Tell the user:

> "Your PR is open! Here's what happens next:
>
> - Maintainers will review your agent system (usually within a few days).
> - If changes are requested, update the files in your fork branch and push again — the PR will update automatically.
> - Once merged, anyone can install your agent system with:
>   ```bash
>   agentically create <name>
>   ```
>
> Nice work!"

Optionally save a note to `memory/in-progress/<name>/test-results.md` appending the submission date and PR URL (if the user provides it).
