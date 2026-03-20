# Installation

## Prerequisites

- **Python 3.9 or later** — agentically requires Python ≥ 3.9.
- **pip** — included with Python 3.4+.
- An internet connection — the CLI fetches agent systems from GitHub.

## Install

```bash
pip install agentically
```

To install in an isolated environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install agentically
```

## Verify

```bash
agentically --version
# → agentically 0.3.0
```

## Dependencies

agentically installs the following packages automatically:

| Package           | Purpose                               |
| ----------------- | ------------------------------------- |
| `typer ≥ 0.12`    | CLI framework                         |
| `requests ≥ 2.31` | HTTP calls to the GitHub registry API |
| `rich ≥ 13`       | Terminal output formatting            |

## Next steps

See [Quick Start](quickstart.md) to browse the registry and install your first agent system.
