# Tasks: [FEATURE NAME]

**Input**: Design documents from `specs/[###-feature-name]/`
**Prerequisites**: `plan.md` and `spec.md`

## Format

`[ID] [P?] [Story] Description with exact file path`

- `[P]` means the task can run in parallel.
- `[Story]` maps work to a user story such as `US1`.

## Phase 1: Setup

- [ ] T001 Create project structure from `plan.md`.
- [ ] T002 [P] Configure the selected development and test tooling.

## Phase 2: Foundational

- [ ] T003 Implement shared configuration and error handling.
- [ ] T004 [P] Add foundational tests for shared contracts.

## Phase 3: User Story 1 - [Title] (Priority: P1)

- [ ] T005 [P] [US1] Add failing acceptance test in [path].
- [ ] T006 [US1] Implement the user story in [path].
- [ ] T007 [US1] Add validation and verification in [path].

## Phase 4: Polish

- [ ] T008 [P] Update documentation in [path].
- [ ] T009 Run the focused verification command from `plan.md`.

## Dependencies and Execution Order

Setup -> Foundational -> User Stories -> Polish. Tests SHOULD be written before implementation when the feature has a testable contract.
