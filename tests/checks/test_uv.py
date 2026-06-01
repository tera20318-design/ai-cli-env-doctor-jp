from __future__ import annotations

from ai_cli_env_doctor_jp.checks import uv
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_uv_found() -> None:
    runner = QueueRunner([CommandResult(("uv", "--version"), 0, stdout="uv 0.5.0")])

    result = uv.run(runner=runner, which=FakeWhich({"uv": "/usr/bin/uv"}))

    assert result.status == Status.OK
    assert "uv が利用できます" in result.summary


def test_uv_missing_is_not_found() -> None:
    result = uv.run(which=FakeWhich({}))

    assert result.status == Status.NOT_FOUND
    assert "必須とはしません" in result.next_steps[1]
