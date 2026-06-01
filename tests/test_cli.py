from __future__ import annotations

import json

from ai_cli_env_doctor_jp.cli import main
from ai_cli_env_doctor_jp.models import CheckResult, Status


def test_cli_runs_selected_check(capsys) -> None:
    registry = {
        "git": lambda: CheckResult(
            name="git",
            title="Git",
            status=Status.OK,
            summary="git が利用できます。",
        )
    }

    code = main(["--check", "git"], registry=registry)
    captured = capsys.readouterr()

    assert code == 0
    assert "[OK] Git" in captured.out


def test_cli_json_output(capsys) -> None:
    registry = {
        "git": lambda: CheckResult(
            name="git",
            title="Git",
            status=Status.OK,
            summary="git が利用できます。",
        )
    }

    code = main(["--check", "git", "--json"], registry=registry)
    payload = json.loads(capsys.readouterr().out)

    assert code == 0
    assert payload["checks"][0]["name"] == "git"


def test_cli_strict_returns_nonzero_for_warning(capsys) -> None:
    registry = {
        "uv": lambda: CheckResult(
            name="uv",
            title="uv",
            status=Status.NOT_FOUND,
            summary="uv が見つかりません。",
        )
    }

    code = main(["--check", "uv", "--strict"], registry=registry)
    capsys.readouterr()

    assert code == 1
