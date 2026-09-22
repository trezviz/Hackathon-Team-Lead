# Hackathon Team Lead

Repository for a lightweight technical-lead agent workflow, with both a Codex/AGENTS.md workflow and a live local web agent.

## What this demonstrates

A Hackathon Tech Lead agent turns a small request into a scoped plan, waits for approval, makes only the approved change, verifies it, and reports the outcome honestly.

## Status

The workflow, specification, and a live local web agent are complete. The web agent reads the real repository, calls a real LLM (Anthropic Claude or Google Gemini) to plan and implement changes, and runs real checks — it is not a scripted simulation.

## Workflow

Analyze task → propose plan → receive approval → implement → verify → report.

## Run the live web agent

Requirements: Python 3.9+ and either an [Anthropic API key](https://console.anthropic.com/) or a [Google Gemini API key](https://aistudio.google.com/apikey). No other packages are installed — the server uses only the Python standard library.

1. Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY=your-key` **or** `GEMINI_API_KEY=your-key` (only one is required; if both are set, Anthropic is used unless `AI_PROVIDER=gemini` is set). `.env` is gitignored and the key is never sent to the browser or logged.
2. Start the server: `python server.py` (serves the UI and API at `http://127.0.0.1:8000`).
3. Open `http://127.0.0.1:8000` in a browser (opening `index.html` directly will not work — the UI needs the API).
4. Review the real project map or search for a file; enter a task goal and constraints.
5. Select **Составить план** — the configured model reads the real file list and returns a plan (relevant files, steps, verification, risks).
6. Select **Согласовать план**, pick the file to edit (from the plan's relevant files) and one or more checks, then select **Применить и завершить**.
7. The agent asks the model to rewrite the chosen file, writes the result to disk, runs real checks (scope, secret-scan, Markdown lint/link check), and shows the actual diff and report.

Without an AI key configured, the server still serves the real project map and search, but plan/apply endpoints return a clear error instead of a fabricated result — the agent never claims to have done work it didn't do.

Safety guardrails enforced server-side: edits are restricted to the plan's relevant files, sensitive filenames (`.env`, `*secret*`, `*credential*`, `*token*`, `*password*`, `.pem`, `.key`) can never be selected as an edit target, and any AI output that looks like a real secret or token blocks the write.

## Deploy

The server is stdlib-only Python, so it runs anywhere Python 3.9+ runs — no build step, no dependencies to install.

**Docker** (works on any host — Fly.io, Railway, Cloud Run, a VPS, etc.):

```bash
docker build -t hackathon-team-lead .
docker run -p 8000:8000 --env ANTHROPIC_API_KEY=your-key hackathon-team-lead
```

The image binds to `0.0.0.0` by default (via `HOST=0.0.0.0` set in the [Dockerfile](Dockerfile)) so the container's port is reachable from outside.

**Render**: connect the GitHub repo — [render.yaml](render.yaml) is picked up automatically. Set `ANTHROPIC_API_KEY` or `GEMINI_API_KEY` as a secret env var in the Render dashboard after the first deploy (it is intentionally left out of the file).

**Heroku / Railway / other Procfile platforms**: the included [Procfile](Procfile) (`web: python server.py`) is enough. Set `HOST=0.0.0.0` plus your AI key in the platform's config vars; these platforms set `PORT` automatically and the server already reads it.

**Any other host**: set `HOST=0.0.0.0` (or leave the default `127.0.0.1` for local-only access), set `PORT` if needed, set your AI key, then run `python server.py`.

A [GitHub Actions workflow](.github/workflows/ci.yml) compiles `server.py` and smoke-tests the `/api/health`, `/api/files`, and `/` endpoints on every push and pull request to `main`.

Never commit `.env` — it holds real API keys and is gitignored. Set keys as platform secrets/config vars instead.

## Troubleshooting

- **Port 8000 already in use**: If starting `python server.py` fails because port 8000 is occupied, set a different port via the `PORT` environment variable (e.g. `PORT=8001 python server.py` or `PORT=8001` in `.env`), or stop the process using port 8000.
- **UI API error / `index.html` opened directly**: Opening `index.html` directly in the browser as a file will fail because the UI relies on API endpoints. Run `python server.py` and open `http://127.0.0.1:8000`.
- **Missing API key**: If plan or apply actions fail, ensure `ANTHROPIC_API_KEY` or `GEMINI_API_KEY` is properly configured in `.env`.
- **Deployed behind a cloud platform but unreachable**: make sure `HOST=0.0.0.0` is set — the server defaults to `127.0.0.1`, which is not reachable from outside a container.

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
- [Live agent server](server.py)
- [Live agent UI](index.html)
- [Dockerfile](Dockerfile)
- [Render deploy config](render.yaml)
- [Procfile](Procfile)
- [CI workflow](.github/workflows/ci.yml)
- [Completed live-agent example run](docs/live-agent-example-report.md)

## Spec Kit

- [Product specification](specs/001-hackathon-tech-lead/spec.md)
- [Implementation plan](specs/001-hackathon-tech-lead/plan.md)
- [Task list](specs/001-hackathon-tech-lead/tasks.md)
- [Local UI specification](specs/002-local-ui/spec.md)
- [Agent capability demo](specs/003-agent-capabilities/spec.md)
- [Live agent (real AI) specification](specs/004-live-agent/spec.md)
