# Claude Agent Teams

Use this reference when Spectacula runs inside Claude Code and the task benefits from parallel workers.

## Choose Between Subagents And Agent Teams

Claude's docs distinguish these two models:

- Use subagents when you need focused workers that report back to the main agent.
- Use agent teams when workers need to communicate with each other, challenge findings, and coordinate independently.

Agent teams are a better fit for:

- parallel research and review
- cross-layer feature work
- competing debugging hypotheses
- architecture, implementation, and review workstreams that can proceed mostly independently

Agent teams are a worse fit for:

- same-file edits
- tightly sequential work
- tasks with many dependencies that force constant coordination

## Enable Agent Teams

Claude's docs say agent teams are experimental and disabled by default. Enable them with:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Put that in Claude's `settings.json` or set the environment variable before launch.

## Spectacula Plugin Agents

The plugin ships these Claude subagents:

- `spectacula-architect`
- `spectacula-implementer`
- `spectacula-reviewer`
- `spectacula-status`

Use them directly from `/agents`, or ask the lead to create a team that uses these roles.

## Recommended Team Patterns

### Spec Discovery Team

- `spectacula-architect` on system design and task decomposition
- `spectacula-reviewer` on risks, non-goals, and missing validation
- optional main lead synthesis

### Implementation Team

- `spectacula-architect` on task boundaries and conflict avoidance
- one or more `spectacula-implementer` teammates on separate workstreams
- `spectacula-reviewer` on continuous review and verification

### Status / Recovery Team

- `spectacula-status` to inspect manifests and resume context
- `spectacula-architect` to decide next safe work split
- `spectacula-reviewer` to validate whether work can move stages

## Example Prompts

### Start a design team

```text
Create an agent team for this spec. Use a spectacula-architect teammate to analyze the design, a spectacula-reviewer teammate to challenge assumptions and validation gaps, and have the lead synthesize the result into the canonical spec in docs/spectacula/specs.
```

### Start an implementation swarm

```text
Create an agent team for this approved Spectacula spec. Use one spectacula-architect teammate to split the work into safe parallel tasks, two spectacula-implementer teammates for separate workstreams, and one spectacula-reviewer teammate to compare the results against the spec and verification gates. Avoid file conflicts and keep docs/spectacula resume context current.
```

### Require plan approval before edits

```text
Create an agent team for this spec. Require plan approval before any implementer makes changes. Only approve plans that include tests and verification gates.
```

## Working Rules

- Read the canonical spec before making or reviewing changes.
- Keep the live `docs/spectacula` tree in the user's repo, not the installed plugin directory.
- Prefer one teammate per workstream with clear file ownership when possible.
- Keep review parallel but final stage movement deliberate.
- Do not move a spec to `done` until verification and spec review are complete.
