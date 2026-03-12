# Clarifying Question Bank

Ask only the questions that materially change the design. Prefer 3-7 total. Stop when additional questions would only polish wording instead of changing decisions.

## Ask In This Priority Order

1. Outcome and success
- What must be true for this to count as successful?
- Who will approve or reject the output?
- Is the target a design doc, implementation-ready spec, RFC, or lightweight brief?

2. Scope boundaries
- What is explicitly in scope for v1?
- What is explicitly out of scope?
- Is this a net-new system, an extension of an existing one, or a replacement?

3. Audience and operators
- Who reads this spec: engineers, PMs, operators, leadership, or customers?
- Who runs or maintains the system after launch?
- Are there human approval or review steps?

4. Environment and integration
- What codebase, platform, language, provider, or runtime does this need to fit?
- What external systems, APIs, or data stores already exist?
- Does the spec need to preserve backward compatibility?

5. Constraints
- Are there deadlines, budget limits, staffing limits, or platform restrictions?
- Are there security, privacy, legal, or compliance constraints?
- Are there latency, throughput, reliability, or cost targets?

6. Data and interfaces
- What data enters the system, and what outputs are expected?
- What contracts, schemas, or interfaces are stable versus still negotiable?
- What identifiers, state, or persistence rules matter?

7. Failure handling and rollout
- What should happen on timeout, validation failure, partial failure, or operator rejection?
- Does the design need retries, fallbacks, manual override, or checkpoint/resume?
- Is rollout phased, behind a flag, or a hard cutover?

## Prefer These Question Patterns

- Ask comparison questions when choices are likely known.
- Ask for concrete targets instead of abstract preferences.
- Bundle related questions into one message so the user can answer efficiently.
- Offer a fallback path: "If unspecified, I’ll assume X and mark it in the spec."
- Prefer inference over interrogation. If repo context or the user's reference examples already answer a question well enough, do not ask it.
- Do not ask whether the user wants a full spec versus a short brief unless they explicitly indicate they want a lighter artifact.

## Example Question Sets

### New Product or Feature Spec

1. Who is the primary user, and what outcome are they trying to achieve?
2. What is in scope for v1, and what should stay out of scope?
3. Does this need to fit an existing stack, API, or design system?
4. What constraints matter most: timeline, reliability, cost, or compliance?
5. Do you want an implementation-ready spec or a lighter product brief?

### Architecture or Workflow Spec

1. Is this a new system or a change to an existing one?
2. What are the key inputs, outputs, and external dependencies?
3. What failure modes must the design explicitly handle?
4. Are there human approval, review, or escalation steps?
5. What level of detail do you want on testing, rollout, and observability?

### Service, Orchestrator, or Agent Runtime Spec

1. What are the core runtime responsibilities versus explicit non-goals?
2. What external contracts or repository-owned files define behavior?
3. What runtime state, lifecycle, or reconciliation rules must be normative?
4. What safety boundaries matter most: filesystem, secrets, approvals, sandboxing, or operator controls?
5. Do you want conformance-style validation sections and implementation checklists in the final spec?
