# SPEC 002 — TODO

Closes the reimport-merge question by adopting **Option A** (full overwrite, wrapper scene for customization) and documenting the workflow. See [STUDY.md](STUDY.md) for the full rationale and the alternative options.

## Decision lock-in

- [ ] Confirm Option A with maintainers before any of the following work begins.
- [ ] Move "Reimport non-destructive merge" from [`specs/backlog.md`](../backlog.md) to "resolved by SPEC 002" with a one-line summary.

## Documentation

- [ ] Add a "Customizing an imported scene" subsection to [`.ai/skills/godot-plugin-dev.md`](../../.ai/skills/godot-plugin-dev.md). Describe the wrapper-scene pattern: instance the generated `.scn`, attach scripts and extra nodes to the wrapper.
- [ ] Document the bone-rename caveat (Q4): a Blender bone rename invalidates wrapper-scene `NodePath`s referencing the old name. State this explicitly so users know to plan renames as cross-DCC operations.
- [ ] Document the animation-extension pattern (Q3): the wrapper's `AnimationPlayer` can hold a second library for user-authored animations.
- [ ] Update [`README.md`](../../README.md) iteration-loop section to point at the wrapper-scene pattern as the recommended workflow.

## Example asset

- [ ] Add `examples/goblin/Goblin.tscn` — a wrapper scene that instances the generated `goblin.scn`, attaches a tiny `Goblin.gd` (one exported property: a default animation name), and lives next to the source `.proscenio`. This is the documentation-by-example.
- [ ] Add a one-sentence note in [`examples/goblin/`](../../examples/goblin/) (or update its README, if any) explaining the difference between `goblin.proscenio`, `goblin.scn` (generated), and `Goblin.tscn` (user-authored wrapper).

## Importer hardening (no behavior change)

The importer already overwrites on every reimport. Add explicit safety so the user is not surprised:

- [ ] If `goblin.scn` already exists when the importer runs, log a single-line confirmation: `Proscenio: regenerating <path> (existing scene will be overwritten)`. Use `print_verbose` so it is suppressible.
- [ ] Add a unit test (GUT) that runs the importer twice on the same `.proscenio` and asserts the resulting `.scn` is byte-identical (or at least produces an identical `PackedScene` tree). Catches non-determinism early.

## Defer (potential SPEC 002.1 if demand emerges)

Track but do not implement:

- Marker-based merge (Option B) gated behind an importer flag.
- A small helper for attaching a script to a Bone2D inside the generated scene without "Editable Children".
- Stable-ID extension to the schema for rename-survivable merges. This belongs to a v2 format conversation, not this spec.
