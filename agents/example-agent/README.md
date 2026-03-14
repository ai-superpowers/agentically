# example-agent

A simple example agent system demonstrating the `agentically` registry format.

## What It Does

This agent system provides a set of AI prompts and skills for building and proposing
apps, demonstrating the canonical structured layout for the `agentically` registry.

## Structure

```
example-agent/
  README.md          ← this file
  prompts/           ← prompt/command files for AI coding tools
    build-app.md
    propose-app.md
  skills/            ← agent skill definitions
    build/
      SKILL.md
    propose/
      SKILL.md
  memory/            ← agent-internal working state (copied as-is)
    config.yaml
    changes/
    specs/
```

## Usage

```bash
agentically use example-agent
```

Or with a specific platform:

```bash
agentically use example-agent --platform cursor
agentically use example-agent --platform copilot
agentically use example-agent --platform claude
agentically use example-agent --platform kiro
```

The CLI will prompt you to choose a platform if `--platform` is omitted.

## Contributing

Made a better version? Open a PR to update this agent system, or add your own under `agents/your-name/`.
