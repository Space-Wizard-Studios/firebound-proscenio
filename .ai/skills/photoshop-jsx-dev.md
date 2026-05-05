---
name: photoshop-jsx-dev
description: ExtendScript exporter for Photoshop — layer slicing and position JSON
---

# Photoshop JSX exporter

## Language

Adobe ExtendScript — legacy ECMAScript ~3 with the Photoshop DOM. **Not** modern JavaScript.

- No `let`, no `const`, no arrow functions, no template strings on older Photoshop versions. Use `var` and string concatenation.
- `JSON.stringify` is built-in only on Photoshop CC 2015+. For older versions, bundle a polyfill. Modern Photoshop is fine.
- Use `#target photoshop` directive at the top of the file.

## Output format

A JSON file alongside an `images/` folder, describing each exported layer:

```json
{
  "doc": "dummy.psd",
  "size": [1024, 1024],
  "layers": [
    {
      "name": "torso",
      "path": "dummy/torso.png",
      "position": [120, 340],
      "size": [180, 240]
    }
  ]
}
```

This JSON is consumed by `blender-addon/importers/photoshop_json.py`.

## Conventions

- Layer groups → folders in the output structure.
- Hidden layers are skipped.
- Layer name prefix `_` → exclude (artist annotation).
- Trim alpha by default; configurable via dialog.

## Reference prior art

`coa_tools2/Photoshop/coa_export.jsx` works and ships in their releases. Port forward and adjust the output schema to match Proscenio's expected shape above.

## Testing

No practical unit tests for ExtendScript. Manual: open a sample `.psd`, run the script, verify the JSON output and the PNG sidecars. Add the result to `examples/` so future regressions are visible.
