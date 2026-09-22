"""Hackathon Tech Lead — live agent server.

Stdlib-only HTTP server that serves the local UI and a small JSON API backed
by real repository access and real calls to an LLM (Anthropic Claude or
Google Gemini). No third party packages are required.

Run:
    python server.py

Configuration (env vars, or a local .env file — see .env.example):
    ANTHROPIC_API_KEY   set to use Claude
    GEMINI_API_KEY / GOOGLE_API_KEY   set to use Gemini
    AI_PROVIDER         optional, "anthropic" or "gemini" to force a choice
                         when both keys are set (default: prefers Anthropic)
    ANTHROPIC_MODEL     optional, defaults to claude-sonnet-5
    GEMINI_MODEL        optional, defaults to gemini-3.6-flash
    PORT                optional, defaults to 8000
    HOST                optional, defaults to 127.0.0.1 (set to 0.0.0.0 in
                         containers/cloud deploys so the port is reachable)
"""

import json
import mimetypes
import os
import re
import threading
import urllib.error
import urllib.request
import uuid
from difflib import unified_diff
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
EXCLUDE_DIRS = {".git", ".specify", "node_modules", "__pycache__", ".vscode", ".idea"}
ALLOWED_EDIT_EXTENSIONS = {".md", ".txt", ".html", ".css", ".js", ".json"}
SENSITIVE_NAME_PATTERN = re.compile(r"(secret|credential|password|token|(^|\.)env(\.|$)|\.pem$|\.key$)", re.I)
SECRET_VALUE_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9]{10,}|api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16})"
)


def load_dotenv():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
AI_PROVIDER_OVERRIDE = os.environ.get("AI_PROVIDER", "").strip().lower()
AGENTS_MD = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""


def active_provider():
    if AI_PROVIDER_OVERRIDE == "anthropic" and ANTHROPIC_API_KEY:
        return "anthropic"
    if AI_PROVIDER_OVERRIDE == "gemini" and GEMINI_API_KEY:
        return "gemini"
    if ANTHROPIC_API_KEY:
        return "anthropic"
    if GEMINI_API_KEY:
        return "gemini"
    return None


def active_model():
    provider = active_provider()
    if provider == "anthropic":
        return ANTHROPIC_MODEL
    if provider == "gemini":
        return GEMINI_MODEL
    return None

PLANS = {}
PLANS_LOCK = threading.Lock()


class AgentError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def is_excluded_dir(name):
    return name in EXCLUDE_DIRS or name.startswith(".")


def list_repo_files(query=None):
    results = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        for name in filenames:
            rel = (Path(dirpath) / name).relative_to(ROOT).as_posix()
            if rel in (".env",):
                continue
            results.append(rel)
    results.sort()
    if query:
        q = query.lower()
        results = [r for r in results if q in r.lower()]
    return results


def is_sensitive_path(rel_path):
    return bool(SENSITIVE_NAME_PATTERN.search(rel_path))


def is_editable(rel_path):
    return Path(rel_path).suffix.lower() in ALLOWED_EDIT_EXTENSIONS and not is_sensitive_path(rel_path)


def scan_for_secrets(*texts):
    return any(text and SECRET_VALUE_PATTERN.search(text) for text in texts)


def call_llm(system, user, max_tokens=1600):
    provider = active_provider()
    if provider == "anthropic":
        return call_anthropic(system, user, max_tokens)
    if provider == "gemini":
        return call_gemini(system, user, max_tokens)
    raise AgentError(
        "Не настроен ключ ИИ. Задайте ANTHROPIC_API_KEY или GEMINI_API_KEY (GOOGLE_API_KEY) "
        "в файле .env (см. .env.example), чтобы включить реальные ответы ИИ.",
        503,
    )


def call_anthropic(system, user, max_tokens):
    payload = json.dumps(
        {
            "model": ANTHROPIC_MODEL,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        exc.read()
        if exc.code == 401:
            raise AgentError("Anthropic API отклонил ключ (401). Проверьте ANTHROPIC_API_KEY.", 502)
        raise AgentError(f"Ошибка Anthropic API ({exc.code}).", 502)
    except urllib.error.URLError as exc:
        raise AgentError(f"Не удалось связаться с Anthropic API: {exc.reason}", 502)
    parts = body.get("content", [])
    return "".join(part.get("text", "") for part in parts if part.get("type") == "text").strip()


def call_gemini(system, user, max_tokens):
    payload = json.dumps(
        {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
    ).encode("utf-8")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    )
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"content-type": "application/json", "x-goog-api-key": GEMINI_API_KEY},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        exc.read()
        if exc.code in (401, 403):
            raise AgentError("Gemini API отклонил ключ. Проверьте GEMINI_API_KEY / GOOGLE_API_KEY.", 502)
        raise AgentError(f"Ошибка Gemini API ({exc.code}).", 502)
    except urllib.error.URLError as exc:
        raise AgentError(f"Не удалось связаться с Gemini API: {exc.reason}", 502)
    candidates = body.get("candidates", [])
    if not candidates:
        raise AgentError("Gemini API не вернул ответ (возможно, сработал фильтр безопасности).", 502)
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(part.get("text", "") for part in parts).strip()


def extract_json(text):
    candidate = text.strip()
    if candidate.startswith("```"):
        # Only strip a fence that wraps the WHOLE response — never search for
        # fences anywhere in the text, since file content inside the JSON
        # (e.g. a README with its own ```text``` examples) can contain them.
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate)
        candidate = re.sub(r"\s*```$", "", candidate)
    start = candidate.find("{")
    if start == -1:
        raise AgentError("Модель вернула ответ без JSON.", 502)
    try:
        obj, _ = json.JSONDecoder().raw_decode(candidate, start)
        return obj
    except json.JSONDecodeError:
        raise AgentError("Не удалось разобрать JSON-ответ модели.", 502)


