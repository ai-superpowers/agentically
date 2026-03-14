---
description: Validate an agent system before submission — checks file structure, frontmatter conventions, prompt quality, and simulates platform installs
---

Test and validate an agent system against the agentically registry standards.

I'll run a structured checklist covering structure, frontmatter, prompt quality, skill quality, and platform install simulation — then save results to `memory/in-progress/<name>/test-results.md`.

---

**Input**: Optionally provide the agent system name (e.g., `/agentsystem:test my-agent`). If omitted, I'll detect from `agents/` or ask.

---

## Steps

### 1. Locate the agent system

If name provided, verify `agents/<name>/` exists.

If no name:
- List directories in `agents/`
- Exclude well-known non-agent directories (`README.md`, etc.)
- If one candidate, use it and announce
- If multiple, ask the user which one to test
- If none, say: "No agent systems found in `agents/`. Run `/agentsystem:build` first."

---

### 2. Structure check

Use the TodoWrite tool to track each check.

Verify the following — mark each ✅ PASS or ❌ FAIL with a specific reason:

**Required files:**
- [ ] `agents/<name>/README.md` exists
- [ ] README has an H1 title matching (or close to) the agent system name
- [ ] README has a "What It Does" or equivalent summary section
- [ ] README has a "Usage" section with `agentically create <name>` example
- [ ] `agents/<name>/prompts/` directory exists and contains at least one `.md` file

**Prompt files:**
- [ ] Each `.md` in `prompts/` has YAML frontmatter
- [ ] Each frontmatter block has a non-empty `description` field
- [ ] Prompt filenames are kebab-case (no spaces, no uppercase)
- [ ] Prompt filenames follow `<prefix>-<command>.md` pattern (namespace-command)
- [ ] All prompts in the same agent system share the same `<prefix>`

**Skill files (if `skills/` exists):**
- [ ] Each subdirectory of `skills/` contains a `SKILL.md` file
- [ ] Each `SKILL.md` has frontmatter with `name`, `description`, and `license` fields
- [ ] `description` in each SKILL.md is specific enough to trigger auto-invocation

**Memory (if `memory/` exists):**
- [ ] `config.yaml` exists (if memory dir has files)
- [ ] No secrets, API keys, or credentials anywhere in `memory/`

Report all failures with exact file paths and suggested fixes.

---

### 3. Prompt quality review

For each prompt file in `agents/<name>/prompts/`:

Read the full file content, then evaluate:

| Quality criterion                                                         | Check |
| ------------------------------------------------------------------------- | ----- |
| Clear input description (what argument/context + what if missing)         | ✅/❌   |
| Steps are numbered and concrete (no vague "do the analysis" instructions) | ✅/❌   |
| Missing-input case is handled (prompts user or fails gracefully)          | ✅/❌   |
| Specific tools mentioned where useful (AskUserQuestion, TodoWrite, etc.)  | ✅/❌   |
| Ends with a clear next-step suggestion or completion message              | ✅/❌   |
| No hardcoded absolute file paths that would break outside the workspace   | ✅/❌   |

Note any issues with specific line references where possible.

---

### 4. Skill quality review

For each `SKILL.md` in `agents/<name>/skills/`:

Evaluate:
| Quality criterion                                                     | Check |
| --------------------------------------------------------------------- | ----- |
| `description` is specific enough for AI to know when to auto-invoke   | ✅/❌   |
| Body explains the "when to use" with explicit triggers                | ✅/❌   |
| Content is self-contained (readable without context from other files) | ✅/❌   |
| `compatibility` field is accurate (lists real external dependencies)  | ✅/❌   |

---

### 5. Install simulation

Compute what `agentically create <name> --platform <p>` would install for each platform.

Apply these mapping rules to every file in `prompts/` and `skills/`:

**Prompt file `<stem>.md`:**
| Platform | Installs to                                                          |
| -------- | -------------------------------------------------------------------- |
| cursor   | `.cursor/commands/<stem>.md`                                         |
| copilot  | `.github/prompts/<stem>.prompt.md`                                   |
| claude   | `.claude/commands/<prefix>/<suffix>.md` (split on first `-` in stem) |
| kiro     | `.kiro/prompts/<stem>.prompt.md`                                     |

**Skill `skills/<skill-name>/SKILL.md`:**
| Platform | Installs to                            |
| -------- | -------------------------------------- |
| cursor   | `.cursor/skills/<skill-name>/SKILL.md` |
| copilot  | `.github/skills/<skill-name>/SKILL.md` |
| claude   | `.claude/skills/<skill-name>/SKILL.md` |
| kiro     | `.kiro/skills/<skill-name>/SKILL.md`   |

Display the full install map as a table. Flag any issues:
- Two prompts that would overwrite the same destination path
- A stem that produces a weird or misleading Claude command name
- Skill names that collide with common system skills

---

### 6. Optional: live install test

If the `agentically` CLI is available (check with `agentically --version`), offer to run a real install test:

```bash
# Creates a temp dir, installs, and shows output
mkdir -p /tmp/agentically-test && cd /tmp/agentically-test && agentically create <name>
```

Capture any errors and include them in the results.

---

### 7. Save test results

Create `memory/in-progress/<name>/test-results.md`:

```markdown
# Test Results: <name>

**Date**: <today's date>
**Overall**: PASS / FAIL / PASS WITH WARNINGS

---

## Structure Check: PASS / FAIL
| Item                     | Result | Notes |
| ------------------------ | ------ | ----- |
| README.md exists         | ✅/❌    |       |
| README has summary       | ✅/❌    |       |
| README has usage         | ✅/❌    |       |
| Prompt files exist       | ✅/❌    |       |
| Prompt frontmatter valid | ✅/❌    |       |
| Skill files valid        | ✅/❌    |       |

## Prompt Quality: PASS / FAIL
| File          | Result | Issues                      |
| ------------- | ------ | --------------------------- |
| <filename.md> | ✅/❌    | <description of any issues> |

## Skill Quality: PASS / FAIL
| Skill        | Result | Issues                      |
| ------------ | ------ | --------------------------- |
| <skill-name> | ✅/❌    | <description of any issues> |

## Install Simulation
| Platform | Prompt destinations | Skill destinations |
| -------- | ------------------- | ------------------ |
| cursor   |                     |                    |
| copilot  |                     |                    |
| claude   |                     |                    |
| kiro     |                     |                    |

## Issues to Fix
1. <specific issue with file path and fix suggestion>
2. ...

## Verdict
- [ ] Ready to submit
- [ ] Needs fixes (see issues above)
```

---

### 8. Report and next steps

Show the test summary in the chat.

- If all checks pass:
  > "All checks passed! Run `/agentsystem:submit <name>` to prepare your registry PR."

- If there are failures:
  > "Found <N> issues to fix. See `memory/in-progress/<name>/test-results.md` for details. Fix them and re-run `/agentsystem:test <name>`."

- If only warnings:
  > "Passed with <N> warnings. These won't block submission but are worth addressing."
