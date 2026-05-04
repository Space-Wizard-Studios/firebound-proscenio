# Proscenio — Photoshop exporter

ExtendScript (`.jsx`) script that exports PSD layers as PNG sprites plus a position JSON consumed by the Proscenio Blender addon.

For development guidance see [`.ai/skills/photoshop-jsx-dev.md`](../.ai/skills/photoshop-jsx-dev.md).

## Install

Copy `proscenio_export.jsx` into Photoshop's Scripts folder:

- **Windows:** `C:\Program Files\Adobe\Adobe Photoshop <version>\Presets\Scripts\`
- **macOS:** `/Applications/Adobe Photoshop <version>/Presets/Scripts/`

Restart Photoshop. Run via **File → Scripts → proscenio_export**.

## Layer conventions

The script walks the active document and exports every visible layer:

- **Hidden layers are skipped.**
- **Layer name prefix `_`** marks an artist annotation — skipped.
- **Layer groups** (`LayerSet`) are walked recursively. Output names join the
  group name and the leaf name with a double underscore (e.g. group
  `head` containing layer `eye_left` becomes `head__eye_left.png`).
- **Adjustment layers** are not exported as PNG (handled by the LayerSet
  walk skipping non-pixel layer types).

## Output layout

Run the script on `goblin.psd`:

```text
goblin.psd
goblin/
  goblin.json
  images/
    torso.png
    head.png
    arm_left.png
    ...
```

`goblin.json` matches the schema in [`.ai/skills/photoshop-jsx-dev.md`](../.ai/skills/photoshop-jsx-dev.md):
each entry carries the layer's pixel position and trimmed size, ready for the
Blender addon to import as planes.

## Status

Working scaffold. The layer walk, PNG export, and JSON manifest are in place.
Untested against a real PSD in CI — there is no headless Photoshop runner.
Manual smoke-test workflow:

1. Open a PSD with a few visible layers in Photoshop CC 2015+.
2. Run **File → Scripts → proscenio_export**.
3. Confirm `<docname>/<docname>.json` lists each layer with non-zero size and
   a matching PNG sidecar in `<docname>/images/`.
