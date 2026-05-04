---
name: blender-addon-dev
description: Develop, install, lint, and test the Blender addon
---

# Blender addon development

## Target versions

- **Minimum:** Blender 4.2 LTS — required for the Extensions system (`blender_manifest.toml`).
- **Tested:** Blender 4.5 LTS, latest 5.x.
- **Python:** 3.11 (bundled with Blender 4.x).

## Project layout

```text
blender-addon/
├── blender_manifest.toml   # Blender Extensions system manifest
├── __init__.py             # entry point — registers operators/panels
├── pyproject.toml          # ruff config + dev tooling
├── core/                   # data classes — Bone, Sprite, Slot, Animation
├── operators/              # bpy.types.Operator subclasses
├── panels/                 # bpy.types.Panel subclasses
├── importers/              # PSD JSON, Krita JSON, etc.
├── exporters/godot/        # .proscenio writer
└── tests/                  # headless test suite
```

The addon ID is `proscenio` (set in the manifest). The directory name `blender-addon/` is purely repo-side; when packaged the contents are zipped, and Blender extracts to `<extensions>/proscenio/`.

## Install for development

Symlink (Windows: directory junction) the contents of `blender-addon/` into Blender's extensions directory:

```text
%APPDATA%\Blender Foundation\Blender\<version>\extensions\user_default\proscenio
```

Reload via **Preferences → Get Extensions → Reload**, or restart Blender.

## Headless tests

```sh
blender --background --python blender-addon/tests/run_tests.py
```

Tests use the real `bpy` shipped with Blender — do not mock. Fixtures live in `blender-addon/tests/fixtures/`.

## Coding rules

- All UI strings should be wrapped for `bpy.app.translations` (i18n later, hooks now).
- No global mutable state. Use `bpy.types.Scene` properties or operator properties.
- Operators must be undoable: `bl_options = {'REGISTER', 'UNDO'}`.
- Lint: `ruff check blender-addon/`. Format: `ruff format blender-addon/`.
- Lazy-import inside operator methods if a top-level import would break Blender's reload cycle.
- Always `unregister()` cleanly — leaked classes break reload.

## Manifest

`blender_manifest.toml` follows the Blender Extensions schema. Required fields: `id`, `version`, `name`, `tagline`, `maintainer`, `type = "add-on"`, `blender_version_min`, `license`. See <https://docs.blender.org/manual/en/latest/extensions/getting_started.html>.

## Common pitfalls

- Reloading addons leaks registered classes — always `unregister()` cleanly.
- `bpy.context` differs between operator and panel scope — read it carefully.
- File paths: use `bpy.path.abspath()` to resolve `//` relative paths.
- Driver and handler registration must clean up in `unregister()`.
