# Tasks: Live Agent (Real AI)

- [x] T001 Add `server.py` with real file listing/search, Anthropic-backed plan/apply, and real checks.
- [x] T002 Add `.env.example` and gitignore `.env`.
- [x] T003 Rewrite `index.html` and `assets/app.js` to call the live API.
- [x] T004 Extend `assets/styles.css` for AI-status/error/diff UI.
- [x] T005 Update `README.md` with live-agent instructions and guardrails.
- [x] T006 Smoke-test server endpoints and internal safety functions (health, files, no-key error path, secret-scan, sensitive-path rejection, markdown lint).
- [x] T007 Run one full live task end to end with a real AI key and record the result in `docs/`. See [docs/live-agent-example-report.md](../../docs/live-agent-example-report.md) (run against Gemini `gemini-3.6-flash`; found and fixed a real JSON-extraction bug along the way).
