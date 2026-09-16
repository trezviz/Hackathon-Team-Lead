# Tasks: Local Demo UI

**Input**: `specs/002-local-ui/`

## Phase 1: Setup

- [x] T001 Create the static application shell in `index.html`.
- [x] T002 [P] Create visual styles in `assets/styles.css`.
- [x] T003 [P] Create workflow state and interactions in `assets/app.js`.

## Phase 2: User Story 1 - Create a safe plan (P1)

- [x] T004 [US1] Add task entry, validation, and plan output in `index.html` and `assets/app.js`.

## Phase 3: User Story 2 - Require approval (P1)

- [x] T005 [US2] Add disabled completion state and explicit approval interaction in `index.html` and `assets/app.js`.

## Phase 4: User Story 3 - Review a verified result (P2)

- [x] T006 [US3] Add final report and reset interaction in `index.html` and `assets/app.js`.

## Phase 5: Verification

- [x] T007 Run static structure and file-integrity checks for the UI files. JavaScript engine unavailable in this environment.
- [ ] T008 Run a browser smoke test covering plan, approval, and completion. Blocked here because the browser policy disallows local `file://` pages.
- [x] T009 Update `README.md` with local UI launch instructions.