def generate_plan(task, constraints):
    files = list_repo_files()
    file_list_text = "\n".join(f"- {f}" for f in files[:200])
    system = (
        "Ты — агент Hackathon Tech Lead. Соблюдай правила из AGENTS.md:\n"
        f"{AGENTS_MD}\n\n"
        "Ответь СТРОГО в виде JSON без markdown-обрамления и пояснений вне JSON, со следующими "
        "полями: summary (строка), relevantFiles (массив путей файлов ТОЛЬКО из списка ниже, "
        "максимум 5), steps (массив из 3-5 коротких шагов плана), verification (строка — какие "
        "проверки уместны для этой задачи), risks (строка — оставшиеся риски), secretsFlag "
        "(boolean — true, если задача или ограничения касаются секретов, токенов или паролей)."
    )
    user = (
        f"Список файлов репозитория:\n{file_list_text}\n\n"
        f"Цель задачи: {task}\n"
        f"Ограничения: {constraints or 'не указаны'}\n\n"
        "Составь короткий безопасный план в рамках правил агента."
    )
    data = extract_json(call_llm(system, user))
    relevant = [f for f in data.get("relevantFiles", []) if isinstance(f, str) and f in files]
    if not relevant:
        relevant = files[:1]
    data["relevantFiles"] = relevant
    data["editableFiles"] = [f for f in relevant if is_editable(f) and (ROOT / f).exists()]
    return data


def apply_change(record, target_file):
    if not target_file or target_file not in record["plan"]["relevantFiles"]:
        raise AgentError("Файл вне согласованной области плана.", 400)
    if not is_editable(target_file):
        raise AgentError("Этот файл нельзя редактировать через агента (тип файла или чувствительное имя).", 400)
    full_path = (ROOT / target_file).resolve()
    if ROOT not in full_path.parents:
        raise AgentError("Недопустимый путь файла.", 400)
    if not full_path.exists():
        raise AgentError("Файл не найден в репозитории.", 404)

    original = full_path.read_text(encoding="utf-8")
    system = (
        "Ты вносишь ОДНО маленькое согласованное изменение в файл, строго в рамках задачи и "
        "ограничений. Не изменяй ничего, не относящегося к задаче. Никогда не добавляй и не "
        "раскрывай реальные секреты, токены или пароли. Ответь СТРОГО JSON без markdown-"
        'обрамления: {"newContent": "...", "changelog": "..."} — newContent содержит ПОЛНОЕ '
        "новое содержимое файла, changelog — одно предложение о том, что изменилось."
    )
    user = (
        f"Файл: {target_file}\nТекущее содержимое:\n---\n{original}\n---\n\n"
        f"Задача: {record['task']}\nОграничения: {record['constraints']}"
    )
    data = extract_json(call_llm(system, user, max_tokens=6000))
    new_content = data.get("newContent")
    changelog = str(data.get("changelog", "")).strip()
    if not isinstance(new_content, str) or not new_content.strip():
        raise AgentError("Модель не вернула содержимое файла.", 502)
    if scan_for_secrets(new_content, changelog):
        raise AgentError("Изменение заблокировано: в результате обнаружены признаки секрета/токена.", 400)

    diff = "".join(
        unified_diff(
            original.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{target_file}",
            tofile=f"b/{target_file}",
        )
    )
    full_path.write_text(new_content, encoding="utf-8")
    record["applied"] = {
        "file": target_file,
        "diff": diff,
        "changelog": changelog or "Изменение применено.",
        "changed": new_content != original,
    }
    return record["applied"]


def lint_markdown(content, rel_path):
    issues = []
    if len(re.findall(r"^# ", content, re.M)) > 1:
        issues.append("больше одного заголовка H1")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if not ((ROOT / rel_path).parent / target).exists():
            issues.append(f"битая локальная ссылка: {target}")
    return issues


