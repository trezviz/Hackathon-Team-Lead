# Hackathon Team Lead Constitution

## Core Principles

### I. Small, Traceable Changes
Every change MUST have a clear goal, a named scope, and a traceable link from specification to plan, tasks, implementation, and verification.

### II. Approval Before Editing
The agent MUST inspect relevant files and present a plan before editing. Implementation begins only after the user approves the proposed change or explicitly requests implementation.

### III. Verification Is Required
Every implementation MUST include the narrowest applicable executable check. Reports MUST distinguish passed, failed, skipped, and unavailable checks.

### IV. Secure and Minimal Handling
The agent MUST NOT expose secrets, credentials, tokens, or environment values. Unrelated files, architecture, and dependencies MUST remain unchanged.

### V. Honest Reporting
The final report MUST list changed files, summarize behavior, record checks and results, and state remaining risks or assumptions.

## Development Workflow

Use the sequence: constitution once per project, then specify -> plan -> tasks -> implement for each feature. Revisit the specification when implementation reveals a requirement gap.

## Governance

This constitution is the quality gate for all Spec Kit artifacts and implementation work in this repository. Amendments require an explicit user request and an updated version/date.

**Version**: 1.0.0 | **Ratified**: 2026-09-16 | **Last Amended**: 2026-09-16
