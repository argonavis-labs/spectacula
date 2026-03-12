# Todo API Specification

Status: Draft v1
Purpose: Define a small JSON API for creating, listing, completing, and deleting todo items.

## 1. Problem Statement

Applications often need a minimal task API for demos, internal tools, or test fixtures. The service should be easy to implement, easy to validate, and explicit about basic behavior.

## 2. Goals and Non-Goals

### 2.1 Goals

- Provide CRUD-style operations for todo items.
- Keep the API small and implementation-ready.
- Define enough validation and error behavior for a clean first implementation.

### 2.2 Non-Goals

- Multi-user collaboration
- Real-time sync
- Advanced search or filtering

## 3. System Overview

The service exposes a JSON HTTP API with one todo collection. Each todo has an ID, title, completion flag, and timestamps.

## 4. Core Requirements

- Create todo items with non-empty titles.
- List all todo items in reverse creation order.
- Mark a todo complete.
- Delete a todo.
- Return structured JSON errors for invalid IDs and invalid input.

## 5. Proposed Design

Resources:

- `POST /todos`
- `GET /todos`
- `POST /todos/{id}/complete`
- `DELETE /todos/{id}`

Todo schema:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable identifier |
| `title` | string | Required, trimmed, non-empty |
| `completed` | boolean | Defaults to `false` |
| `created_at` | string | ISO-8601 |
| `completed_at` | string or null | ISO-8601 when completed |

## 6. Failure Modes and Safeguards

- Empty title -> `400` with structured validation error
- Unknown ID -> `404`
- Duplicate completion -> idempotent success or explicit no-op response, but behavior must be documented and tested

## 7. Test and Validation Plan

- Run formatter and linter if the stack has them
- Run unit tests for create/list/complete/delete
- Run API-level tests for `400` and `404` behavior

## 8. Implementation Checklist

- [ ] Implement routes
- [ ] Implement request validation
- [ ] Add unit and API tests
- [ ] Run verification gates
- [ ] Review behavior against the spec

## 9. Open Questions / Assumptions

- Persistence may be in-memory for v1 unless the user requests durability.
