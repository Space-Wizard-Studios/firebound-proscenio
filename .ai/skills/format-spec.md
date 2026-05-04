---
name: format-spec
description: .proscenio JSON format — fields, semantics, versioning, migrations
---

# `.proscenio` format

JSON file with extension `.proscenio`. Source of truth: [`schemas/proscenio.schema.json`](../../schemas/proscenio.schema.json). Any change to this skill must also change the schema and vice versa.

## Top level

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `format_version` | int | yes | bump on breaking change |
| `name` | string | yes | character/asset name |
| `pixels_per_unit` | number | yes | Blender unit ↔ Godot pixel ratio (e.g. 100) |
| `atlas` | string | no | path to packed atlas texture |
| `skeleton` | object | yes | bone hierarchy |
| `sprites` | array | yes | mesh + texture data |
| `slots` | array | no | sprite swap groups |
| `animations` | array | no | track data |

## Coordinate system

- 2D plane: Blender XY → Godot XY.
- Y is up in Blender, down in Godot. The exporter flips Y.
- Rotations are in radians, CCW in Blender, CW in Godot. The exporter negates.
- Scales are Vec2 multipliers around the bone origin.

The Godot importer trusts the exporter — it does not re-flip. If you write a non-Blender exporter, follow Godot conventions in the file.

## Versioning policy

- `format_version` is integer, monotonic.
- Breaking change → bump.
- Adding an optional field with a safe default → no bump.
- The schema is validated in CI for every `examples/**/*.proscenio` and every `tests/fixtures/**/*.proscenio`.

## Migration

Each version bump ships a migrator at:

```text
blender-addon/exporters/godot/migrations/v{N}_to_v{N+1}.py
```

The Godot importer rejects unknown future versions with a clear error message and refuses to import.

## Track types

| Track type | Targets | Per-key data |
| --- | --- | --- |
| `bone_transform` | `Bone2D` | `position`, `rotation`, `scale` |
| `sprite_frame` | `Sprite2D` / `Polygon2D` | `frame` (spritesheet index) |
| `slot_attachment` | slot | `attachment` (sprite name) |
| `visibility` | any | `visible` (bool) |

Per-key interpolation: `interp` field with values `linear`, `constant`, `cubic`. Default is `linear` if omitted.
