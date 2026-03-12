---
name: spectacula
description: Plan, write, store, track, and implement detailed specifications from rough ideas. Use when Claude needs to turn a high-level prompt into a clarified, implementation-ready spec, manage the work through docs/spectacula in the user's repo, preserve resume context, or answer status questions about active or completed specs.
---

# Spectacula

Use Spectacula to turn a vague request into a tracked, implementation-ready specification and then drive the work through implementation and completion.

## Core Workflow

1. Frame the request
- Identify the artifact type, audience, constraints, dependencies, deadlines, and success criteria.
- Inspect the repo or provided docs before proposing architecture when the spec depends on an existing system.

2. Plan before writing
- Draft a short internal outline with likely sections, missing facts, major decisions, and risks.
- Match the shape and rigor of any reference specs the user provides.

3. Ask clarifying questions
- Ask 3-7 high-leverage questions when the request is still ambiguous.
- Prefer grouped, concrete questions that affect scope, interfaces, constraints, acceptance criteria, or rollout.

4. Write the spec
- Produce a structured Markdown spec with concrete behavior, interfaces, failure handling, and validation logic where relevant.
- End with a definition of done, validation matrix, acceptance checks, or an assumption ledger when those artifacts add review value.

5. Move into implementation when requested
- Treat the approved spec as the reference contract.
- Implement against it, re-read it, fix gaps, run verification gates, and finish with a final review against the same spec.

## Manage Spectacula State

- Store live specs in the user's working repository, not in the installed plugin directory.
- If `docs/spectacula` does not exist in the user's repo, bootstrap it with:

```bash
python3 "${CLAUDE_SKILL_DIR}/../../scripts/bootstrap_repo.py" .
```

- Store the canonical spec at `docs/spectacula/specs/<slug>.md`.
- Keep exactly one active JSON manifest at `docs/spectacula/specs`, `ready`, `inprogress`, or `done`.
- Move only the manifest between stage directories. Keep the spec Markdown fixed in `docs/spectacula/specs`.
- Preserve `summary`, `next_action`, `history`, `verification`, and `resume_context` so interrupted work can resume cleanly.

## Use Claude Subagents And Agent Teams

- The plugin ships focused Claude subagents in `agents/` for architecture, implementation, review, and status work.
- Use subagents for focused work that reports back to the lead.
- Use Claude agent teams when you need parallel workers that can communicate and coordinate independently.
- Agent teams are experimental and must be enabled by the user before use.
- For team patterns and prompts, see [../../references/claude-agent-teams.md](../../references/claude-agent-teams.md).

## Status Queries

When asked for the status of a spec:

- inspect the manifests in `docs/spectacula/specs`, `ready`, `inprogress`, and `done`
- match by slug first, then title
- report stage, summary, blockers, next action, verification status, updated time, and canonical spec path

## Additional Resources

- For the authoritative Codex skill instructions, see [../../SKILL.md](../../SKILL.md)
- For the lifecycle contract, see [../../references/spectacula-lifecycle.md](../../references/spectacula-lifecycle.md)
- For spec structure guidance, see [../../references/spec-blueprint.md](../../references/spec-blueprint.md)
- For clarifying-question strategy, see [../../references/question-bank.md](../../references/question-bank.md)
- For implementation handoff and verification expectations, see [../../references/implementation-handoff.md](../../references/implementation-handoff.md)
- For Claude parallel-execution guidance, see [../../references/claude-agent-teams.md](../../references/claude-agent-teams.md)
- For the scaffold copied into user repos, see [../../assets/repo-template/docs/spectacula](../../assets/repo-template/docs/spectacula)
