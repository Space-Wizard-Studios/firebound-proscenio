# Backlog

Items that are not in any active SPEC. Each entry promotes into a numbered SPEC when work begins. Order within a section is rough priority.

## Format and schema

### Bezier curve preservation

**What:** the `.proscenio` v1 stores keyframes with track-level interpolation only (`linear`, `constant`); the Godot importer also offers cubic via `INTERPOLATION_CUBIC*` for smooth automatic splines. Blender authors curves with per-key Bezier handles that the format does not transmit.

**Why future-SPEC:** transmitting Bezier handles requires schema fields (`tangent_in`, `tangent_out`) and a Godot-side custom Bezier track or pre-baking. Cubic auto-spline is good enough for MVP.

**Trigger to revisit:** an animator complains that the imported animation does not match Blender to within visual tolerance.

### Multiple atlases per character

`atlas` is a single string in v1. Multi-atlas characters split into multiple `.proscenio` files. Future v2 may support an `atlas_pages` array indexed by sprite.

### Animation events (method tracks)

`AnimationPlayer` supports method tracks for audio cues, particle spawns, etc. v1 has no `event` track type.

### Per-key interpolation mixing

Schema's `interp` field is per-key but the importer applies a single track-level interpolation. Mixed `linear`/`constant`/`cubic` keys in one track would require splitting into multiple tracks at runtime or adopting a Bezier track type.

### Format detection / migration

Schema validation rejects unknown `format_version`. Once v2 lands, the Blender exporter ships `migrations/v1_to_v2.py` and the Godot importer surfaces a clear migration error pointing to the migrator.

## Blender addon

### General rig orientation detection

Writer assumes the 2D plane is Blender XZ (Z up, Y into screen). Some users author on XY (Y up). Future work: detect the dominant plane from the armature's bone axes or expose an export option.

### Multi-polygon mesh meshes

`writer._build_sprite` only emits the **first** polygon of a mesh. A mesh with multiple disjoint polygons (mask cutouts, complex topology) is silently truncated. Multi-polygon support would either:

- emit one Proscenio sprite per polygon (cleanest), or
- use `Polygon2D.polygons` array for multi-island Polygon2D nodes (preserves original mesh structure).

### Skinning weights export

Vertex group weights are read in the inspector but the writer only emits rigid attachment. Phase 2 (SPEC 004) is the planned home for this — see SPEC 000 Q3.

### Atlas region authoring helper

User UV-maps each plane in Blender to a region of the atlas; the writer reads whatever UVs are there. There is no Blender operator to "snap UV to atlas region by name". Could ship as a Phase 2 quality-of-life operator.

### IK constraints export

Out of scope for v1. Godot has built-in `Skeleton2DIK` so the user adds IK in-engine post-import. Future SPEC could detect IK constraints in the armature and round-trip them.

### Auto-detect 2D rig vs 3D mesh

Currently the writer assumes every mesh is a 2D sprite plane. A future check could skip 3D meshes or warn.

### Camera orthographic preview helper

A Blender operator that adds a properly configured ortho camera for pixel-perfect preview, matching the goblin's `pixels_per_unit`.

### Blender 4.3 legacy actions compatibility

`writer._action_fcurves` falls back to `action.fcurves` when present. Untested against Blender 4.2 LTS — may need fixture-based regression once the addon is shipped.

## Godot plugin

### Reimport non-destructive merge

**Resolved by [SPEC 002](002-reimport-merge/STUDY.md)** — adopt full overwrite plus the wrapper-scene pattern (Option A). Marker-based merge (Option B) deferred unless demand emerges.

### Spritesheet support and `Sprite2D` path

Slated for SPEC 003. Add `Sprite2D` rendering path for sprites that animate via `frame` index. Schema needs a sprite `type` discriminator or implicit detection.

### Slot system

Slated for SPEC 005. Sprite-swap groups via `slots` field; importer wires `slot_attachment` tracks.

### Node name collision polish

When a Bone2D and a child Polygon2D share a name (e.g. both called `head`), Godot auto-renames the polygon to `head_001`. Acceptable but ugly. Either prefix sprite names in the importer (`sprite_head`) or document the convention.

### Plugin-uninstall warning UI

Currently the rule "scene must work without the plugin" is enforced by review. A small editor check that opens a generated scene with the plugin disabled and asserts no errors would be a CI-friendly guard.

## Photoshop and Krita

### JSX exporter port from `coa_tools2`

Port `coa_tools2/Photoshop/coa_export.jsx` forward into `photoshop-exporter/proscenio_export.jsx`. Adapt output JSON to the format documented in `.ai/skills/photoshop-jsx-dev.md`.

### Krita exporter

`coa_tools2/Krita/coa_export.py` works in Krita 4.x. Phase 2 port-forward target.

### GIMP exporter

`coa_tools2` has a GIMP path. Lower priority — fewer 2D animation users on GIMP.

## Tests and CI

### Blender headless test runner

`blender-addon/tests/run_tests.py` is a stub. Wire `pytest` to run a real export against `tests/fixtures/*.blend`, diff against expected `.proscenio` ignoring volatile fields (timestamps).

### GUT tests for the Godot importer

`godot-plugin/tests/` is empty. Add fixtures + GUT tests asserting:

- generated scene has the expected node hierarchy
- bone count, bone names, bone rest positions
- animation library has the expected animations and track count
- imported scene runs in stock Godot without the plugin (the no-GDExtension hard rule, automated)

### CI matrix

`.github/workflows/ci.yml` lints. Add `test-blender` and `test-godot` jobs once headless tests exist. Pin Blender 4.2 LTS and 4.5 LTS, Godot 4.3 and the latest stable.

## Repo and packaging

### LICENSE full GPL-3.0 body

`LICENSE` ships the header only with a clear placeholder pointing to gnu.org. Replace with the full text before the first public release.

### Maintainer contact

`blender-addon/blender_manifest.toml` has `hello@spacewizardstudios.example`. Replace with a real address before submitting to the Blender Extensions Platform.

### Final repo URL

Confirm the canonical GitHub URL is `Space-Wizard-Studios/proscenio` and update any docs that assumed it.

### Issue and PR templates

`.github/` lacks templates. Low priority until the project is open to outside contributors.

### Statusline / dev-loop polish

The dev junction setup for the Blender addon is a manual `New-Item -ItemType Junction`. A `scripts/install-dev.ps1` would automate it. Same for copying the goblin fixture into `godot-plugin/test_goblin/`.
