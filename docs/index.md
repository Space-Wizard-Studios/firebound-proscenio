# Proscenio docs

Pre-alpha. User-facing documentation lands with the MVP end-to-end sample.

For contributors: start at [AGENTS.md](../AGENTS.md) at the repo root, which directs you to [`.ai/skills/`](../.ai/skills/).

## Roadmap

### Phase 1 — MVP vertical slice

A single character with separate sprites (no mesh deformation, no slot system) goes from Blender to Godot 4 with one looping animation playing. End to end. Everything else is built on this baseline.

### Phase 2 — Pipeline completeness

- Mesh editing on top of sprites (tessellation + UV).
- Spritesheet support.
- Reimport with non-destructive merge.
- Slot system.

### Phase 3 — Polish

- Documentation site (mkdocs-material).
- Video tutorial of the full pipeline.
- Compatibility matrix tested across Blender 4.2 LTS, 4.5 LTS, 5.x and Godot 4.3, 4.4, 4.5.
- Submission to Blender Extensions Platform and Godot Asset Library.
