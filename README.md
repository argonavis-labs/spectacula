# Spectacula 🧛🏻‍♂️

Spectacula 🧛🏻‍♂️ is a spec-first workflow for Codex and Claude.

It combines:

- a reusable Codex skill at the repository root
- a first-class Claude Code plugin
- a Claude-compatible prompt reference
- a bootstrap template for creating `docs/spectacula` inside a user's working repository

The goal is to take a rough idea, turn it into a rigorous specification, track the work through approval and implementation, preserve resume context if execution is interrupted, and answer status questions from structured metadata.

## Packaging Best Practice

This repository follows a split that works well across both agent ecosystems:

- the installed package stays static and reusable
- the live `docs/spectacula` state lives in the user's project repo
- Codex uses the root [SKILL.md](./SKILL.md)
- Claude Code uses the plugin manifest at [.claude-plugin/plugin.json](./.claude-plugin/plugin.json) and the plugin skill at [skills/spectacula/SKILL.md](./skills/spectacula/SKILL.md)

The top-level `skills/` directory exists because Claude plugins require that layout. It does not mean this repo contains multiple logical skills.
The top-level `agents/` directory is shared: `openai.yaml` is Codex-facing metadata, while the Markdown files are Claude Code subagents.

## Repository Layout

```text
SKILL.md
agents/
  openai.yaml
  spectacula-architect.md
  spectacula-implementer.md
  spectacula-reviewer.md
  spectacula-status.md
.claude-plugin/
  plugin.json
  marketplace.json
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
- turns short prompts into full engineering specs by using repo context and reference examples
- audits existing specs against the current quality bar
- upgrades weaker specs in place
- stores canonical specs in `docs/spectacula/specs`
- moves stage manifests across `specs`, `ready`, `inprogress`, and `done`
- preserves summary, history, verification state, and resume context
- drives implementation from the approved spec
- requires verification gates before marking work done

Primary files:

- Skill instructions: [SKILL.md](./SKILL.md)
- Claude prompt: [references/claude-portable-prompt.md](./references/claude-portable-prompt.md)
- Claude team guidance: [references/claude-agent-teams.md](./references/claude-agent-teams.md)
- Lifecycle contract: [references/spectacula-lifecycle.md](./references/spectacula-lifecycle.md)
- Bootstrap script: [scripts/bootstrap_repo.py](./scripts/bootstrap_repo.py)
- Bootstrap template: [assets/repo-template/docs/spectacula](./assets/repo-template/docs/spectacula)
- Claude plugin manifest: [.claude-plugin/plugin.json](./.claude-plugin/plugin.json)
- Claude plugin skill: [skills/spectacula/SKILL.md](./skills/spectacula/SKILL.md)
- Claude plugin subagents: [agents](./agents)

## Better Specs With Less Prompting

Spectacula is designed so the user does not need to write a perfect prompt.

Default behavior:

- short prompts are expanded into implementation-ready specs
- repo context is used to infer affected systems and current state
- reference specs set the expected depth and structure
- clarifying questions are reserved for decisions that materially change the design
- the default output is a full technical spec, not a brief

Good minimal prompts:

```text
$spectacula Evidence-first insight detail
```

```text
$spectacula Add approval gates to the deploy workflow. Match the Attractor-style reference in depth.
```

```text
$spectacula Build a full implementation-ready spec for dashboard alert explainability. Use the repo and existing docs to fill in the current state.
```

Review prompts:

```text
$spectacula spec-audit docs/spectacula/specs
```

```text
$spectacula spec-upgrade docs/spectacula/specs/evidence-first-insight-detail.md
```

Help prompt:

```text
$spectacula help
```

When you want to steer the result more explicitly, add one of these suffixes:

- `Match this reference in depth and structure`
- `Assume implementation-ready detail by default`
- `Use the existing repo context and make reasonable assumptions`
- `Produce a full RFC-style engineering spec`
- `Audit every spec against the current Spectacula quality bar`
- `Upgrade this spec in place to match the Attractor-style reference quality`

## Install And Upgrade In Codex

Recommended Codex install modes:

- regular users: install from GitHub with the built-in Codex skill installer
- local development: symlink the repo into `~/.codex/skills`

Best-practice install for normal use:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo argonavis-labs/spectacula \
  --path . \
  --name spectacula
```

Best-practice install for local development on this repo:

```bash
mkdir -p ~/.codex/skills
ln -s /absolute/path/to/spectacula ~/.codex/skills/spectacula
```

Upgrade if you installed with a symlink:

```bash
cd /absolute/path/to/spectacula
git pull
```

Upgrade if you installed a copied snapshot from GitHub:

```bash
rm -rf ~/.codex/skills/spectacula
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo argonavis-labs/spectacula \
  --path . \
  --name spectacula
```

After any install or upgrade, restart Codex so it reloads the skill.

Codex entrypoint:

- [SKILL.md](./SKILL.md)

Codex invocation:

```text
$spectacula <your idea>
```

Examples:

```text
$spectacula help
```

```text
$spectacula Build a full implementation-ready spec for dashboard alert explainability.
```

```text
$spectacula spec-audit docs/spectacula/specs
```

```text
$spectacula spec-upgrade docs/spectacula/specs/evidence-first-insight-detail.md
```

Important:

