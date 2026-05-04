# Goblin example

End-to-end sample asset showing the full Proscenio pipeline:

```text
goblin.psd ──▶ goblin (sprites + json) ──▶ goblin.blend ──▶ goblin.proscenio ──▶ Godot scene
```

Files (added during Phase 1):

- `goblin.psd` — source PSD (Git LFS)
- `goblin.blend` — rigged and animated (Git LFS)
- `goblin.proscenio` — exported intermediate (text, in-repo)
- `goblin_atlas.png` — packed atlas (Git LFS)

## Why a goblin

Simple silhouette, distinct body parts (head, torso, two arms, two legs), minimal weights, two animations (idle, walk). Small enough to fit in CI, complex enough to exercise every track type.
