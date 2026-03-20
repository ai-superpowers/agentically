---
name: mkdocs-documentation-mkdocs-material
description: MkDocs Material configuration patterns, nav structure, plugin usage, and markdown extension conventions. Auto-apply when writing mkdocs.yml or generating any MkDocs documentation page.
license: MIT
compatibility: Requires mkdocs and mkdocs-material Python packages (pip install mkdocs-material).
metadata:
  author: community
  version: "1.0"
---

Reference knowledge for writing correct, idiomatic MkDocs Material configuration and documentation pages.

## When to use this skill

Auto-apply when:
- Writing or updating `mkdocs.yml`
- Generating `.md` files destined for a `docs/` directory
- Choosing plugins, markdown extensions, or theme features
- Formatting code blocks, admonitions, or tables in documentation pages
- Troubleshooting nav mismatches or build errors

---

## `mkdocs.yml` reference template

```yaml
site_name: My Project
site_description: One-sentence description of the project.
site_url: https://example.com/            # optional; set for production
repo_url: https://github.com/org/repo     # optional; adds GitHub link
repo_name: org/repo                       # optional; display name for repo link
docs_dir: docs
site_dir: site

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: Roboto
    code: Roboto Mono
  features:
    - navigation.tabs          # top-level sections as tabs
    - navigation.instant       # SPA-style instant loading
    - navigation.top           # back-to-top button
    - navigation.indexes       # section index pages
    - search.highlight         # highlight search terms on page
    - search.share             # shareable search URL
    - content.code.copy        # copy button on code blocks

plugins:
  - search

  # Python API docs — uncomment and configure if using Python
  # - mkdocstrings:
  #     handlers:
  #       python:
  #         paths: [src]        # path(s) containing Python source
  #         options:
  #           show_source: true
  #           show_root_heading: true
  #           heading_level: 2

  # Git revision dates — uncomment if repo has git history
  # - git-revision-date-localized:
  #     enable_creation_date: true

markdown_extensions:
  - admonition                 # !!! note, !!! warning, etc.
  - tables                     # GFM-style tables
  - attr_list                  # { .class } and { #id } on blocks
  - md_in_html                 # Markdown inside HTML tags
  - toc:
      permalink: true          # ¶ anchor links on headings
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.superfences       # fenced code blocks in lists, admonitions, etc.
  - pymdownx.inlinehilite      # `#!python inline code` highlighting
  - pymdownx.snippets          # --8<-- file includes
  - pymdownx.details           # ??? collapsible blocks
  - pymdownx.tabbed:
      alternate_style: true    # content tabs

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
  - Concepts:
      - Architecture: concepts/architecture.md
  - Guides:
      - Example Guide: guides/example.md
  - API Reference:
      - Module A: api/module-a.md
  - Contributing: contributing.md
  - Changelog: changelog.md
  - Reference:
      - Glossary: reference/glossary.md
      - Acronyms: reference/acronyms.md
```

---

## Nav rules

- Every nav entry must correspond to an **existing `.md` file** under `docs_dir`. Missing files cause `mkdocs build` to fail.
- Section titles (e.g., `Getting Started:`) do NOT need a file; they are just grouping labels.
- To give a section an index page, add `- Section: section/index.md` as the first item.
- File paths in nav are **relative to `docs_dir`**, not the project root.
- Omit a file from nav to hide it from the sidebar (it still builds, just not linked).

---

## mkdocstrings directives

For a Python module page, use:

```markdown
# Module Name

Brief description of what this module provides.

::: my_package.module_name
```

Options can be added inline:

```markdown
::: my_package.module_name
    options:
      show_source: false
      members_order: alphabetical
      filters:
        - "!^_"        # exclude private members
```

For a single class or function:

```markdown
::: my_package.module.ClassName
::: my_package.module.function_name
```

---

## Admonition types

```markdown
!!! note "Optional title"
    Content here. Rendered as a blue note box.

!!! warning
    Content. Yellow warning box.

!!! danger
    Content. Red danger box.

!!! tip
    Content. Green tip box.

!!! info
    Content. Blue info box.

??? example "Collapsible example"
    Content. Collapsed by default; click to expand.
```

---

## Code block formatting

Use fenced blocks with the language identifier:

````markdown
```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```
````

For shell commands, use `bash` or `shell`:

````markdown
```bash
pip install mkdocs-material
mkdocs serve
```
````

Show expected output as a separate block:

````markdown
```bash
$ mkdocs serve
INFO     -  Building documentation...
INFO     -  Serving on http://127.0.0.1:8000/
```
````

---

## Common page patterns

### Installation page

```markdown
# Installation

## Prerequisites

- Python 3.8 or later
- pip

## Install

```bash
pip install <package-name>
```

## Verify

```bash
<package-name> --version
# → <package-name> 1.0.0
```
```

### Quick Start page

```markdown
# Quick Start

## 1. Import

```python
from <package> import <ClassName>
```

## 2. Configure

```python
obj = <ClassName>(param="value")
```

## 3. Run

```python
result = obj.do_thing()
print(result)
# → expected output
```

See [API Reference](../api/<module>.md) for full details.
```

### API Reference page (manual style)

```markdown
# <Module Name>

Brief description.

## Classes

### `ClassName`

Definition and purpose.

| Parameter | Type | Description |
|-----------|------|-------------|
| `param`   | str  | What it controls |

**Example**

```python
obj = ClassName(param="x")
```
```

---

## [TODO] placeholder convention

When content cannot be inferred from the codebase, insert a clearly visible placeholder:

```markdown
[TODO: describe the architecture here]
[TODO: add a diagram showing data flow]
[TODO: expand this section with examples]
```

Always use the `[TODO: ...]` format (square brackets, uppercase TODO, colon, space, description). This makes placeholders easily searchable with `grep "[TODO]"` or a find-in-files search.

---

## Install command

```bash
pip install mkdocs-material
# For Python API docs:
pip install mkdocs-material "mkdocstrings[python]"
```

## Preview and build commands

```bash
mkdocs serve          # live-reload preview at http://127.0.0.1:8000/
mkdocs build          # build static site to site/
mkdocs build --strict # fail on warnings (recommended for CI)
```
