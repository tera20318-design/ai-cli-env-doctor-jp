from __future__ import annotations

import json
import os

from ai_cli_env_doctor_jp.models import CheckResult, Evidence, Status
from ai_cli_env_doctor_jp.report import (
    redact_value,
    render_json,
    render_text,
    should_fail_strict,
    summarize,
)


def test_render_text_contains_japanese_labels() -> None:
    result = CheckResult(
        name="git",
        title="Git",
        status=Status.OK,
        summary="git が利用できます。",
        next_steps=("この項目は対応不要です。",),
        evidence=(Evidence("version", "git version 2.0"),),
    )

    output = render_text([result])

    assert "ローカル環境の読み取り専用診断結果" in output
    assert "[OK] Git" in output
    assert "次の一手" in output


def test_render_json_uses_stable_top_level_shape() -> None:
    result = CheckResult(name="path", title="PATH", status=Status.WARNING, summary="警告")

    payload = json.loads(render_json([result], generated_at="2026-06-01T00:00:00+00:00"))

    assert payload["schema_version"] == "1.0"
    assert payload["generated_at"] == "2026-06-01T00:00:00+00:00"
    assert payload["summary"]["warning"] == 1
    assert payload["checks"][0]["name"] == "path"


def test_summarize_and_strict_failure() -> None:
    results = [
        CheckResult(name="python", title="Python", status=Status.OK, summary="ok"),
        CheckResult(name="uv", title="uv", status=Status.NOT_FOUND, summary="missing"),
    ]

    assert summarize(results)["ok"] == 1
    assert should_fail_strict(results) is True


def test_redact_value_masks_home_and_common_tokens() -> None:
    value = (
        "c:/users/Alice/project "
        "OPENAI_API_KEY: sk-1234567890abcdef "
        "MY_TOKEN=abc123 "
        "ghp_1234567890abcdef"
    )

    redacted = redact_value(value, home="C:/Users/alice")

    assert "~/project" in redacted
    assert "OPENAI_API_KEY=<redacted>" in redacted
    assert "MY_TOKEN=<redacted>" in redacted
    assert "ghp_<redacted>" in redacted
    assert "1234567890abcdef" not in redacted


def test_redact_value_masks_generic_home_paths() -> None:
    value = (
        r"D:\Users\Bob\repo "
        "C:/Users/Carol/project "
        "/home/dave/work "
        "/Users/erin/src"
    )

    redacted = redact_value(value, home="C:/Users/alice")

    assert r"~\repo" in redacted
    assert "~/project" in redacted
    assert "~/work" in redacted
    assert "~/src" in redacted
    assert "Bob" not in redacted
    assert "Carol" not in redacted
    assert "dave" not in redacted
    assert "erin" not in redacted


def test_redact_value_masks_additional_secret_shapes() -> None:
    value = (
        "Authorization: Bearer abcdefghijklmnop "
        "https://user:pass@example.com/path "
        "glpat-1234567890abcdef "
        "npm_1234567890abcdef "
        "AKIA1234567890ABCDEF"
    )

    redacted = redact_value(value)

    assert "Bearer <redacted>" in redacted
    assert "https://<redacted>@example.com/path" in redacted
    assert "glpat-<redacted>" in redacted
    assert "npm_<redacted>" in redacted
    assert "AKIA<redacted>" in redacted
    assert "abcdefghijklmnop" not in redacted
    assert "user:pass" not in redacted
    assert "1234567890abcdef" not in redacted


def test_redaction_applies_to_all_rendered_fields() -> None:
    home = os.path.expanduser("~")
    result = CheckResult(
        name="tool",
        title="Tool",
        status=Status.WARNING,
        summary=f"failed at {home}/project",
        details=("OPENAI_API_KEY=sk-1234567890abcdef",),
        next_steps=(f"check {home}/.config",),
        evidence=(Evidence("stderr", "MY_TOKEN=abc123"),),
    )

    output = render_text([result])

    assert home not in output
    assert "sk-1234567890abcdef" not in output
    assert "abc123" not in output


def test_render_json_redacts_evidence_values() -> None:
    home = os.path.expanduser("~")
    result = CheckResult(
        name="python",
        title="Python",
        status=Status.OK,
        summary="ok",
        evidence=(Evidence("path", f"{home}/project/.venv/Scripts/python.exe"),),
    )

    payload = json.loads(render_json([result], generated_at="2026-06-01T00:00:00+00:00"))

    assert "privacy_notice" in payload
    assert payload["summary"]["ok"] == 1
    assert payload["checks"][0]["evidence"][0]["value"].startswith("~/project")
