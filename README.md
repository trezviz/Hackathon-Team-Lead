# Hackathon Team Lead

Repository for a lightweight technical-lead agent workflow.

## Status

The workflow, specification, plan, and demo task are complete. A standalone application runtime is intentionally out of scope.

## Workflow

Analyze task → propose plan → receive approval → implement → verify → report.

## Run the workflow

1. Open the repository in Codex.
2. Ask the agent to inspect the repository and propose a plan without editing files.
3. Review and explicitly approve the plan.
4. Ask the agent to implement, verify, and report the approved change.

Requirements: Codex and Git. This project has no standalone application runtime.

## Spec Kit

- [Product specification](specs/001-hackathon-tech-lead/spec.md)
- [Implementation plan](specs/001-hackathon-tech-lead/plan.md)
- [Task list](specs/001-hackathon-tech-lead/tasks.md)
