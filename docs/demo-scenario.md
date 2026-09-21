# Demo Scenario

## Live web agent (`server.py`)

1. Set `ANTHROPIC_API_KEY` in `.env` and run `python server.py`.
2. Open `http://127.0.0.1:8000`; the project map is the real repository file listing.
3. Give the agent a small task and constraints; Claude proposes a plan from the real files.
4. Approve the plan, pick one relevant file to edit, and select checks.
5. The agent asks Claude to rewrite that file, writes it to disk, runs real checks, and reports the real diff, check results, and risks.

## Codex / AGENTS.md workflow

1. Give the agent a small task.
2. Agent inspects the repository and proposes a plan.
3. Approve the plan.
4. Agent makes the small change, runs checks, and reports the result.
