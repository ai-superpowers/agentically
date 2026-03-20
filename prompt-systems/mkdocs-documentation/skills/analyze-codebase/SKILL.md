---
name: mkdocs-documentation-analyze-codebase
description: Scan source files to extract symbols, docstrings, domain terms, and acronyms and map them to a documentation hierarchy. Auto-apply when analyzing any repository to plan MkDocs documentation.
license: MIT
compatibility: No external dependencies. Works with Python, TypeScript/JavaScript, and config file projects.
metadata:
  author: community
  version: "1.0"
---

Procedures and heuristics for scanning a codebase and transforming raw source symbols into a structured documentation plan.

## When to use this skill

Auto-apply when the task involves:
- Reading source files to understand what a project does
- Extracting class names, function signatures, or docstrings
- Building a glossary or acronym list from code
- Deciding which files belong to which documentation section
- Mapping source file coverage to documentation pages

---

## File scanning rules

### Directories to exclude

Always skip: `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `env`, `dist`, `build`, `.tox`, `*.egg-info`, `.pytest_cache`, `.mypy_cache`, `coverage_html_report`, `htmlcov`.

### Python files (`*.py`)

Extract in this priority order:
1. Module docstring (first string literal after `import` statements)
2. Class definitions: name + class docstring
3. Function/method definitions: name + signature + docstring (first 2 sentences only)
4. `__all__` list → these are the public API surface
5. Inline comments on class/function definitions (lines starting with `#`)
6. CLI entrypoints: `if __name__ == "__main__"` blocks; `console_scripts` entries in `pyproject.toml`

**Inference fallback**: If a symbol has no docstring, infer purpose from:
- The symbol name (snake_case → human words)
- The names of its parameters
- The names of functions it calls

### TypeScript / JavaScript files (`*.ts`, `*.js`, `*.tsx`, `*.jsx`)

Extract:
1. Exported identifiers (`export class`, `export function`, `export const`, `export interface`, `export type`)
2. JSDoc comments (`/** ... */`) attached to exports
3. `README` imports or barrel files (`index.ts`) as indicators of the module's public surface

### Config files (`*.yaml`, `*.toml`, `*.json`, `*.ini`, `*.cfg`)

Extract:
1. Top-level keys as potential glossary terms if they are domain concepts
2. Inline comments as definitions
3. From `pyproject.toml`: `[project] name`, `description`, `dependencies`, `[project.scripts]`
4. From `package.json`: `name`, `description`, `scripts`, `dependencies`

### Existing documentation files (`*.md`, `*.rst`)

Extract:
1. H1 and H2 headings → reuse as documentation page titles
2. Any explicitly defined terms or glossary sections

---

## Term extraction heuristics

A term is worth including in the glossary if:
- It is a **noun** used to describe a concept (not just a variable name)
- It appears in **at least two** places (docstring + comment, or docstring + README)
- It represents something domain-specific, not a generic programming concept (prefer "Widget" over "function")

**Definition quality tiers**:
1. **Use verbatim** — docstring is a clean one-sentence definition starting with a capital letter
2. **Abbreviate** — docstring is multi-sentence; use the first sentence
3. **Synthesize** — no docstring; build from `"<Name> is a <noun> that <verb>..."` using parameter names and call graph
4. **Placeholder** — no usable context; write `"[TODO: define this term]"`

---

## Acronym detection rules

Detect an acronym if it matches any of:
- All-uppercase, 2–6 characters, appearing in identifiers or comments (e.g., `API`, `CLI`, `URL`)
- CamelCase prefix with lowercase expansion hinted nearby (e.g., `mkdocs` → MkDocs)
- A variable or parameter named `<acronym>_<noun>` (e.g., `api_key`, `cli_args`)

**Expansion resolution**:
1. Check for inline hint: `# API: Application Programming Interface` → use it
2. Check if it's a well-known software acronym → use standard expansion
3. Check if the full name appears nearby in comments → use it
4. Otherwise: `"[TODO: expand this acronym]"`

---

## Documentation hierarchy mapping

### Grouping rules

- **One nav section per logical concern**, not per file.
- A "concern" is a set of symbols that share a domain concept or user task.
- If a module has fewer than 3 exported symbols AND no unique domain concept, merge it into the nearest parent section.
- CLI commands → one Guide page per command (or group closely related commands on one page).
- Config keys → one Concepts or Reference page.

### Section decision tree

```
Does the project have install instructions or a requirements file?
  YES → include "Getting Started / Installation"

Is there a README with a usage snippet?
  YES → include "Getting Started / Quick Start"

Are there abstract concepts (data models, architecture, protocols)?
  YES → include "Concepts" section, one page per concept

Are there Python modules with public APIs?
  YES → include "API Reference" section, one page per module

Are there CLI commands?
  YES → include "Guides" section, one page per command or workflow

Does CONTRIBUTING.md or CONTRIBUTING.rst exist?
  YES → include "Contributing" page

Does CHANGELOG.md, HISTORY.md, or CHANGES.md exist?
  YES → include "Changelog" page

Always include:
  - Home (index.md)
  - Reference / Glossary
  - Reference / Acronyms
```

---

## Task depth assignment

| Page type | Depth | Criteria |
|-----------|-------|----------|
| index.md | brief | Overview only; source: README first paragraph |
| installation | standard | Prerequisites + steps + verification |
| quickstart | standard | One working example end-to-end |
| concept | thorough | Architecture, design rationale, cross-links |
| API reference | thorough | All public symbols with examples |
| guide | standard | Numbered steps with code blocks |
| contributing | brief | PRs, code style, test instructions |
| changelog | brief | Link to file or paste latest entries |
| glossary | brief | Table only |
| acronyms | brief | Table only |