- Installing the skill does not make this repository the home for your live specs.
- Live specs should be stored in the user's active project repo under `docs/spectacula`.
- Use the bootstrap script or copy the template into the target repo before first use.

## Install And Upgrade In Claude

Official Claude best practice is:

- use a plugin marketplace for shared installs and updates
- use `--plugin-dir` only for local development and testing

This repo now includes a marketplace manifest at [.claude-plugin/marketplace.json](./.claude-plugin/marketplace.json), so you can install it with Claude's marketplace flow.

Best-practice install from GitHub:

```text
/plugin marketplace add argonavis-labs/spectacula
/plugin install spectacula@argonavis-labs
```

Choose installation scope through the `/plugin` UI if you want `user`, `project`, or `local` scope explicitly. The CLI form also works:

```bash
claude plugin install spectacula@argonavis-labs --scope project
```

Best-practice upgrade from the marketplace:

```text
/plugin marketplace update argonavis-labs
/reload-plugins
```

Notes:

- third-party marketplaces have auto-update disabled by default in Claude; enable it in `/plugin` -> `Marketplaces` if you want automatic updates at startup
- if Claude reports that a restart is required after plugin changes, restart Claude Code
- Spectacula currently ships skills and agents, not LSP servers, so `/reload-plugins` is normally enough

Best-practice local development flow:

```bash
claude --plugin-dir /absolute/path/to/spectacula
```

Then invoke the plugin as:

```text
/spectacula:spectacula
```

If you are using `--plugin-dir`, upgrading is just updating the local repo and restarting or rerunning Claude:

```bash
cd /absolute/path/to/spectacula
git pull
```

You can still copy the prompt from [references/claude-portable-prompt.md](./references/claude-portable-prompt.md) into Claude project instructions or an agent definition when a plugin is not available.

Keep using the same `docs/spectacula` directory contract so Codex and Claude share the same source of truth.

Plugin files:

- Manifest: [.claude-plugin/plugin.json](./.claude-plugin/plugin.json)
- Marketplace: [.claude-plugin/marketplace.json](./.claude-plugin/marketplace.json)
- Skill: [skills/spectacula/SKILL.md](./skills/spectacula/SKILL.md)
- Subagents: [agents](./agents)

Claude Code entrypoint:

- `/spectacula:spectacula`

Claude usage examples:

```text
/spectacula:spectacula help
```

```text
/spectacula:spectacula Build a full implementation-ready spec for dashboard alert explainability.
```

```text
/spectacula:spectacula spec-audit docs/spectacula/specs
```

```text
/spectacula:spectacula spec-upgrade docs/spectacula/specs/evidence-first-insight-detail.md
```

Available Claude plugin subagents:

- `spectacula-architect`
- `spectacula-implementer`
- `spectacula-reviewer`
- `spectacula-status`

### Parallel / Swarm Execution In Claude

Claude's docs distinguish subagents from agent teams:

- use subagents for focused workers that report back to the lead
- use agent teams when teammates need to communicate and coordinate with each other

Agent teams are experimental and must be enabled first. Add this to Claude `settings.json` or set it in the environment:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Then start Claude with the plugin:

```bash
claude --plugin-dir /absolute/path/to/spectacula
```

Example team prompt:

```text
Create an agent team for this approved Spectacula spec. Use one spectacula-architect teammate to split the work into safe parallel tasks, two spectacula-implementer teammates for separate workstreams, and one spectacula-reviewer teammate to compare the result against the spec and verification gates. Avoid file conflicts and keep docs/spectacula resume context current.
```

See [references/claude-agent-teams.md](./references/claude-agent-teams.md) for recommended patterns.

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

## Codex Invocation

Invoke the skill explicitly in Codex with:

```text
$spectacula <your idea>
```

Examples:

```text
$spectacula help
```

```text
$spectacula Evidence-first insight detail
```

```text
$spectacula Add spec status dashboards for docs/spectacula. Use repo context and write the full implementation-ready spec.
```

```text
$spectacula Design a DOT-based workflow runner. Match the provided reference spec in depth and structure.
```

```text
$spectacula spec-audit docs/spectacula/specs and rank the weakest specs by implementation risk.
```

```text
$spectacula spec-upgrade docs/spectacula/specs/evidence-first-insight-detail.md using repo context and the Attractor-style reference as the quality bar.
```

## Help And Best-Practice Usage

Use help when you want the workflow summary without starting work:

```text
$spectacula help
```

If you accidentally type the common typo:

```text
$spectacular help
```

Spectacula should treat that as a request for help and return the same usage guidance.

Best-practice prompt patterns:

- New spec from a short idea:

```text
$spectacula <short feature or system idea>
```

- New spec with stronger steering:

```text
$spectacula <idea>. Match this reference in depth and structure. Use repo context and make reasonable assumptions.
```

- Audit all specs:

```text
$spectacula spec-audit docs/spectacula/specs
```

- Upgrade one weak spec:

```text
$spectacula spec-upgrade docs/spectacula/specs/<slug>.md
```

- Check status:

```text
$spectacula What is the status of <slug>?
```

- Drive implementation from an approved spec:

```text
$spectacula Implement docs/spectacula/specs/<slug>.md and keep the manifest current through ready, inprogress, and done.
```

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
