# Spectacula

Spectacula is a spec-first workflow for Codex and Claude.

It combines:

- a reusable Codex skill at `skills/spectacula`
- a Claude-compatible prompt reference
- a repository-native spec lifecycle under `docs/spectacula`

The goal is to take a rough idea, turn it into a rigorous specification, track the work through approval and implementation, preserve resume context if execution is interrupted, and answer status questions from structured metadata.

## Repository Layout

```text
skills/
  spectacula/
    SKILL.md
    agents/openai.yaml
    references/

docs/
  spectacula/
    README.md
    templates/
    examples/
    specs/
    ready/
    inprogress/
    done/
```

## What The Skill Does

`spectacula`:

- plans before writing
- asks clarifying questions
- writes implementation-ready specs
- stores canonical specs in `docs/spectacula/specs`
- moves stage manifests across `specs`, `ready`, `inprogress`, and `done`
- preserves summary, history, verification state, and resume context
- drives implementation from the approved spec
- requires verification gates before marking work done

Primary files:

- Skill instructions: [skills/spectacula/SKILL.md](./skills/spectacula/SKILL.md)
- Claude prompt: [skills/spectacula/references/claude-portable-prompt.md](./skills/spectacula/references/claude-portable-prompt.md)
- Lifecycle contract: [skills/spectacula/references/spectacula-lifecycle.md](./skills/spectacula/references/spectacula-lifecycle.md)

## Install For Codex

Option 1: copy or symlink the skill folder into `~/.codex/skills/`:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/spectacula" ~/.codex/skills/spectacula
```

Option 2: install from GitHub after publishing:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo argonavis-labs/spectacula \
  --path skills/spectacula
```

Restart Codex after installing or updating the skill.

## Use With Claude

Copy the prompt from [skills/spectacula/references/claude-portable-prompt.md](./skills/spectacula/references/claude-portable-prompt.md) into Claude project instructions or an agent definition.

Keep using the same `docs/spectacula` directory contract so Codex and Claude share the same source of truth.

## Spectacula Lifecycle

Canonical spec text always lives in:

- `docs/spectacula/specs/<slug>.md`

Each spec also has exactly one stage manifest:

- `docs/spectacula/specs/<slug>.json`
- `docs/spectacula/ready/<slug>.json`
- `docs/spectacula/inprogress/<slug>.json`
- `docs/spectacula/done/<slug>.json`

Rules:

- Move only the JSON manifest between stage directories.
- Keep the Markdown spec fixed in `specs/`.
- Do not duplicate the full spec text in the manifest.
- Keep enough metadata to answer status questions and resume work.

See [docs/spectacula/README.md](./docs/spectacula/README.md) for the local workflow and [skills/spectacula/references/spectacula-lifecycle.md](./skills/spectacula/references/spectacula-lifecycle.md) for the authoritative contract.

## Quick Start

1. Copy [docs/spectacula/templates/spec.template.md](./docs/spectacula/templates/spec.template.md) to `docs/spectacula/specs/<slug>.md`.
2. Copy [docs/spectacula/templates/manifest.template.json](./docs/spectacula/templates/manifest.template.json) to `docs/spectacula/specs/<slug>.json`.
3. Use `spectacula` to clarify and draft the spec.
4. Move the manifest to `ready/` once approved.
5. Move the manifest to `inprogress/` when implementation starts.
6. Run verification and final spec review.
7. Move the manifest to `done/` when the implementation and review are complete.

## Examples And Templates

- Templates: [docs/spectacula/templates](./docs/spectacula/templates)
- Example spec and manifest: [docs/spectacula/examples](./docs/spectacula/examples)

## Development

Validate the skill:

```bash
PYTHONPATH=/tmp/skill-creator-deps python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/spectacula
```
