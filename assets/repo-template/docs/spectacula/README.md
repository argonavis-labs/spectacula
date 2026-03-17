# Spectacula

Canonical specs live in [specs](./specs). Each spec also has exactly one JSON manifest in the current stage directory:

- `specs/` for drafting and revision before approval
- `ready/` for approved specs waiting for implementation
- `inprogress/` for active implementation
- `done/` for completed work

Rules:

- Keep the Markdown spec in `specs/<slug>.md` as the source of truth.
- Move only the JSON manifest between stage directories.
- Do not duplicate the full spec body in manifests.
- Store enough metadata in the manifest to answer status questions and resume interrupted work.

Supporting directories:

- [templates](./templates) for reusable starting points
- [examples](./examples) for sample spec + manifest pairs

Recommended manifest fields:

- `spec_id`
- `slug`
- `title`
- `stage`
- `spec_path`
- `updated_at`
- `summary`
- `next_action`
- `resume_context`
- `history`
- `review_policy`

Recommended workflow:

1. Copy `templates/spec.template.md` into `specs/<slug>.md`
2. Copy `templates/manifest.template.json` into `specs/<slug>.json`
3. Draft until approved
4. Move the manifest to `ready/`
5. Move the manifest to `inprogress/` when implementation starts
6. Run verification and final self-review against the spec
7. If the current Spectacula call is the stricter form (`spectacula++`), run the final vetting pass and record the result
8. Move the manifest to `done/` only after the required review gates for the current task are complete
