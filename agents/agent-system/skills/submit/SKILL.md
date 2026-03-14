---
name: agentsystem-submit
description: Prepare an agent system for submission to the agentically registry. Use when running the final pre-submission checklist, generating a PR description, or guiding the fork-and-PR workflow for https://github.com/ai-superpowers/agentically.
license: MIT
compatibility: No external dependencies. Requires a GitHub account for PR submission.
metadata:
  author: community
  version: "1.0"
---

Submit agent systems to the agentically community registry.

## When to use this skill

Invoke when the user:
- Has finished building and testing an agent system and wants to submit it
- Needs a PR description generated for their agent system
- Wants guidance on the fork → branch → PR workflow
- Is running the final safety checklist before submission
- Asks "how do I publish my agent system?"

## Registry details

- **Registry URL**: https://github.com/ai-superpowers/agentically
- **Agent systems live in**: `agents/<name>/` at the root of the repo
- **Install command after merge**: `agentically create <name>`
- **PR target branch**: `main`

## Pre-submission checklist

All of these must pass before submitting:

**Safety:**
- [ ] No API keys, tokens, passwords, or secrets anywhere in the agent system
- [ ] No absolute paths hardcoded to the author's machine
- [ ] No references to private/internal systems (unless disclosed in README)
- [ ] Memory directory is safe to copy into any project

**README quality:**
- [ ] H1 title matches the agent system folder name (kebab-case)
- [ ] "What It Does" section clearly explains the value proposition
- [ ] Usage section includes `agentically create <name>`
- [ ] At least two `--platform` examples
- [ ] Prompts reference table is accurate and up-to-date

**Prompt files:**
- [ ] Every `.md` in `prompts/` has valid YAML frontmatter with a `description` field
- [ ] No placeholder text (`TODO`, `FIXME`, `<insert here>`) anywhere
- [ ] All prompts have a consistent `<prefix>-` naming pattern

**Skill files:**
- [ ] Every `SKILL.md` has `name`, `description`, and `license` in frontmatter
- [ ] `license` is a valid SPDX identifier

**Uniqueness:**
- [ ] Agent system name is unique — not a duplicate of an existing entry in `agents/`

## PR description template

Generate and provide this template filled in from the agent system files:

```markdown
## New Agent System: `<name>`

### What it does
<2–3 sentences from README>

### Prompts
| File | Claude command | Description |
|------|---------------|-------------|
| `<file.md>` | `/prefix:cmd` | <frontmatter description> |

### Skills
| Skill | Description |
|-------|-------------|
| `<skill-name>` | <SKILL.md frontmatter description> |

### Tested on
- [ ] cursor
- [ ] copilot
- [ ] claude
- [ ] kiro

### Checklist
- [x] README explains purpose and usage
- [x] All prompts have `description` frontmatter
- [x] All skills have required frontmatter
- [x] No secrets or hardcoded absolute paths
- [x] Agent system name is unique in the registry
```

## Fork-and-PR workflow

Guide the user through these steps in order:

**1. Fork the registry**
> Go to https://github.com/ai-superpowers/agentically and click "Fork"

**2. Clone the fork**
```bash
git clone https://github.com/<username>/agentically.git
cd agentically
```

**3. Create a feature branch**
```bash
git checkout -b add-<name>
```

**4. Copy the agent system**
```bash
# Run from your project root
cp -r agents/<name> <path-to-fork>/agents/<name>
```

**5. Verify contents before committing**
```bash
cd <path-to-fork>
git status
git diff --stat
```
Only files under `agents/<name>/` should appear as new.

**6. Commit and push**
```bash
git add agents/<name>
git commit -m "feat: add <name> agent system"
git push origin add-<name>
```

**7. Open the PR**
> Go to your fork on GitHub → click "Compare & pull request" → paste the PR description → submit to `main`.

## After submission

- Maintainers review within a few days
- Iterate freely by pushing more commits to your branch — the PR updates automatically
- Once merged, `agentically create <name>` works for everyone immediately
