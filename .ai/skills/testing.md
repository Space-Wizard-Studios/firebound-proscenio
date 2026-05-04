---
name: testing
description: How to run lint and tests for each component
---

# Testing

## Blender addon

```sh
blender --background --python blender-addon/tests/run_tests.py
```

- Real `bpy`, no mocks.
- Fixtures: `blender-addon/tests/fixtures/*.blend`.
- CI runs against pinned Blender LTS versions on Linux.

## Godot plugin

```sh
godot --headless --path godot-plugin -s addons/gut/gut_cmdln.gd
```

- GUT framework.
- Fixtures: `.proscenio` files in `godot-plugin/tests/fixtures/`.
- CI runs against Godot 4.3 and the latest stable on Linux.

## Schema validation

Every `.proscenio` in `examples/` and `tests/fixtures/` is validated against [`schemas/proscenio.schema.json`](../../schemas/proscenio.schema.json) in CI:

```sh
check-jsonschema --schemafile schemas/proscenio.schema.json path/to/file.proscenio
```

## Lint

```sh
ruff check blender-addon/
ruff format --check blender-addon/

gdformat --check godot-plugin/addons/proscenio/
gdlint godot-plugin/addons/proscenio/
```

## End-to-end

Manual until CI runners ship both Blender and Godot:

1. Open `examples/goblin/goblin.blend` in Blender.
2. Run the Proscenio export operator.
3. Drop the resulting `.proscenio` (and texture files) into `godot-plugin/`.
4. Open the generated scene in Godot, hit Play, verify the animation runs.
