# Implementation Plan: Live Agent (Real AI)

**Branch**: `004-live-agent` | **Date**: 2026-09-21 | **Spec**: [spec.md](spec.md)

## Technical Context

**Language**: Python 3.9+ (standard library only), browser JavaScript

**Dependencies**: None (uses `http.server`, `urllib.request`, `difflib`, `re`)

**Storage**: In-memory plan records on the server process; real edits persist to the repository files on disk

**External call**: Anthropic Messages API (`https://api.anthropic.com/v1/messages`) or Google Gemini generateContent API (`https://generativelanguage.googleapis.com/v1beta/models/*:generateContent`), key from `ANTHROPIC_API_KEY` or `GEMINI_API_KEY`/`GOOGLE_API_KEY` (env or `.env`, gitignored); provider auto-selected from which key is present, overridable via `AI_PROVIDER`

**Verification**: Manual local run against this repository plus scripted smoke checks of the server's internal safety functions

## Constitution Check

- [x] Scope is traceable to the stated requirements.
- [x] Approval is enforced server-side before edit/check endpoints accept requests.
- [x] Edits are restricted to the plan's relevant files and reject sensitive filenames.
- [x] Failures return honest errors; no fabricated success.

## Changes

- Add `server.py`: static file server + JSON API (`/api/health`, `/api/files`, `/api/plan`, `/api/approve`, `/api/apply`, `/api/checks`, `/api/report`).
- Add `.env.example` and gitignore `.env`.
- Rewrite `index.html` and `assets/app.js` to call the live API instead of running a client-side scripted state machine.
- Extend `assets/styles.css` for AI-status banner, error banner, diff view, and target-file select.
- Update `README.md` with live-agent run instructions and safety guardrails.
