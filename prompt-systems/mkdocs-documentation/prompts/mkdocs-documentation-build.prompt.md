---
description: Builds complete MkDocs Material documentation from analysis artifacts. Invoke after reviewing memory/analysis/ produced by /mkdocs-documentation:analyze.
---

Generate the full MkDocs Material documentation site from your approved analysis plan. This command reads the hierarchy, tasks, glossary, and acronyms from `memory/analysis/`, writes `mkdocs.yml`, scaffolds `docs/`, and generates every documentation page end-to-end.

**Input**: Optionally provide an output directory path (e.g., `/mkdocs-documentation:build docs/`) — defaults to the `docs_output_dir` in `memory/config.yaml` or `docs/` if absent. Pass `--force` to overwrite existing files without prompting.

---

## Steps

### 1. Verify analysis artifacts exist

Check for `memory/analysis/hierarchy.md`.

- If it does **not** exist, stop and say: "No analysis found. Run `/mkdocs-documentation:analyze` first to generate the documentation plan."
- If it exists, read all four analysis files:
  - `memory/analysis/hierarchy.md` — nav structure and page sources
  - `memory/analysis/tasks.md` — ordered task list
  - `memory/analysis/glossary.md` — terms and definitions
  - `memory/analysis/acronyms.md` — acronyms and expansions
- Also read `memory/config.yaml` for `project_name`, `docs_output_dir`, `mkdocs_config_path`, and `style` settings.

Announce: "Building documentation for `<project_name>`. Output: `<docs_output_dir>/`."

---

### 2. Write `mkdocs.yml`

Create or update `mkdocs.yml` at `<mkdocs_config_path>` (default: project root).

If the file already exists and `--force` was not passed, ask: "A `mkdocs.yml` already exists. Overwrite it? (yes/no)". If the user says no, skip this step.

Generate `mkdocs.yml` with:

```yaml
site_name: <project_name>
site_description: Documentation for <project_name>
docs_dir: <docs_output_dir>

theme:
  name: material
  palette:
    primary: <style.theme_palette>   # from config, default: indigo
    accent: <style.theme_palette>
  font:
    text: Roboto
    code: Roboto Mono
  features:
    - navigation.tabs
    - navigation.instant
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy

plugins:
  - search
  # Uncomment if using Python with docstrings:
  # - mkdocstrings:
  #     handlers:
  #       python:
  #         paths: [src]

markdown_extensions:
  - admonition
  - tables
  - attr_list
  - md_in_html
  - toc:
      permalink: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.details

nav:
<nav-block from hierarchy.md, indented 2 spaces>
```

Convert the nav outline from `hierarchy.md` into valid YAML nav entries, ensuring all paths are relative to `<docs_output_dir>/`.

---

### 3. Scaffold the `docs/` directory

From the page list in `hierarchy.md`, create every subdirectory and an empty stub `.md` file for each planned page.

For each page:
- Create parent directories if they don't exist.
- If the file already exists and `--force` was not passed, skip it and note it as "skipped (exists)".
- If the file does not exist, create a stub with just the page title as an H1 heading.

Announce each directory created (e.g., "Created `docs/getting-started/`").

---

### 4. Generate each documentation page

Process tasks from `tasks.md` in order. For each task, identify the target page path and source type from `hierarchy.md`, then generate content:

**For `index.md` (Home)**:
- Write a brief overview: what the project does, who it's for, and key features.
- Source from: `README.md` (first 2–3 paragraphs), `pyproject.toml` description field, or `package.json` description.
- Include a quick-start code block if a CLI command or import is identifiable.
- Add navigation hints: "See [Getting Started](getting-started/installation.md) to install."

**For Getting Started pages**:
- `installation.md`: list prerequisites, then the install command (`pip install <name>`, `npm install <name>`, etc.), then a verification step. Source from `pyproject.toml`/`package.json` and any `INSTALL.md` or README install section.
- `quickstart.md`: write a "Hello, World" style walkthrough — import/require, one meaningful example, expected output. Source from tests, examples directory, or README usage section.

**For Concept pages**:
- Write a prose explanation of the concept (2–5 sections).
- Open with a one-paragraph summary of what the concept is and why it matters.
- Include a diagram placeholder (`[TODO: add architecture diagram]`) if the concept is architectural.
- Cross-link to relevant API reference pages using relative links.
- Source from: docstrings on core classes, inline comments describing design decisions, any `ARCHITECTURE.md` or `DESIGN.md`.

**For API Reference pages (source type: `auto`)**:
- If `api_style` is `mkdocstrings` (default):
  ```markdown
  # <Module Name>

  ::: <python.module.path>
  ```
  Add a brief intro paragraph above the directive describing the module's purpose.
- If `api_style` is `manual`:
  Write a table of exported symbols with signature + one-line description sourced from docstrings.

**For Guide pages**:
- Write numbered step-by-step instructions.
- One guide per CLI command or common workflow identified in the scan.
- Include code blocks for every command, with expected output shown in a `shell` block.

**For `reference/glossary.md`**:
- Copy and reformat the content of `memory/analysis/glossary.md` into a polished page:
  ```markdown
  # Glossary

  Terms and definitions used throughout the <project_name> documentation.

  | Term | Definition |
  | ---- | ---------- |
  ...
  ```

**For `reference/acronyms.md`**:
- Same pattern as glossary, sourced from `memory/analysis/acronyms.md`.

After writing each page:
- Mark the corresponding checkbox in `memory/analysis/tasks.md` as `[x]`.
- If any section required a `[TODO]` placeholder, note the file in a running list of pages needing review.

---

### 5. Validate nav completeness

After all pages are written:

1. Parse `mkdocs.yml` nav entries and collect all referenced file paths.
2. Check each path exists under `<docs_output_dir>/`.
3. For any missing file, create a stub with an H1 heading and a `[TODO: write this page]` note.
4. If any new stubs were created, log them as "auto-stubbed".

---

### 6. Print completion summary

Output:

```
Documentation build complete for <project_name>:

  Files created  : <n>
  Files skipped  : <n> (already existed)
  Auto-stubbed   : <n>
  [TODO] pages   : <n>  ← require manual review

Pages needing review:
  - docs/<path>.md  (<reason>)

To preview:
  pip install mkdocs-material
  mkdocs serve

To build static site:
  mkdocs build
```

Then say:

> "Documentation built in `<docs_output_dir>/`. Preview with `mkdocs serve`. Any pages marked `[TODO]` need manual content — check the list above. Run `/mkdocs-documentation:analyze` again at any time to refresh the analysis if your codebase changes."
