# Dummy example

Hand-written end-to-end fixture for SPEC 000 Phase 1. Bypasses the Blender exporter (which does not exist yet) and exercises the Godot importer in isolation.

## Files

| File | Purpose | LFS |
| --- | --- | --- |
| `dummy.proscenio` | hand-authored character — 3 bones, 3 sprites, 1 idle animation | text |
| `dummy.blend` | minimal Blender source matching the hand-written `.proscenio` | yes |
| `atlas.png` | 256×256 placeholder texture with three labeled 80×80 regions | yes |
| `generate_atlas.py` | regenerates `atlas.png` from scratch (Pillow required) | text |

## Anatomy

```text
root          legs sprite (parented to root, polygon extends below the bone)
 │
 └─ torso     torso sprite (centered on the torso bone)
     │
     └─ head  head sprite (centered on the head bone)
              animated: head bobs ±15° on the rotation axis, 1.0 s loop
```

The atlas is 256×256. Three vertical 80×80 regions on the left edge, top to bottom: head (red), torso (blue), legs (green). Anything magenta is "off the atlas" and indicates a UV bug.

## Validate the fixture

```sh
python -m check_jsonschema --schemafile schemas/proscenio.schema.json examples/dummy/dummy.proscenio
```

Should print `ok -- validation done`.

## Next steps in the spec

This dummy is the input to the Godot importer smoke test (TODO §"Godot importer — make MVP work end-to-end" in [`specs/000-initial-plan/TODO.md`](../../specs/000-initial-plan/TODO.md)).
