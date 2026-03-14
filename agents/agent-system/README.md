# agent-system

An agent system for building agent systems. Provides prompts and skills to help you design, build, test, and submit a new agent system to the `agentically` registry.

## What It Does

This agent system guides you through the full lifecycle of creating a new agentically agent system:

1. **Design** — Interview yourself (or let the AI interview you) to turn a workflow idea into a concrete spec: what prompts, skills, and memory structure to create.
2. **Build** — Generate all the files (prompts, skill definitions, memory layout, README) from the spec.
3. **Test** — Validate structure, frontmatter conventions, prompt quality, and simulate platform installs before you ship.
4. **Submit** — Run the final checklist and get a ready-to-paste PR description for the community registry.

## Structure

```
agent-system/
  README.md                        ← this file
  prompts/
    agentsystem-design.md          ← design & spec a new agent system
    agentsystem-build.md           ← build files from a spec
    agentsystem-test.md            ← validate & test before submission
    agentsystem-submit.md          ← prepare and guide the registry PR
  skills/
    design/
      SKILL.md                     ← agent system design knowledge
    build/
      SKILL.md                     ← agent system build knowledge
    test/
      SKILL.md                     ← agent system test knowledge
    submit/
      SKILL.md                     ← agent system submit knowledge
  memory/
    config.yaml                    ← agentically registry context
    in-progress/                   ← specs & test results for systems under construction
```

## Usage

```bash
agentically create agent-system
```

Or with a specific platform:

```bash
agentically create agent-system --platform cursor
agentically create agent-system --platform copilot
agentically create agent-system --platform claude
agentically create agent-system --platform kiro
```

## Prompts Reference

| File                    | Claude command        | Description                                          |
| ----------------------- | --------------------- | ---------------------------------------------------- |
| `agentsystem-design.md` | `/agentsystem:design` | Interview-driven design session → produces a spec    |
| `agentsystem-build.md`  | `/agentsystem:build`  | Builds all files from a spec                         |
| `agentsystem-test.md`   | `/agentsystem:test`   | Validates structure, quality, and install simulation |
| `agentsystem-submit.md` | `/agentsystem:submit` | Final checklist + registry PR guidance               |

## Typical Workflow

```
/agentsystem:design my-cool-agent    ← creates memory/in-progress/my-cool-agent/spec.md
/agentsystem:build my-cool-agent     ← creates agents/my-cool-agent/ from spec
/agentsystem:test my-cool-agent      ← validates and saves test-results.md
/agentsystem:submit my-cool-agent    ← prepares PR for https://github.com/ai-superpowers/agentically
```

## Contributing

Made an improvement? Open a PR to update this agent system, or add your own under `agents/your-name/`.
