---
description: Analyzes a repository codebase and produces a glossary, acronyms list, documentation hierarchy, and prioritized task list for MkDocs Material documentation. Invoke this first, before building docs.
---

Scan the codebase and produce a complete documentation plan. This command reads your source files, extracts domain terms and acronyms, derives a MkDocs Material nav hierarchy, and writes a prioritized task checklist — all to `memory/analysis/` for your review before any docs are written.

**Input**: Optionally provide a path to the codebase root (e.g., `/mkdocs-documentation:analyze src/`) and/or a project name override (e.g., `/mkdocs-documentation:analyze --name "My Project"`). If omitted, the project root and name are read from `memory/config.yaml`; if absent there, they are inferred from the workspace root and directory name.

---

## Steps

### 1. Load configuration

Read `memory/config.yaml`.

- If the file exists, extract `project_root`, `project_name`, `docs_output_dir`, and `style` settings.
- If the file is missing or a field is blank:
  - `project_root` → use the workspace root (`.`)
  - `project_name` → check `pyproject.toml` (`[project] name`), `package.json` (`"name"`), or the root directory name, in that order
  - `docs_output_dir` → default to `docs`
- If the user supplied a path argument, override `project_root` with that value.
- If the user supplied `--name`, override `project_name`.

Announce: "Analyzing `<project_name>` at `<project_root>`."

---

### 2. Scan source files

Recursively list all files under `project_root`, excluding common non-source directories: `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `dist`, `build`, `.tox`, `*.egg-info`.

For each source file, collect:

- **Python (`*.py`)**: module path, top-level class names, function/method signatures, docstrings (module, class, function), inline comments, and any `__all__` exports.
- **TypeScript/JavaScript (`*.ts`, `*.js`, `*.tsx`, `*.jsx`)**: exported class/function/interface names and JSDoc comments.
- **Config files (`*.yaml`, `*.toml`, `*.json`, `*.ini`, `*.cfg`)**: top-level keys and any inline comments.
- **Existing docs (`*.md`, `*.rst`)**: headings and any defined terms.
- **CLI entrypoints**: `console_scripts` in `pyproject.toml`/`setup.cfg`, `scripts` in `package.json`, or `if __name__ == "__main__"` blocks.

Build an in-memory index: `{file_path: {type, symbols: [], docstrings: [], cli_commands: []}}`.

---

### 3. Extract glossary terms

From the index, identify domain-specific terms:

- Class names, function names, and module names that appear in docstrings or comments as nouns describing concepts (not just implementors).
- Any term explicitly defined with patterns like `"X is a ..."`, `"X refers to ..."`, or `"X: ..."` in docstrings or comments.
- Config key names that represent user-facing concepts.

For each term, write a one-sentence definition by:
1. Using the docstring verbatim if it is a clean definition sentence.
2. Otherwise, synthesizing from usage context in comments.
3. If no context exists, write `"[TODO: define this term]"`.

Write `memory/analysis/glossary.md`:

```markdown
# Glossary

| Term   | Definition   |
| ------ | ------------ |
| <Term> | <Definition> |
```

Sort rows alphabetically by term.

---

### 4. Extract acronyms

From the index, identify acronyms:

- All-uppercase tokens of 2–6 characters appearing in source code identifiers, docstrings, or comments.
- CamelCase compound words where the expansion is hinted in nearby comments.
- Common software acronyms (e.g., `API`, `CLI`, `URL`, `HTTP`, `JSON`, `YAML`, `SDK`, `CSV`) — include these if they appear in the codebase.

For each acronym, write its expansion:
1. Use any inline hint (e.g., `# API: Application Programming Interface`) as the authoritative expansion.
2. For common acronyms, use the standard expansion.
3. For unknown acronyms, write `"[TODO: expand this acronym]"`.

Write `memory/analysis/acronyms.md`:

```markdown
# Acronyms

| Acronym   | Expansion   |
| --------- | ----------- |
| <ACRONYM> | <Expansion> |
```

Sort rows alphabetically by acronym.

---

### 5. Derive the documentation hierarchy

Group the scanned symbols into logical documentation sections. Apply these rules:

- **One section per logical concern**, not per file. Merge thin modules (fewer than 3 exported symbols) into a parent section.
- **Standard top-level sections** (include only those that apply):
  - `Home` → `index.md` (always include)
  - `Getting Started` → installation + quickstart
  - `Concepts` → architecture, data model, key abstractions
  - `Guides` → how-to pages derived from CLI commands or common workflows
  - `API Reference` → one page per public module; use mkdocstrings if Python
  - `Contributing` → if `CONTRIBUTING.md` or similar exists
  - `Changelog` → if `CHANGELOG.md` or `HISTORY.md` exists
  - `Reference` → glossary and acronyms pages (always include)

For each planned page, record:
- Relative path under `docs/` (e.g., `api/module-a.md`)
- Source type: `auto` (mkdocstrings), `hand-written` (prose), or `compiled` (assembled from analysis files)
- Which source files it covers

Write `memory/analysis/hierarchy.md`:

```markdown
# Documentation Hierarchy

## nav

- Home: index.md
- Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
- ...

## Page sources

| Page                            | Source type  | Covers                      |
| ------------------------------- | ------------ | --------------------------- |
| index.md                        | hand-written | README.md                   |
| getting-started/installation.md | hand-written | pyproject.toml, README.md   |
| api/<module>.md                 | auto         | src/<module>.py             |
| reference/glossary.md           | compiled     | memory/analysis/glossary.md |
| reference/acronyms.md           | compiled     | memory/analysis/acronyms.md |
```

---

### 6. Produce the task list

Convert every page in the hierarchy into a numbered task. Order tasks as:

1. `index.md`
2. Getting Started pages (installation before quickstart)
3. Concept pages
4. Guide pages
5. API Reference pages (one per module, alphabetical)
6. Contributing and Changelog (if applicable)
7. `reference/glossary.md` and `reference/acronyms.md`

For each task, assign depth:
- `brief` — 1–3 short paragraphs or a simple table (index, reference pages)
- `standard` — 2–5 sections with examples (getting started, guides)
- `thorough` — comprehensive coverage with code samples and cross-links (concepts, API reference)

Note dependencies explicitly (e.g., "depends on #2").

Write `memory/analysis/tasks.md`:

```markdown
# Documentation Tasks

- [ ] 1. Write index.md — project overview (brief)
- [ ] 2. Write getting-started/installation.md (standard)
- [ ] 3. Write getting-started/quickstart.md — depends on #2 (standard)
- [ ] 4. Generate api/<module>.md via mkdocstrings (thorough)
- [ ] 5. Compile reference/glossary.md from analysis (brief)
- [ ] 6. Compile reference/acronyms.md from analysis (brief)
```

---

### 7. Print summary

Output a summary table:

```
Analysis complete for <project_name>:

  Glossary terms : <n>
  Acronyms       : <n>
  Planned pages  : <n>
  Tasks created  : <n>
  [TODO] items   : <n>  ← terms/acronyms needing manual review

Files written:
  memory/analysis/glossary.md
  memory/analysis/acronyms.md
  memory/analysis/hierarchy.md
  memory/analysis/tasks.md
```

Then say:

> "Review the files in `memory/analysis/`. Edit any `[TODO]` placeholders, adjust the nav in `hierarchy.md`, and reorder tasks in `tasks.md` if needed. When satisfied, run `/mkdocs-documentation:build` to generate all documentation."
