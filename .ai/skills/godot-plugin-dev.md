---
name: godot-plugin-dev
description: Develop, lint, and test the Godot editor plugin
---

# Godot plugin development

## Target versions

- **Minimum:** Godot 4.3 — `AnimationLibrary` is stable and `EditorImportPlugin` is mature.
- **Tested:** Godot 4.4, latest 4.x.

## Project layout

```text
godot-plugin/
├── project.godot           # dev project — kept inline for easy testing
├── addons/proscenio/
│   ├── plugin.cfg
│   ├── plugin.gd           # EditorPlugin entry — registers importer
│   ├── importer.gd         # EditorImportPlugin
│   ├── reimporter.gd       # diff/merge logic for non-destructive reimport
│   └── builders/
│       ├── skeleton_builder.gd
│       ├── polygon_builder.gd
│       └── animation_builder.gd
└── tests/                  # GUT
```

## How import works

1. User drops a `.proscenio` file in the project.
2. Godot calls `importer.gd._import()`.
3. Importer parses the JSON and validates `format_version`.
4. Builders construct nodes in memory:
   - `Node2D` (root)
     - `Skeleton2D` → `Bone2D` (recursive) → `Polygon2D` (sprites attached to bones)
     - `AnimationPlayer` with one default `AnimationLibrary`
5. Wrap root in `PackedScene`, save via `ResourceSaver` to `.godot/imported/<hash>.scn`.

## The "no GDExtension" rule

This plugin runs **only** at editor import time. Generated scenes use built-in nodes only. To verify: open a generated `.tscn` in another Godot project that does not have Proscenio installed — it must work.

## Reimport merge (Phase 2)

When a `.proscenio` file is reimported and a previous import exists:

1. Load the existing imported scene from `.godot/imported/`.
2. Walk both trees in parallel.
3. Preserve any node not present in the new source `.proscenio` (the user added it).
4. Preserve scripts attached to source nodes.
5. Merge animations: replace ones from `.proscenio`, keep user-added ones in the same `AnimationLibrary`.

Do not implement until Phase 1 is solid and end-to-end verified.

## Coding rules

- GDScript 2.0 syntax. Use static typing wherever possible (`var x: int = 0`).
- One class per file. Filename matches the class concept.
- Format: `gdformat addons/proscenio/`. Lint: `gdlint addons/proscenio/`.
- No `@tool` scripts in user-facing scenes — only inside the plugin.

## Testing

GUT-based tests in `godot-plugin/tests/`. Run via Godot CLI:

```sh
godot --headless --path godot-plugin -s addons/gut/gut_cmdln.gd
```

Fixtures: small `.proscenio` files in `tests/fixtures/`.
