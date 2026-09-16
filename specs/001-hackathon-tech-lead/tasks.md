# Tasks: Hackathon Tech Lead Workflow

**Input**: Design documents from `specs/001-hackathon-tech-lead/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`

## Phase 1: Governance

- [x] T001 Record agent workflow and safety rules in `AGENTS.md`.
- [x] T002 Record project quality gates in `.specify/memory/constitution.md`.
- [x] T003 Document the agent role and review checklist in `docs/agent-spec.md` and `docs/agent-checklist.md`.

## Phase 2: User Story 1 - Plan a task before editing (P1)

- [x] T004 [US1] Run the analysis-only prompt from `specs/001-hackathon-tech-lead/quickstart.md`.
- [x] T005 [US1] Save the reviewed plan and confirm no files changed with `git status`.

## Phase 3: User Story 2 - Implement only an approved scope (P1)

- [x] T006 [US2] Approve the reviewed README-only plan in the Codex conversation.
- [x] T007 [US2] Implement only the approved README change in `README.md`.
- [x] T008 [US2] Confirm the changed-file scope with `git diff -- README.md`.

## Phase 4: User Story 3 - Verify and report the result (P2)

- [x] T009 [US3] Run `git diff --check` and any relevant project check.
- [x] T010 [US3] Produce the final report with changed files, summary, check results, and remaining risks.

## Phase 5: Review

- [x] T011 Review the demo against `docs/agent-checklist.md`.
- [x] T012 No requirement gap found; feature artifacts need no revision.

## Dependencies and Execution Order

`T001–T003` are complete. `T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011`. `T012` is conditional on a documented gap.
