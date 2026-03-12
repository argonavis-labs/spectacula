# Spectacula

Spectacula is a spec-first workflow for Codex and Claude.

It combines:

- a reusable Codex skill at the repository root
- a first-class Claude Code plugin
- a Claude-compatible prompt reference
- a bootstrap template for creating `docs/spectacula` inside a user's working repository

The goal is to take a rough idea, turn it into a rigorous specification, track the work through approval and implementation, preserve resume context if execution is interrupted, and answer status questions from structured metadata.

## Repository Layout

```text
SKILL.md
agents/
  openai.yaml
.claude-plugin/
  plugin.json
skills/
  spectacula/
    SKILL.md
references/
scripts/
assets/
  repo-template/
    docs/
      spectacula/
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

- Skill instructions: [SKILL.md](./SKILL.md)
- Claude prompt: [references/claude-portable-prompt.md](./references/claude-portable-prompt.md)
- Lifecycle contract: [references/spectacula-lifecycle.md](./references/spectacula-lifecycle.md)
- Bootstrap script: [scripts/bootstrap_repo.py](./scripts/bootstrap_repo.py)
- Bootstrap template: [assets/repo-template/docs/spectacula](./assets/repo-template/docs/spectacula)
- Claude plugin manifest: [.claude-plugin/plugin.json](./.claude-plugin/plugin.json)
- Claude plugin skill: [skills/spectacula/SKILL.md](./skills/spectacula/SKILL.md)

## Install For Codex

Option 1: copy or symlink the skill folder into `~/.codex/skills/`:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)" ~/.codex/skills/spectacula
```

Option 2: install from GitHub after publishing:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo argonavis-labs/spectacula \
  --path . \
  --name spectacula
```

Restart Codex after installing or updating the skill.

Important:

- Installing the skill does not make this repository the home for your live specs.
- Live specs should be stored in the user's active project repo under `docs/spectacula`.
- Use the bootstrap script or copy the template into the target repo before first use.

## Use With Claude

Spectacula now supports Claude Code as a real plugin, not just a pasted prompt.

Local development and testing:

```bash
claude --plugin-dir .
```

Then invoke the skill as:

```text
/spectacula:spectacula
```

You can still copy the prompt from [references/claude-portable-prompt.md](./references/claude-portable-prompt.md) into Claude project instructions or an agent definition when a plugin is not available.

Keep using the same `docs/spectacula` directory contract so Codex and Claude share the same source of truth.

Plugin files:

- Manifest: [.claude-plugin/plugin.json](./.claude-plugin/plugin.json)
- Skill: [skills/spectacula/SKILL.md](./skills/spectacula/SKILL.md)

## Bootstrap A User Repo

Create the working `docs/spectacula` tree in a user repo with:

```bash
python3 ~/.codex/skills/spectacula/scripts/bootstrap_repo.py /path/to/project-repo
```

If already inside the target repo:

```bash
python3 ~/.codex/skills/spectacula/scripts/bootstrap_repo.py .
```

This creates:

- `docs/spectacula/specs`
- `docs/spectacula/ready`
- `docs/spectacula/inprogress`
- `docs/spectacula/done`
- `docs/spectacula/templates`
- `docs/spectacula/README.md`

Use `--include-examples` if you also want sample files copied into the target repo.

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

This lifecycle lives in the user's working repo, not in the installed skill directory.

See [assets/repo-template/docs/spectacula/README.md](./assets/repo-template/docs/spectacula/README.md) for the scaffolded local workflow and [references/spectacula-lifecycle.md](./references/spectacula-lifecycle.md) for the authoritative contract.

## Quick Start

1. Run [scripts/bootstrap_repo.py](./scripts/bootstrap_repo.py) against the target repo.
2. Copy `docs/spectacula/templates/spec.template.md` in that target repo to `docs/spectacula/specs/<slug>.md`.
3. Copy `docs/spectacula/templates/manifest.template.json` in that target repo to `docs/spectacula/specs/<slug>.json`.
4. Use `spectacula` to clarify and draft the spec.
5. Move the manifest to `ready/` once approved.
6. Move the manifest to `inprogress/` when implementation starts.
7. Run verification and final spec review.
8. Move the manifest to `done/` when the implementation and review are complete.

## Examples And Templates

- Templates: [assets/repo-template/docs/spectacula/templates](./assets/repo-template/docs/spectacula/templates)
- Example spec and manifest: [assets/repo-template/docs/spectacula/examples](./assets/repo-template/docs/spectacula/examples)

## Development

Validate the skill:

```bash
PYTHONPATH=/tmp/skill-creator-deps python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Test the Claude plugin locally:

```bash
claude --plugin-dir .
```
