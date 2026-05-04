# Conventions — Proscenio

Inspired by the FairCut conventions, adapted to Proscenio's polyglot pipeline (Python + GDScript + JSX + a JSON schema as contract).

## Branches

```text
feat/<short-description>      # New feature
fix/<short-description>       # Bug fix
docs/<short-description>      # Documentation only
refactor/<short-description>  # Refactor without behavior change
chore/<short-description>     # Maintenance, tooling, configs
ci/<short-description>        # Workflow changes
```

Examples: `feat/photoshop-json-importer`, `fix/godot-bone-y-flip`.

When an issue exists, reference it in the commit body (`Refs: #42`), not in the branch name. Keep branch names readable.

## Files and folders

| Convention | Used for |
| --- | --- |
| `snake_case.py` | Python modules |
| `PascalCase` | Python class names |
| `PROSCENIO_OT_*` / `PROSCENIO_PT_*` | Blender operator and panel class names (Blender requirement; ruff `N801` is silenced) |
| `snake_case.gd` | GDScript files — one class per file |
| `PascalCase` | GDScript `class_name` |
| `kebab-case` | Config and workflow file names (`.editorconfig`, `release.yml`) |
| `lower-case-no-spaces.proscenio` | Asset files |
| `UPPER_SNAKE_CASE` | Module-level constants |

## JSON keys

The `.proscenio` format uses `snake_case` keys throughout (`format_version`, `pixels_per_unit`). Any new field must follow this rule. The schema in [`schemas/proscenio.schema.json`](../schemas/proscenio.schema.json) is the source of truth.

## Versioning

Three independent SemVer streams plus one integer schema version:

| Stream | Tag prefix |
| --- | --- |
| Photoshop exporter | `photoshop-exporter-vX.Y.Z` |
| Blender addon | `blender-addon-vX.Y.Z` |
| Godot plugin | `godot-plugin-vX.Y.Z` |

`schemas/proscenio.schema.json` carries its own integer `format_version`, independent of component versions. Bump only on a breaking change to the document shape.

A schema change is a multi-component PR by definition (schema bump + Blender exporter + Godot importer guard). See [`.ai/skills/format-spec.md`](skills/format-spec.md).

## Commits

### Grouping

- One commit per cohesive unit of work.
- Do not mix components in a single commit unless the change is a schema bump (which crosses by design).
- Prefer short subjects; use the body only when the *why* is non-obvious.

### Format

Conventional Commits:

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Use for |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Refactor without behavior change |
| `test` | Tests |
| `chore` | Maintenance, tooling, configs |
| `ci` | CI workflow changes |

### Scopes

| Scope | Area |
| --- | --- |
| `blender` | Blender addon |
| `godot` | Godot plugin |
| `photoshop` | Photoshop JSX exporter |
| `schema` | `.proscenio` format schema |
| `skills` | `.ai/skills/` and `.ai/conventions.md` |
| `specs` | Planning specs under `specs/` |
| `docs` | User-facing docs (future `docs/` site) |
| `ci` | Workflows in `.github/` |
| `repo` | Root meta (license, configs, `.gitattributes`, etc.) |

### Examples

```text
feat(blender): add Photoshop JSON importer
fix(godot): flip Y on bone transform tracks
feat(schema): bump format_version to 2 for cubic interpolation
docs(skills): clarify reimport merge algorithm
chore(repo): pin ruff version in pyproject
```

## Pull requests

### Title

Same format as the commit subject:

```text
feat(blender): add Photoshop JSON importer
```

### Description

1. **What changed** — short summary.
2. **Why** — motivation if non-obvious.
3. **How to test** — concrete steps, including which Blender or Godot version.
4. **Schema impact** — if `format_version` bumped, link to the migration note.

### Template

```markdown
## What changed
<!-- one or two sentences -->

## Why
<!-- only if non-obvious -->

## How to test
<!-- concrete steps -->

## Checklist
- [ ] Lint passes (`ruff check` and/or `gdlint`)
- [ ] Tests pass (Blender headless and/or GUT)
- [ ] Schema validates against examples and fixtures
- [ ] If `format_version` changed, migration documented
```

## Code review

What to review:

1. **Correctness** — does it do what the PR claims?
2. **Boundary discipline** — Photoshop knows nothing of Blender; Blender knows nothing of Godot internals; Godot reads only `.proscenio`. See [`.ai/skills/architecture.md`](skills/architecture.md).
3. **Schema fidelity** — exporter output and importer input both match `schemas/proscenio.schema.json`.
4. **No GDExtension creep** — Godot side stays pure GDScript with built-in nodes only.
5. **Reload safety** — Blender addon `register()` / `unregister()` symmetry, no leaked classes.
6. **Test coverage** — non-trivial logic gets a fixture or a unit test.

What not to review:

- Code style — `ruff` and `gdformat` handle it.
- Personal preferences when a convention already chose.
- Formatting — covered by the editor and lint hooks.