def run_checks(record, selected):
    applied = record.get("applied")
    target = applied["file"] if applied else None
    content = (ROOT / target).read_text(encoding="utf-8") if target else ""
    results = []

    if "scope" in selected:
        ok = bool(target) and target in record["plan"]["relevantFiles"]
        results.append(
            {
                "name": "Проверка области изменённых файлов",
                "passed": ok,
                "detail": f"Изменён файл {target}, входящий в согласованный список."
                if ok
                else "Изменение не применялось или вышло за рамки плана.",
            }
        )

    if "secrets" in selected:
        found = scan_for_secrets(content)
        results.append(
            {
                "name": "Проверка на секреты",
                "passed": not found,
                "detail": "Признаков секретов/токенов не найдено."
                if not found
                else "Обнаружены признаки секрета — требуется ручная проверка.",
            }
        )

    if "markdown" in selected:
        if target and target.endswith(".md"):
            issues = lint_markdown(content, target)
            results.append(
                {
                    "name": "Проверка Markdown-форматирования",
                    "passed": not issues,
                    "detail": "; ".join(issues) if issues else "Структура и локальные ссылки корректны.",
                }
            )
        else:
            results.append(
                {
                    "name": "Проверка Markdown-форматирования",
                    "passed": True,
                    "detail": "Файл не Markdown — проверка неприменима.",
                }
            )

    return results


class Handler(BaseHTTPRequestHandler):
    server_version = "HackathonAgent/1.0"

    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        pass

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            raise AgentError("Некорректный JSON в запросе.", 400)

    def _serve_file(self, full_path, content_type):
        data = full_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_static(self, path):
        full = (ROOT / path.lstrip("/")).resolve()
        if ROOT not in full.parents or not full.exists() or not full.is_file():
            return self._send_json(404, {"error": "Not found"})
        content_type, _ = mimetypes.guess_type(str(full))
        self._serve_file(full, content_type or "application/octet-stream")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path in ("/", "/index.html"):
            return self._serve_file(ROOT / "index.html", "text/html; charset=utf-8")
        if path.startswith("/assets/"):
            return self._serve_static(path)
        if path == "/api/health":
            provider = active_provider()
            return self._send_json(200, {"aiConfigured": provider is not None, "provider": provider, "model": active_model()})
        if path == "/api/files":
            query = parse_qs(parsed.query).get("q", [""])[0]
            files = list_repo_files(query)
            return self._send_json(200, {"files": files, "total": len(files)})
        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._read_json()
            handler = {
                "/api/plan": self._handle_plan,
                "/api/approve": self._handle_approve,
                "/api/apply": self._handle_apply,
                "/api/checks": self._handle_checks,
                "/api/report": self._handle_report,
            }.get(path)
            if not handler:
                return self._send_json(404, {"error": "Not found"})
            handler(body)
        except AgentError as exc:
            self._send_json(exc.status, {"error": str(exc)})
        except Exception:
            self._send_json(500, {"error": "Внутренняя ошибка сервера."})

    def _get_record(self, plan_id):
        record = PLANS.get(plan_id)
        if not record:
            raise AgentError("План не найден. Сформируйте план заново.", 404)
        return record

    def _handle_plan(self, body):
        task = str(body.get("task") or "").strip()
        constraints = str(body.get("constraints") or "").strip()
        if not task:
            raise AgentError("Укажите цель задачи.", 400)
        plan = generate_plan(task, constraints)
        plan_id = uuid.uuid4().hex
        with PLANS_LOCK:
            PLANS[plan_id] = {
                "task": task,
                "constraints": constraints,
                "plan": plan,
                "approved": False,
                "applied": None,
                "checks": None,
            }
        self._send_json(200, {"planId": plan_id, "plan": plan})

    def _handle_approve(self, body):
        record = self._get_record(body.get("planId"))
        record["approved"] = True
        self._send_json(200, {"ok": True})

    def _handle_apply(self, body):
        record = self._get_record(body.get("planId"))
        if not record["approved"]:
            raise AgentError("План должен быть согласован перед изменением.", 400)
        applied = apply_change(record, body.get("targetFile"))
        self._send_json(200, applied)

    def _handle_checks(self, body):
        record = self._get_record(body.get("planId"))
        if not record["approved"]:
            raise AgentError("План должен быть согласован перед проверками.", 400)
        selected = body.get("checks") or []
        if not selected:
            raise AgentError("Выберите хотя бы одну проверку.", 400)
        results = run_checks(record, selected)
        record["checks"] = results
        self._send_json(200, {"results": results})

    def _handle_report(self, body):
        record = self._get_record(body.get("planId"))
        applied = record.get("applied")
        checks = record.get("checks") or []
        report = {
            "task": record["task"],
            "changedFiles": [applied["file"]] if applied else [],
            "diff": applied["diff"] if applied else "",
            "summary": applied["changelog"] if applied else "Изменение не применялось — план сформирован, но файл не редактировался.",
            "checks": checks,
            "risks": record["plan"].get("risks", ""),
            "allChecksPassed": bool(checks) and all(c["passed"] for c in checks),
        }
        self._send_json(200, report)


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Hackathon Tech Lead server running at http://{host}:{port}")
    provider = active_provider()
    print(f"AI provider: {provider or 'none configured'} (model: {active_model() or '-'})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
