---
name: agentsystem-test
description: Validate an agentically agent system. Use when checking file structure, frontmatter correctness, prompt quality, skill quality, or simulating platform installs for an agent system under agents/<name>/.
license: MIT
compatibility: No external dependencies. Optional: agentically CLI for live install testing.
metadata:
  author: community
  version: "1.0"
---

Validate agent systems against agentically registry standards.

## When to use this skill

Invoke when the user:
- Wants to check if their agent system is ready to submit
- Is debugging why a prompt or skill isn't working as expected
- Needs to verify frontmatter is correct
- Wants to know what file paths will be installed on a specific platform
- Is reviewing someone else's agent system for quality

## Validation checklist

Run through each category. Mark PASS / FAIL / WARNING.

### Structure checks

| Check | Requirement |
|-------|-------------|
| `README.md` exists | Required |
| README has H1 title | Must match (or approximate) the agent system name |
| README has summary section | "What It Does" or equivalent, ≥2 sentences |
| README has usage section | Must include `agentically create <name>` |
| `prompts/` exists | Required (at least one .md file) |
| All prompts have frontmatter | YAML block at top of file |
| `description` in each prompt | Non-empty string |
| Kebab-case filenames | No spaces, no uppercase |
| Consistent prefix | All prompt filenames share same `<prefix>-` |
| Skill dirs have SKILL.md | Each subdirectory of `skills/` must have one |
| SKILL.md has `name` | Non-empty |
| SKILL.md has `description` | Non-empty and specific |
| SKILL.md has `license` | Valid SPDX identifier (MIT, Apache-2.0, etc.) |
| No secrets in memory | No API keys, tokens, passwords |

### Prompt quality criteria

For each prompt file:
1. **Input handling** — describes what argument the user provides AND what happens if it's absent
2. **Concrete steps** — steps are numbered, specific, actionable (no "do the thing")
3. **Decision branches** — ambiguous situations have explicit "if X then Y" handling
4. **Tool references** — mentions specific tools where useful (AskUserQuestion, TodoWrite, etc.)
5. **No placeholder text** — no `TODO`, `FIXME`, `<insert here>` remaining
6. **Next-step chain** — ends by suggesting the next command in the workflow
7. **Safe paths** — no absolute paths hardcoded to one machine

### Skill quality criteria

For each SKILL.md:
1. **Auto-invocation clarity** — description tells the AI precisely when to apply this skill
2. **Trigger section** — body has a "When to use" section with specific triggers
3. **Self-contained** — readable and useful without any other file for context
4. **Accurate compatibility** — `compatibility` field lists real external dependencies (or "No external dependencies.")

## Platform install simulation

Apply these rules to compute installed paths:

**Prompt file `<stem>.md`:**
| Platform | Destination |
|----------|-------------|
| cursor   | `.cursor/commands/<stem>.md` |
| copilot  | `.github/prompts/<stem>.prompt.md` |
| claude   | `.claude/commands/<text-before-first-dash>/<text-after-first-dash>.md` |
| kiro     | `.kiro/prompts/<stem>.prompt.md` |

**Claude example:**
- `review-start.md` → `.claude/commands/review/start.md` (slash command: `/review:start`)
- `myagent-run-check.md` → `.claude/commands/myagent/run-check.md` (slash command: `/myagent:run-check`)

**Skill `skills/<skill-name>/SKILL.md`:**
All platforms: `.<platform-dir>/skills/<skill-name>/SKILL.md`

**Flag these install issues:**
- Two prompt files that resolve to the same destination path on any platform
- A Claude command name that is generic or potentially conflicting (e.g., `/agent:run`)
- A skill name that shadows a common system skill name

## Test results format

Save results to `memory/in-progress/<name>/test-results.md`:

```markdown
# Test Results: <name>
Date: <YYYY-MM-DD>
Overall: PASS / FAIL / PASS WITH WARNINGS

## Structure: PASS/FAIL
| Item | Result | Notes |
...

## Prompt Quality: PASS/FAIL
| File | Result | Issues |
...

## Skill Quality: PASS/FAIL
| Skill | Result | Issues |
...

## Install Simulation
| Platform | Prompt paths | Skill paths |
...

## Issues to Fix
1. <file>: <specific issue and fix>
...

## Verdict
[ ] Ready to submit
[ ] Needs fixes: <list>
```
