# Implementation Plan: Local Demo UI

**Branch**: `002-local-ui` | **Date**: 2026-09-16 | **Spec**: [spec.md](spec.md)

## Summary

Build a single-page static demo that makes the safe agent workflow visible and interactive.

## Technical Context

**Language/Version**: HTML5, CSS3, modern browser JavaScript

**Primary Dependencies**: None

**Storage**: In-memory browser state

**Testing**: Static syntax inspection and browser interaction smoke test

**Target Platform**: Modern desktop browser, opened locally

**Project Type**: Static single-page UI

**Constraints**: Offline, no API calls, no real repository changes, no secrets

## Constitution Check

- [x] Scope is small and traceable.
- [x] Approval gate is represented in the UI.
- [x] Verification is defined.
- [x] The UI does not expose secrets or modify unrelated files.

## Project Structure

```text
index.html
assets/
  styles.css
  app.js
specs/002-local-ui/
  spec.md
  research.md
  data-model.md
  quickstart.md
  plan.md
  tasks.md
```

**Structure Decision**: Keep the UI self-contained in three static files for direct local opening.
