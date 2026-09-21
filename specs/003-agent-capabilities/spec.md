# Feature Specification: Agent Capability Demo

**Feature Branch**: `003-agent-capabilities`

**Created**: 2026-09-16
**Status**: Approved

## Product

Extend the local UI so a reviewer can demonstrate the six required Hackathon Tech Lead capabilities: inspect a project map, capture goal and constraints, plan, require approval, select checks, and report outcome and risks.

## User Scenarios & Testing

### User Story 1 - Inspect scope and define work (Priority: P1)

The reviewer sees a project map, searches for relevant files, enters a task, and records constraints.

**Acceptance Scenarios**:

1. **Given** a file search, **When** the reviewer enters a filename, **Then** matching project-map items are highlighted.
2. **Given** a task and constraints, **When** a plan is generated, **Then** both appear in the plan.

### User Story 2 - Gate work on approval (Priority: P1)

The reviewer receives a short plan and must approve it before checks and completion are available.

**Acceptance Scenarios**:

1. **Given** a plan, **When** it is unapproved, **Then** completion is unavailable.
2. **Given** approval, **When** checks are selected, **Then** the report action becomes available.

### User Story 3 - Verify and report (Priority: P1)

The reviewer chooses appropriate checks and sees a final report with changed files, result, check status, and risks.

**Acceptance Scenarios**:

1. **Given** approval and at least one selected check, **When** completion is selected, **Then** the final report contains each required section.

## Requirements

- **FR-001**: Display and search a project map.
- **FR-002**: Collect task goal and constraints separately.
- **FR-003**: Generate a short plan from scope, goal, and constraints.
- **FR-004**: Require explicit approval before showing verification controls.
- **FR-005**: Require at least one selected check before completion.
- **FR-006**: Report changed files, result, selected checks, and remaining risks.
- **FR-007**: Label all output as a local simulation without repository access.

## Success Criteria

- **SC-001**: All six capabilities are visible in one demo flow.
- **SC-002**: A reviewer can complete the flow in under three minutes.
- **SC-003**: Completion cannot occur without approval and a selected check.
