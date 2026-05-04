---
name: architecture
description: Repo layout, component boundaries, dependency direction, extension points
---

# Proscenio architecture

## Three components, one format

```text
Photoshop ──JSX──▶ sprites + position JSON
                        │
                        ▼
                     Blender (addon: rig, mesh, animate)
                        │
                        ▼ exporter
                  .proscenio (JSON, schema-versioned)
                        │
                        ▼ EditorImportPlugin
                     Godot .tscn (Skeleton2D + Bone2D + Polygon2D + AnimationPlayer)
```

## Strict dependency direction

- **Photoshop exporter** knows nothing of Blender or Godot. Output is generic JSON describing layer positions and exported sprite paths.
- **Blender addon** knows the Photoshop input format and the `.proscenio` output format. Knows nothing of Godot internals.
- **Godot plugin** knows only the `.proscenio` schema. Does not parse `.blend`. Does not depend on Python.
- **All three** depend on [`schemas/proscenio.schema.json`](../../schemas/proscenio.schema.json).

## What goes where

| Concern | Component |
| --- | --- |
| Layer slicing, alpha trim, position JSON | photoshop-exporter |
| Bone hierarchy, weights, keyframes | blender-addon |
| Mesh tessellation, UV, slot system | blender-addon |
| `.proscenio` file production | blender-addon (godot exporter submodule) |
| `.tscn` generation | godot-plugin |
| Reimport merge logic | godot-plugin |

## Extension points

- New input format (Krita, GIMP, Aseprite) → new module under [`blender-addon/importers/`](../../blender-addon/importers/).
- New output target (Unity, Defold, raw Spine emitter) → new module under [`blender-addon/exporters/`](../../blender-addon/exporters/).
- New animation track type → bump `format_version`, update schema, update Blender exporter, update Godot animation builder.

## Hard rules

- Generated `.tscn` must run in stock Godot **without** the Proscenio plugin installed. The plugin is import-time only.
- No GDExtension. No native libraries. No runtime dependencies in user games.
- Blender addon is GPL-3.0 (Blender constraint). Repo is GPL-3.0 throughout for simplicity.
- Format change requires `format_version` bump and a migration path.
