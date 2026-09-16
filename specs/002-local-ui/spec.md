# Feature Specification: Local Demo UI

**Feature Branch**: `002-local-ui`

**Created**: 2026-09-16
**Status**: Approved

## Product

Provide a local visual demo of the Hackathon Tech Lead workflow: task intake, plan review, explicit approval, implementation result, and verification report.

## User Scenarios & Testing

### User Story 1 - Create a safe plan (Priority: P1)

A reviewer enters a technical task and receives a visible plan before any simulated implementation is available.

**Independent Test**: Enter a task and select “Generate plan”.

**Acceptance Scenarios**:

1. **Given** a non-empty task, **When** the reviewer generates a plan, **Then** the UI shows goal, relevant files, proposed changes, and verification plan.
2. **Given** an empty task, **When** the reviewer generates a plan, **Then** the UI asks for a task and remains in the input state.

### User Story 2 - Require approval (Priority: P1)

A reviewer must explicitly approve the plan before implementation can continue.

**Independent Test**: Generate a plan and verify the result action is disabled until approval.

**Acceptance Scenarios**:

1. **Given** a generated plan, **When** the reviewer has not approved it, **Then** implementation is unavailable.
2. **Given** a generated plan, **When** the reviewer selects “Approve plan”, **Then** implementation becomes available and the state is visibly approved.

### User Story 3 - Review a verified result (Priority: P2)

After approval, a reviewer can view a concise simulated completion report.

**Independent Test**: Approve a plan and select “Complete task”.

**Acceptance Scenarios**:

1. **Given** an approved plan, **When** the reviewer completes the task, **Then** a report lists changed files, result, check status, and remaining risk.

## Edge Cases

- A task that mentions credentials or `.env` shows the safety constraint in the generated plan.
- A new task resets approval and completion state.
- The UI must remain usable without an internet connection.

## Requirements

### Functional Requirements

- **FR-001**: The UI MUST accept a task description.
- **FR-002**: The UI MUST display a plan with goal, relevant files, proposed changes, and verification.
- **FR-003**: The UI MUST require explicit approval before enabling completion.
- **FR-004**: The UI MUST display a final report with changed files, result, checks, and risks.
- **FR-005**: The UI MUST show that it is a local workflow demonstration, not a real code executor.
- **FR-006**: The UI MUST run as static local files with no network or package dependency.

### Key Entities

- **Task**: reviewer-entered description.
- **Plan**: generated goal, scope, change, and verification proposal.
- **Workflow state**: draft, planned, approved, or completed.
- **Report**: simulated result, check status, and residual risk.

## Success Criteria

- **SC-001**: A reviewer completes the full four-stage workflow in under two minutes.
- **SC-002**: Completion cannot be triggered before explicit approval.
- **SC-003**: The demo works by opening `index.html` locally.

## Assumptions

- This is a presentation UI; it does not call Codex, edit files, or execute shell commands.
- A future integration feature may connect the interface to a real agent.
