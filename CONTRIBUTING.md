# Contributing to Proscenio

Read [AGENTS.md](AGENTS.md) first. It points to [`.ai/skills/`](.ai/skills/) — load the skill that matches your task before touching code.

## Setup

```sh
git clone https://github.com/Space-Wizard-Studios/firebound-proscenio
cd firebound-proscenio
git lfs install
```

For component-specific setup, see the corresponding skill in `.ai/skills/`.

## PR rules

- One component per PR (Photoshop, Blender, Godot). Exception: format-version bumps cross all components by definition.
- Conventional Commits in commit messages and PR titles.
- Squash merge.
- A schema change requires a `format_version` bump in [`schemas/proscenio.schema.json`](schemas/proscenio.schema.json) and a migration note in the PR body.
- Run lint and tests before pushing — see [`.ai/skills/testing.md`](.ai/skills/testing.md).

## License

By contributing you agree your contributions are licensed under GPL-3.0-or-later.
