# Research: Hackathon Tech Lead Workflow

## Decisions

### Use repository instructions as the product surface

**Decision**: Use `AGENTS.md`, the constitution, and feature artifacts as the initial product surface.

**Rationale**: The hackathon goal is to demonstrate a reliable agent workflow. This is testable now and avoids unapproved UI or infrastructure choices.

### Use Spec Kit as the traceability system

**Decision**: Each future feature follows `specify → plan → tasks → implement`.

**Rationale**: It links requests to acceptance criteria, design, implementation tasks, and verification.

### Do not add runtime storage yet

**Decision**: Keep task state in the conversation and project artifacts.

**Rationale**: No persistent multi-user product requirement exists yet.
