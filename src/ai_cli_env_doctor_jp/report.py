from __future__ import annotations

import json
import os
import platform
import re
from collections import Counter
from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any

from .models import CheckResult, Evidence, Status

STATUS_LABELS = {
    Status.OK: "OK",
    Status.WARNING: "警告",
    Status.ERROR: "エラー",
    Status.NOT_FOUND: "未検出",
    Status.UNKNOWN: "不明",
}

SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b([A-Z0-9_]*(?:TOKEN|SECRET|API[_-]?KEY|PASSWORD|ACCESS[_-]?KEY)[A-Z0-9_]*)"
    r"\s*[:=]\s*([^\s,;]+)"
)
WINDOWS_HOME_RE = re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\r\n]+(?=[\\/])")
POSIX_HOME_RE = re.compile(r"(?<!\w)/(?:Users|home)/[^/\r\n]+(?=/)")
URL_AUTH_RE = re.compile(r"\b([a-z][a-z0-9+.-]*://)([^/\s:@]+):([^@\s/]+)@")
BEARER_TOKEN_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}")
OPENAI_KEY_RE = re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b")
GITHUB_TOKEN_RE = re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{8,}\b")
GITLAB_TOKEN_RE = re.compile(r"\bglpat-[A-Za-z0-9_-]{8,}\b")
NPM_TOKEN_RE = re.compile(r"\bnpm_[A-Za-z0-9_-]{8,}\b")
AWS_ACCESS_KEY_RE = re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")
PRIVACY_NOTICE = "共有前に、出力内のローカルパスやユーザー名を確認してください。"


def summarize(results: Sequence[CheckResult]) -> dict[str, int]:
    counts = Counter(result.status.value for result in results)
    return {status.value: counts.get(status.value, 0) for status in Status}


def should_fail_strict(results: Sequence[CheckResult]) -> bool:
    return any(
        result.status in {Status.WARNING, Status.ERROR, Status.NOT_FOUND} for result in results
    )


def redact_value(value: str, home: str | None = None) -> str:
    redacted = value
    home_path = home if home is not None else os.path.expanduser("~")
    if home_path and home_path not in {"~", ""}:
        variants = {home_path, home_path.replace("\\", "/"), home_path.replace("/", "\\")}
        for variant in variants:
            redacted = re.sub(re.escape(variant), "~", redacted, flags=re.IGNORECASE)
    redacted = WINDOWS_HOME_RE.sub("~", redacted)
    redacted = POSIX_HOME_RE.sub("~", redacted)
    redacted = URL_AUTH_RE.sub(r"\1<redacted>@", redacted)
    redacted = BEARER_TOKEN_RE.sub("Bearer <redacted>", redacted)
    redacted = SECRET_ASSIGNMENT_RE.sub(
        lambda match: f"{match.group(1)}=<redacted>",
        redacted,
    )
    redacted = OPENAI_KEY_RE.sub("sk-<redacted>", redacted)
    redacted = GITHUB_TOKEN_RE.sub(
        lambda match: match.group(0).split("_", 1)[0] + "_<redacted>",
        redacted,
    )
    redacted = GITLAB_TOKEN_RE.sub("glpat-<redacted>", redacted)
    redacted = NPM_TOKEN_RE.sub("npm_<redacted>", redacted)
    redacted = AWS_ACCESS_KEY_RE.sub(lambda match: match.group(0)[:4] + "<redacted>", redacted)
    return redacted


def redact_result(result: CheckResult) -> CheckResult:
    return CheckResult(
        name=result.name,
        title=result.title,
        status=result.status,
        summary=redact_value(result.summary),
        details=tuple(redact_value(detail) for detail in result.details),
        next_steps=tuple(redact_value(step) for step in result.next_steps),
        evidence=tuple(
            Evidence(label=item.label, value=redact_value(item.value)) for item in result.evidence
        ),
    )


def render_text(results: Sequence[CheckResult]) -> str:
    counts = summarize(results)
    lines = [
        "AI CLI Env Doctor JP",
        "ローカル環境の読み取り専用診断結果です。",
        PRIVACY_NOTICE,
        "",
        (
            "Summary: "
            f"OK={counts['ok']} "
            f"警告={counts['warning']} "
            f"エラー={counts['error']} "
            f"未検出={counts['not_found']} "
            f"不明={counts['unknown']}"
        ),
        "",
    ]
    for result in (redact_result(result) for result in results):
        lines.append(f"[{STATUS_LABELS[result.status]}] {result.title}")
        lines.append(f"  概要: {result.summary}")
        if result.details:
            lines.append("  詳細:")
            lines.extend(f"    - {detail}" for detail in result.details)
        if result.evidence:
            lines.append("  検出情報:")
            lines.extend(f"    - {item.label}: {item.value}" for item in result.evidence)
        if result.next_steps:
            lines.append("  次の一手:")
            lines.extend(f"    - {step}" for step in result.next_steps)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_json(
    results: Sequence[CheckResult],
    generated_at: str | None = None,
) -> str:
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "privacy_notice": PRIVACY_NOTICE,
        "summary": summarize(results),
        "checks": [redact_result(result).to_dict() for result in results],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
