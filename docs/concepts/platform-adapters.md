# Platform Adapters

When you install an agent system with `--platform <name>`, agentically uses a **platform adapter** to route each downloaded file to the correct location on disk for that coding tool. This lets multiple agent systems coexist in the same project without overwriting each other.

## How file routing works

Every adapter subclasses `PlatformAdapter` and defines three properties:

| Property         | Example (Copilot) | Effect                                           |
| ---------------- | ----------------- | ------------------------------------------------ |
| `platform_dir`   | `.github`         | Root directory all files land under              |
| `prompts_subdir` | `prompts`         | Subdirectory for prompt files                    |
| `skills_subdir`  | `skills`          | Subdirectory for skill files (default: `skills`) |

Given an agent-relative path, the `dest_for` method applies these routing rules in order:

```
prompts/<stem>.md  →  <platform_dir>/<prompts_subdir>/<dest-stem>
skills/<rest>      →  <platform_dir>/skills/<rest>
memory/<rest>      →  <platform_dir>/memory/<rest>
README.md          →  <platform_dir>/<agent-name>-README.md
<anything else>    →  <platform_dir>/<original path>
```

The prompt filename may be transformed by `prompt_dest`. For example, Copilot appends `.prompt.md` to the stem, while Claude splits on the first `-` to create a subdirectory.

## Supported platforms

| Platform  | `platform_dir` | `prompts_subdir` | Prompt filename convention                  |
| --------- | -------------- | ---------------- | ------------------------------------------- |
| `copilot` | `.github`      | `prompts`        | `<stem>.prompt.md`                          |
| `claude`  | `.claude`      | `commands`       | `<prefix>/<suffix>.md` (split on first `-`) |
| `cursor`  | `.cursor`      | `commands`       | `<stem>.md`                                 |
| `kiro`    | `.kiro`        | `prompts`        | `<stem>.prompt.md`                          |

## Auto-detection

If you omit `--platform`, agentically runs `detect_platform` against your current working directory:

1. `.cursor/` directory present → `cursor`
2. `.github/copilot-instructions.md` or `.github/prompts/` present → `copilot`
3. `CLAUDE.md` or `.claude/` present → `claude`
4. `.kiro/` present → `kiro`
5. None of the above → prompts for a choice

## Adding a new platform

1. Create `agentically/adapters/<platform>.py` with a `PlatformAdapter` subclass:

```python
from agentically.adapters.base import PlatformAdapter

class MyPlatformAdapter(PlatformAdapter):
    name = "myplatform"
    platform_dir = ".myplatform"
    prompts_subdir = "prompts"

_adapter = MyPlatformAdapter()
```

2. Import `_adapter` in `agentically/adapters/__init__.py` and add it to `_ADAPTERS`.
3. Add `"myplatform"` to `SUPPORTED_PLATFORMS`.
4. Update `detect_platform` with a filesystem signal for the new platform.

See [Adapters API Reference](../api/adapters.md) for the full `PlatformAdapter` interface.
