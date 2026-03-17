# Implementation Handoff

Use this reference when the planning/spec phase is complete and the next agent should implement the work.

## Purpose

Move from plan to code without losing rigor. The reference spec is the contract. The implementation agent should build against it, self-check against it, repair gaps, and only stop after a final review pass against the same reference.

## Default Handoff Structure

Use these directives in order. Replace `<reference spec>` with the actual spec path, title, or artifact the implementation must follow.

### 1. Implementation directive

```md
You are the best engineer with a solid foundation in Gang of Four principles and write DRY, clean, bug-free code. Implement this plan.
```

### 2. Self-check and repair loop

```md
Once you are done, make sure that you have read and built the <reference spec> and are happy with the result. If not, make the changes needed until you are happy with it.
```

### 3. Final review directive

```md
Review your work against <reference spec> and make sure that you built everything.
```

### 4. Verification gate directive

```md
Before the final review, run the available project checks for formatting, linting, type-checking, build, and tests. Fix failures and rerun the checks until they pass, or record the blocker explicitly if a passing result is not currently possible.
```

### 5. Final vetting gate directive

```md
After the self-review passes, inspect the current run's review policy. If the user invoked the stricter alias (`spectacula++`), or the active manifest records `review_policy.final_vetting = "required"`, run a final vetting pass before marking the work done. Prefer `scripts/spectacula++` or `scripts/spectacula review [<slug-or-manifest>]` to render the reviewer prompt plus current manifest/spec context, then apply that rubric as a separate read-only review inside Codex or Claude. Start with the local diff, scale the depth of review to the size and risk of the change, and treat a failed final vetting pass as blocking until the findings are addressed or the user explicitly accepts the risk.
```

## Stronger Implementation Variant

Use this variant when you want the implementation prompt to be more explicit about behavior:

```md
You are a strong implementation engineer with a solid foundation in Gang of Four principles. Write DRY, clean, bug-free code and implement the approved plan exactly as specified in <reference spec>.

After the first implementation pass:
1. Re-read <reference spec>.
2. Compare the code and behavior against the spec.
3. Fix missing requirements, incorrect behavior, weak edge-case handling, and validation gaps.
4. Run the available formatter, linter, type-checker, build, and test commands for the project.
5. Fix failures and rerun checks.
6. Record the self-review result as `verification.spec_review`.
7. If `review_policy.final_vetting = "required"`, run the final vetting gate and record it as `verification.final_vetting`.
8. Repeat until the implementation matches the spec and all required review gates are satisfied.

Before finishing, review your work against <reference spec> and verify that you built everything required.
```

## Rules For The Implementation Phase

- Treat the reference spec as normative unless the user explicitly changes scope.
- If the implementation reveals ambiguity or conflict in the spec, surface it and resolve it instead of guessing silently.
- Verify behavior, not just file presence. Match flows, interfaces, state handling, validation logic, and failure behavior described in the spec.
- If project verification commands exist, run them in this order when reasonable: format, lint, typecheck, build, tests, self-review against the spec, then final vetting when `review_policy.final_vetting = "required"`.
- If one of those gates does not exist, skip it explicitly rather than implying it passed.
- If the repository uses `docs/spectacula`, move the manifest from `ready` to `inprogress` when implementation begins, keep `resume_context` current during the work, record verification results in the manifest, and move it to `done` only after verification and self-review pass, plus final vetting pass when `review_policy.final_vetting = "required"`, or an explicit blocker is accepted.
- If the result is incomplete, continue iterating before declaring completion.

## Recommended Final Checklist

- Re-read the reference spec after the first implementation pass.
- Check every required behavior and every explicit non-goal boundary.
- Check defaults, configuration precedence, interfaces, and failure handling when applicable.
- Run available format/lint/typecheck/build/test steps.
- Fix gaps.
- Rerun verification after fixes.
- Perform one final self-review against the reference spec.
- Run the final vetting gate and record the verdict before closing when `review_policy.final_vetting = "required"`.
