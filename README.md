# Hackathon Team Lead

Repository for a lightweight technical-lead agent workflow and interactive local demo.

## What this demonstrates

A Hackathon Tech Lead agent turns a small request into a scoped plan, waits for approval, makes only the approved change, verifies it, and reports the outcome honestly.

## Status

The workflow, specification, and local interactive demo are complete.

## Workflow

Analyze task → propose plan → receive approval → implement → verify → report.

## Run locally with UI

No installation is needed.

1. Open [index.html](index.html) in a browser by double-clicking it, or use VS Code's **Open with Live Server**.
2. Enter a task and select **Generate plan**.
3. Select **Approve plan**, then **Complete task** to view the report.

The UI is an offline demonstration; it does not call an AI model, edit files, or execute commands.

## Run the Codex workflow

1. Open the repository in Codex.
2. Ask the agent to inspect the repository and propose a plan without editing files.
3. Review and explicitly approve the plan.
4. Ask the agent to implement, verify, and report the approved change.

Requirements: Codex and Git.

## Demo prompt

Copy this into a Codex chat opened in this repository:

```text
Read AGENTS.md and inspect the repository.
Propose a plan to improve README.md. Do not modify files yet.
```

After reviewing the plan, reply:

```text
Approved. Implement the plan, run checks, and report changed files, results, and risks.
```

## Project map

- [Agent rules](AGENTS.md)
- [Agent specification](docs/agent-spec.md)
- [Agent review checklist](docs/agent-checklist.md)
- [Demo scenario](docs/demo-scenario.md)

## Spec Kit

- [Product specification](specs/001-hackathon-tech-lead/spec.md)
- [Implementation plan](specs/001-hackathon-tech-lead/plan.md)
- [Task list](specs/001-hackathon-tech-lead/tasks.md)
- [Local UI specification](specs/002-local-ui/spec.md)
