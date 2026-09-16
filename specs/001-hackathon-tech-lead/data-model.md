# Conceptual Data Model

No runtime database is required for this feature. The following concepts are represented in Markdown and the task conversation.

| Entity | Required fields | Lifecycle |
|---|---|---|
| Task | goal, constraints, scope, approval state | requested → planned → approved → implemented → reported |
| Plan | relevant files, proposed changes, verification plan | drafted → approved or revised |
| Verification record | check, status, result, limitation | created after implementation |
| Report | changed files, summary, checks, risks | created at task completion |
