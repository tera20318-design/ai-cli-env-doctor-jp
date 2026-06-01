from __future__ import annotations

from ai_cli_env_doctor_jp.checks.common import check_version_tool
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_check_version_tool_warns_on_empty_version_output() -> None:
    runner = QueueRunner([CommandResult(("tool", "--version"), 0)])

    result = check_version_tool(
        name="tool",
        title="Tool",
        commands=("tool",),
        version_args=("--version",),
        missing_summary="missing",
        missing_next_steps=("install it",),
        ok_summary_prefix="available",
        runner=runner,
        which=FakeWhich({"tool": "C:/bin/tool.exe"}),
    )

    assert result.status == Status.WARNING
    assert result.evidence[0].value == "tool"


def test_check_version_tool_reports_timeout() -> None:
    runner = QueueRunner([CommandResult(("tool", "--version"), 1, timed_out=True)])

    result = check_version_tool(
        name="tool",
        title="Tool",
        commands=("tool",),
        version_args=("--version",),
        missing_summary="missing",
        missing_next_steps=("install it",),
        ok_summary_prefix="available",
        runner=runner,
        which=FakeWhich({"tool": "C:/bin/tool.exe"}),
    )

    assert result.status == Status.WARNING


def test_check_version_tool_reports_nonzero_exit() -> None:
    runner = QueueRunner([CommandResult(("tool", "--version"), 2, stderr="broken shim")])

    result = check_version_tool(
        name="tool",
        title="Tool",
        commands=("tool",),
        version_args=("--version",),
        missing_summary="missing",
        missing_next_steps=("install it",),
        ok_summary_prefix="available",
        runner=runner,
        which=FakeWhich({"tool": "C:/bin/tool.exe"}),
    )

    assert result.status == Status.ERROR
    assert "broken shim" in result.details
