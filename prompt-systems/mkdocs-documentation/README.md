# mkdocs-documentation

Generate thorough, structured MkDocs Material documentation from any codebase in two steps: analyze then build.

## What It Does

`mkdocs-documentation` is an AI agent system that automates the end-to-end creation of MkDocs Material documentation for your project. It works in two phases:

1. **Analyze** — Scans your source files to extract domain terms, acronyms, module structure, CLI commands, and docstrings. Produces a documentation plan (hierarchy, glossary, task list) in `memory/analysis/` for your review before a single doc page is written.

2. **Build** — Reads the approved plan and generates `mkdocs.yml` plus every documentation page: API reference, getting started, concept guides, glossary, and acronym reference. Pages that cannot be fully inferred are marked `[TODO]` for easy follow-up.

## Install

```bash
agentically create mkdocs-documentation
```

With a specific platform:

```bash
agentically create mkdocs-documentation --platform cursor
agentically create mkdocs-documentation --platform copilot
agentically create mkdocs-documentation --platform claude
agentically create mkdocs-documentation --platform kiro
```

## Prerequisites

For the built documentation to render, install MkDocs Material in the target project:

```bash
pip install mkdocs-material
# For Python API reference via mkdocstrings:
pip install mkdocs-material "mkdocstrings[python]"
```

## Usage

### Step 1 — Analyze your codebase

```
/mkdocs-documentation:analyze
```

Optional arguments:
- Path to codebase root: `/mkdocs-documentation:analyze path/to/src`
- Project name override: `/mkdocs-documentation:analyze --name "My Project"`

Review the output in `memory/analysis/`:
- `glossary.md` — domain terms; fill in any `[TODO]` definitions
- `acronyms.md` — acronyms; fill in any `[TODO]` expansions
- `hierarchy.md` — nav structure; reorder or rename sections as needed
- `tasks.md` — task list; adjust priorities if needed

### Step 2 — Build the documentation

```
/mkdocs-documentation:build
```

Optional arguments:
- Output directory: `/mkdocs-documentation:build path/to/docs`
- Force overwrite: `/mkdocs-documentation:build --force`

This generates `mkdocs.yml` and all pages under `docs/`. Pages marked `[TODO]` need manual content.

### Preview

```bash
mkdocs serve       # live preview at http://127.0.0.1:8000/
mkdocs build       # build static site to site/
```

## Prompts Reference

| File | Command | Description |
|------|---------|-------------|
| `mkdocs-documentation-analyze.md` | `/mkdocs-documentation:analyze` | Scan codebase → write documentation plan to `memory/analysis/` |
| `mkdocs-documentation-build.md` | `/mkdocs-documentation:build` | Read plan → generate `mkdocs.yml` and all `docs/` pages |

## Skills Reference

| Skill | Auto-applies when... |
|-------|----------------------|
| `analyze-codebase` | Scanning source files, extracting terms, mapping hierarchy |
| `mkdocs-material` | Writing `mkdocs.yml` or any MkDocs documentation page |

## Memory Structure

```
memory/
  config.yaml          ← project root, name, output dir, style settings
  analysis/
    glossary.md        ← domain terms (written by analyze, read by build)
    acronyms.md        ← acronyms (written by analyze, read by build)
    hierarchy.md       ← nav outline (written by analyze, read by build)
    tasks.md           ← task checklist (written by analyze, updated by build)
```

Edit `memory/config.yaml` to set your project root, output directory, and theme preferences before running.

## Typical Workflow

```
/mkdocs-documentation:analyze       ← Phase 1: scan repo, create plan
  (review memory/analysis/, fix TODOs)
/mkdocs-documentation:build         ← Phase 2: generate all docs
  mkdocs serve                       ← preview the result
```

All files written to `prompt-systems/mkdocs-documentation/`. Run `/promptsystem:test mkdocs-documentation` to validate the structure and quality before submitting.
