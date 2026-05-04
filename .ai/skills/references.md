---
name: references
description: Prior-art repos and external docs to study before implementing a feature
---

# References

External resources, ranked by how often you should reach for them while working on Proscenio. Read the relevant section before writing a feature, not after.

## Tier 1 — read before touching the relevant area

### Godot 2D Bridge — `Tor-Kai/Godot-2d-Bridge-1.0.0`

Repo: <https://github.com/Tor-Kai/Godot-2d-Bridge-1.0.0>

The closest existing prior art. A Blender addon that exports 2D meshes and armatures to a Godot scene as `Polygon2D` and `Skeleton2D` nodes. Stuck on Godot 4.0, no animation support.

What to read:

- `gd2db_scene_parsing.py` — main exporter. Note especially:
  - **Boundary-first vertex ordering via BMesh.** Boundary vertices come first to match Godot's polygon winding expectation. Replicate this when we write the Blender exporter.
  - **UV extraction.** Active render layer, scaled by image dimensions, Y-flipped.
  - **Bone weights from Blender vertex groups** mapped to Godot's `bones = [name, PoolRealArray(...)]`.
  - **Skeleton2D rest + pose.** Each bone gets a rest `Transform2D` plus a current pose value.
  - **Single armature per mesh** is a hard limit — Godot does not link more than one armature to a `Polygon2D`. We enforce the same.
- `gd2db_2d_constraints.py` — how the addon locks 2D objects to the XY plane in Blender.

What we deliberately do differently:

- They write `.tscn` text directly. We use `PackedScene.pack()` + `ResourceSaver.save()` inside an `EditorImportPlugin`. More robust against `.tscn` syntax drift and lets the engine canonicalize.
- They support Godot 1.x / 2.x / 3.x in one file. We target 4.3+ only.
- They have no animation pipeline. We do — that is the whole point of Proscenio.

### coa_tools2 — `Aodaruma/coa_tools2`

Repo: <https://github.com/Aodaruma/coa_tools2>

Forked from `ndee85/coa_tools` in 2023, alive on Blender 3.4 → 5.x. The Photoshop and Krita exporter scripts work and are the right starting point for the Proscenio Photoshop side. **The Godot export is missing entirely** — see `issue #28` (open since 2023).

What to read:

- `coa_tools2/Photoshop/coa_export.jsx` — port forward into `photoshop-exporter/proscenio_export.jsx`, adapt output JSON to our format.
- `coa_tools2/Krita/coa_export.py` — same porting target for the Krita path (Phase 2).
- The Blender addon code only as a study of how Sprite Objects, slots, and the import-from-JSON flow are structured. Do **not** copy the export pipeline — the existing JSON exporter is broken and incompatible with Blender 2.8+.
- `issue #28` thread: <https://github.com/Aodaruma/coa_tools2/issues/28>. Confirms the gap, shows EvgeneKuklin's 2023 attempt at a fix that never merged. Useful as a list of pitfalls to avoid.

### Original ndee85 — `ndee85/coa_tools`

Repo: <https://github.com/ndee85/coa_tools>

Dead since 2019. JSON export was actively being removed by the maintainer at the time. The Godot importer (`coa_importer/`) was Godot 2.x only.

Worth reading **only** for the **reimport-with-merge algorithm** in the GDScript importer. That single piece of design is recovered and modernized for Godot 4 in Phase 2 (SPEC 002).

## Tier 2 — Godot internals

### `EditorImportPlugin` docs

<https://docs.godotengine.org/en/stable/classes/class_editorimportplugin.html>

The class our plugin extends. Required reading to understand the import lifecycle, how options work, and how saved resources are placed under `.godot/imported/`.

### `PackedScene` and `ResourceSaver`

<https://docs.godotengine.org/en/stable/classes/class_packedscene.html>
<https://docs.godotengine.org/en/stable/classes/class_resourcesaver.html>

How scenes are constructed in memory and saved to disk. Crucial for the importer.

### `AnimationLibrary` and `AnimationPlayer`

<https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html>
<https://docs.godotengine.org/en/stable/classes/class_animationplayer.html>

Godot 4 separated animations from the player into reusable libraries. Our importer creates one default library `""` and adds animations to it.

### TSCN file format

<https://docs.godotengine.org/en/stable/contributing/development/file_formats/tscn.html>

We do not write `.tscn` text by hand — `PackedScene.pack()` does it for us — but understanding the format is useful when debugging diffs and reading test output.

### `Skeleton2D`, `Bone2D`, `Polygon2D`

<https://docs.godotengine.org/en/stable/classes/class_skeleton2d.html>
<https://docs.godotengine.org/en/stable/classes/class_bone2d.html>
<https://docs.godotengine.org/en/stable/classes/class_polygon2d.html>

The three nodes the importer assembles. `Polygon2D.skeleton` (NodePath) and `Polygon2D.set_bones()` are the skinning entry points consumed in Phase 2.

## Tier 3 — Blender addon authoring

### Blender Extensions Platform

<https://docs.blender.org/manual/en/latest/extensions/getting_started.html>

The 4.2+ extension system that replaces the old `bl_info` style. Our addon ships under it — see `blender_manifest.toml`.

### `bpy` API reference

<https://docs.blender.org/api/current/>

Look up specific operators, properties, and types. Stay on stable APIs only — `coa_tools2` has been chasing `bpy` drift for years (issues #92, #93, #95, #107, #109, #110, #111).

## Tier 4 — what we explicitly avoid

### Spine Godot integration

<https://github.com/EsotericSoftware/spine-runtimes/tree/4.2/spine-godot>

Cited as the anti-pattern Proscenio rejects: paid runtime, GDExtension dependency, "third-party-of-third-party" support, custom C++ engine module variant. Read once to understand why we chose differently. Do not adopt patterns from it.
