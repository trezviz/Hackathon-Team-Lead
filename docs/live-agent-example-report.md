# Live Agent — Completed Example Run

This is a real, end-to-end run of the live agent (`server.py`) against this
repository, using Google Gemini (`gemini-3.6-flash`) as the AI provider. It
satisfies the "one completed example of agent work" requirement: every step
below is an actual request/response captured from a live run, not a scripted
or fabricated example.

## Task

- **Goal**: "Add a short Troubleshooting section to README.md covering the case where server port 8000 is already in use."
- **Constraints**: "Only modify README.md; do not expose secrets or tokens."

## 1. Plan (real AI response)

```json
{
  "summary": "Add a Troubleshooting section to README.md explaining how to resolve port 8000 conflicts.",
  "relevantFiles": ["README.md"],
  "steps": [
    "Read README.md to determine the best place for the Troubleshooting section.",
    "Draft instructions on how to identify and free port 8000 or pass a custom port to server.py.",
    "Append the Troubleshooting section to README.md.",
    "Verify markdown formatting and ensure no secret tokens or unrelated files were altered."
  ],
  "verification": "Inspect README.md for clarity and correct markdown syntax, confirming no other files were modified.",
  "risks": "Minimal risk of minor formatting issues in README.md.",
  "secretsFlag": false,
  "editableFiles": ["README.md"]
}
```

## 2. Approval

`POST /api/approve` — plan approved before any file was touched.

## 3. Applied change (real AI-written diff, written to disk)

```diff
--- a/README.md
+++ b/README.md
@@ -29,6 +29,10 @@
 Without an AI key configured, the server still serves the real project map and search, but plan/apply endpoints return a clear error instead of a fabricated result — the agent never claims to have done work it didn't do.

 Safety guardrails enforced server-side: edits are restricted to the plan's relevant files, sensitive filenames (`.env`, `*secret*`, `*credential*`, `*token*`, `*password*`, `.pem`, `.key`) can never be selected as an edit target, and any AI output that looks like a real secret or token blocks the write.
+
+## Troubleshooting
+
+- **Port 8000 already in use**: If starting `python server.py` fails because port 8000 is occupied, set a different port via the `PORT` environment variable (e.g. `PORT=8001 python server.py` or `PORT=8001` in `.env`), or stop the process using port 8000.

 ## Run the Codex workflow
```

Changelog reported by the model: "Added a Troubleshooting section to README.md explaining how to handle server port 8000 conflicts."

## 4. Checks (real, executed server-side)

| Check | Result | Detail |
|---|---|---|
| Проверка области изменённых файлов (scope) | ✅ passed | Изменён файл README.md, входящий в согласованный список. |
| Проверка на секреты (secret-scan) | ✅ passed | Признаков секретов/токенов не найдено. |
| Проверка Markdown-форматирования | ✅ passed | Структура и локальные ссылки корректны. |

## 5. Final report

- **Changed files**: `README.md`
- **Result**: Added a Troubleshooting section to README.md explaining how to handle server port 8000 conflicts.
- **Remaining risk**: Minimal risk of minor formatting issues in README.md.
- **All checks passed**: true

## Notes from this run

- Google's Gemini API returned transient `503 Service Unavailable` responses on some attempts under load; the agent surfaced these as honest errors rather than fabricating a result, and the run succeeded on retry.
- One real bug was found and fixed during this run: the server's JSON extractor mis-detected a markdown code fence *inside* README.md's own content (a `text` fence in its "Demo prompt" section) as the model's response wrapper, which broke parsing. It was replaced with a fence check that only applies when the fence wraps the entire response, plus a proper JSON-prefix decode (`json.JSONDecoder().raw_decode`) — see `server.py`'s `extract_json`.
