from __future__ import annotations

from ai_cli_env_doctor_jp.checks import python
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_python_current_version_ok() -> None:
    runner = QueueRunner([CommandResult(("python", "--version"), 0, stdout="Python 3.12.0")])

    result = python.run(
        runner=runner,
        which=FakeWhich({"python": "C:/Python312/python.exe"}),
        version_info=(3, 12, 0),
        executable="C:/Python312/python.exe",
    )

    assert result.status == Status.OK
    assert "3.12.0" in result.summary


def test_python_current_version_too_old() -> None:
    result = python.run(
        which=FakeWhich({}),
        version_info=(3, 9, 18),
        executable="C:/Python39/python.exe",
    )

    assert result.status == Status.ERROR
    assert "3.10 未満" in result.summary


def test_python_command_failure_warns() -> None:
    runner = QueueRunner([CommandResult(("python", "--version"), 1, stderr="broken shim")])

    result = python.run(
        runner=runner,
        which=FakeWhich({"python": "C:/Python312/python.exe"}),
        version_info=(3, 12, 0),
        executable="C:/Python312/python.exe",
    )

    assert result.status == Status.WARNING
    assert "バージョン確認に失敗" in result.details[0]


def test_python_command_timeout_warns() -> None:
    runner = QueueRunner(
        [CommandResult(("python", "--version"), 124, stderr="timeout", timed_out=True)]
    )

    result = python.run(
        runner=runner,
        which=FakeWhich({"python": "C:/Python312/python.exe"}),
        version_info=(3, 12, 0),
        executable="C:/Python312/python.exe",
    )

    assert result.status == Status.WARNING
    assert "5秒以内に応答しません" in result.details[0]


def test_python_too_old_stays_error_when_command_fails() -> None:
    runner = QueueRunner([CommandResult(("python", "--version"), 1, stderr="broken shim")])

    result = python.run(
        runner=runner,
        which=FakeWhich({"python": "C:/Python39/python.exe"}),
        version_info=(3, 9, 18),
        executable="C:/Python39/python.exe",
    )

    assert result.status == Status.ERROR
