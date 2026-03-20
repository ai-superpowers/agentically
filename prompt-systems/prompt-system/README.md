# prompt-system

A prompt system for building agent systems. Provides prompts and skills to help you design, build, test, and submit a new agent system to the `agentically` registry.

## What It Does

This prompt system guides you through the full lifecycle of creating a new agentically agent system:

1. **Design** — Interview yourself (or let the AI interview you) to turn a workflow idea into a concrete spec: what prompts, skills, and memory structure to create.
2. **Build** — Generate all the files (prompts, skill definitions, memory layout, README) from the spec.
3. **Test** — Validate structure, frontmatter conventions, prompt quality, and simulate platform installs before you ship.
4. **Submit** — Run the final checklist and get a ready-to-paste PR description for the community registry.

## Structure

```
prompt-system/
  README.md                        ← this file
  prompts/
    promptsystem-design.md         ← design & spec a new agent system
    promptsystem-build.md          ← build files from a spec
    promptsystem-test.md           ← validate & test before submission
    promptsystem-submit.md         ← prepare and guide the registry PR
  skills/
    design/
      SKILL.md                     ← design knowledge for agent systems
    build/
      SKILL.md                     ← build knowledge for agent systems
    test/
      SKILL.md                     ← test knowledge for agent systems
    submit/
      SKILL.md                     ← submit knowledge for agent systems
  memory/
    config.yaml                    ← agentically registry context
    in-progress/                   ← specs & test results for systems under construction
```

## Usage

```bash
agentically create prompt-system
```

Or with a specific platform:

```bash
agentically create prompt-system --platform cursor
agentically create prompt-system --platform copilot
agentically create prompt-system --platform claude
agentically create prompt-system --platform kiro
```

## Prompts Reference

| File                     | Claude command         | Description                                          |
| ------------------------ | ---------------------- | ---------------------------------------------------- |
| `promptsystem-design.md` | `/promptsystem:design` | Interview-driven design session → produces a spec    |
| `promptsystem-build.md`  | `/promptsystem:build`  | Builds all files from a spec                         |
| `promptsystem-test.md`   | `/promptsystem:test`   | Validates structure, quality, and install simulation |
| `promptsystem-submit.md` | `/promptsystem:submit` | Final checklist + registry PR guidance               |

## Typical Workflow

```
/promptsystem:design my-cool-agent    ← creates memory/in-progress/my-cool-agent/spec.md
/promptsystem:build my-cool-agent     ← creates prompt-systems/my-cool-agent/ from spec
/promptsystem:test my-cool-agent      ← validates and saves test-results.md
/promptsystem:submit my-cool-agent    ← prepares PR for https://github.com/ai-superpowers/agentically
```

## Contributing

Made an improvement? Open a PR to update this prompt system, or add your own under `prompt-systems/your-name/`.
