# SPEC 000 — TODO

Closes the Phase 0 (foundation) work and primes Phase 1 (MVP). Each item is concrete, ordered roughly by dependency.

## Schema cleanup (apply Q1–Q9 decisions)

- [ ] **Q2.** Remove `"cubic"` from the `interp` enum in [`schemas/proscenio.schema.json`](../../schemas/proscenio.schema.json). Keep `"linear"` and `"constant"`.
- [ ] **Q2.** Update [`.ai/skills/format-spec.md`](../../.ai/skills/format-spec.md) interpolation row to match.
- [ ] **Q3.** Add a one-line note in `format-spec.md`: weights accepted in v1 schema, ignored by MVP importer, full skinning in Phase 2.
- [ ] **Q4.** Add a "Atlas packing" subsection to `format-spec.md` clarifying that atlases are pre-packed externally in v1.
- [ ] **Q9.** Add a "Coordinate origin" line to `format-spec.md` stating the scene-root `Node2D` is `(0, 0)`.

## Documentation

- [ ] Add `.ai/skills/references.md` listing prior-art repos with priority and what to read in each (extract from `STUDY.md` "Prior art" section).
- [ ] Expand the "Why no GDExtension" reasoning into [`.ai/skills/architecture.md`](../../.ai/skills/architecture.md) (currently one paragraph; merge the table from `STUDY.md`).
- [ ] Update `AGENTS.md` to point at `specs/` for planning specs (replacing the removed `docs/index.md` link).
- [ ] Update `README.md` to point at `specs/000-initial-plan/STUDY.md` for the current plan.

## Goblin fixture (schema-first, no Blender required)

The first end-to-end test bypasses the Blender exporter entirely and hand-writes a `.proscenio` file to validate the Godot importer.

- [ ] Hand-write `examples/goblin/goblin.proscenio` with: 3 bones (root, torso, head), 3 `Polygon2D` sprites as simple quads, one `idle` animation with one `bone_transform` track that rotates the head ±15°.
- [ ] Add a tiny placeholder `examples/goblin/atlas.png` (commit as LFS via `.gitattributes` rule already in place).
- [ ] Run `check-jsonschema --schemafile schemas/proscenio.schema.json examples/goblin/goblin.proscenio` and fix any failures.

## Godot importer — make MVP work end-to-end

Order matters. Each step must produce a visible result before moving on.

- [ ] **Smoke import.** Drop `goblin.proscenio` into `godot-plugin/`. Confirm the importer fires, parses, and produces a saved `.scn`. Fix any surface bugs.
- [ ] **Skeleton render.** Open the imported scene in the Godot editor. Verify the `Skeleton2D` and `Bone2D` hierarchy is correct visually.
- [ ] **Sprites render.** Verify each `Polygon2D` shows the right region of `atlas.png`. Y-flip and UV correctness checked by eye against the source.
- [ ] **Implement `bone_transform` track wiring.** Currently [`animation_builder.gd`](../../godot-plugin/addons/proscenio/builders/animation_builder.gd) creates empty `Animation` resources. Wire keyframes into Godot's separate position/rotation/scale tracks per `Bone2D`.
- [ ] **Animation playback.** Press Play in Godot, confirm the head rotates as authored.
- [ ] **Plugin-uninstall test.** Move `addons/proscenio/` out of the project. Confirm the imported scene still opens and plays. Critical no-GDExtension verification.

## Blender exporter — minimal path

Once the importer is proven against the hand-written fixture, write the smallest possible exporter that reproduces the same fixture from Blender data.

- [ ] Build a tiny `goblin.blend` with: 3 sprite planes, an armature with 3 bones, one animation action that rotates the head bone.
- [ ] Implement `blender-addon/exporters/godot/writer.py` — walks the active scene, emits `.proscenio` JSON conforming to the schema.
- [ ] Add an operator `proscenio.export_godot` that opens a file picker and writes the result.
- [ ] Replace the smoke-test panel button with the export button.
- [ ] Round-trip test: export `goblin.blend` → `.proscenio` → import in Godot → animation plays.

## Tests

- [ ] Add `blender-addon/tests/fixtures/goblin/` with the `.blend` and the expected `.proscenio` output.
- [ ] Replace the placeholder body of `blender-addon/tests/run_tests.py` with one assertion: re-export `goblin.blend` and compare the JSON to the expected fixture (minus volatile fields).
- [ ] Add `godot-plugin/tests/fixtures/goblin.proscenio` and a GUT test that runs the importer in headless mode and asserts node names, bone count, and animation length.
- [ ] Wire both into CI (already partially scaffolded in `.github/workflows/ci.yml`).

## Photoshop exporter

- [ ] Port `coa_tools2/Photoshop/coa_export.jsx` into `photoshop-exporter/proscenio_export.jsx`. Adapt output JSON to the format described in [`.ai/skills/photoshop-jsx-dev.md`](../../.ai/skills/photoshop-jsx-dev.md).
- [ ] Add a `photoshop-exporter/examples/` PSD or document the expected layer convention in the README.

Phase 1 ends once the goblin round-trip passes and the photoshop exporter produces the per-sprite PNGs + position JSON for the same goblin.

## Cleanup before declaring Phase 1 done

- [ ] Replace LICENSE placeholder body with the full GPL-3.0 text from gnu.org.
- [ ] Replace the placeholder maintainer email in `blender-addon/blender_manifest.toml`.
- [ ] Decide and document the canonical `Space-Wizard-Studios/proscenio` GitHub URL or update references if it differs.

## Out of scope for SPEC 000

These belong to follow-up specs, listed only so they are not lost:

- Reimport-with-merge — SPEC 002.
- Spritesheets and `Sprite2D` path — SPEC 003.
- Full skinning weights — SPEC 004.
- Slot system — SPEC 005.
