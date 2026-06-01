from __future__ import annotations

from ai_cli_env_doctor_jp.checks import codex
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_codex_prefers_cmd_on_windows() -> None:
    which = FakeWhich({"codex.cmd": "C:/node/codex.cmd", "codex.ps1": "C:/node/codex.ps1"})
    runner = QueueRunner([CommandResult(("codex.cmd", "--version"), 0, stdout="codex 0.1.0")])

    result = codex.run(runner=runner, which=which, platform_system="Windows")

    assert result.status == Status.OK
    assert which.calls[0] == "codex.cmd"
    assert any(item.value == "codex.cmd" for item in result.evidence)


def test_codex_warns_when_ps1_is_only_match_on_windows() -> None:
    which = FakeWhich({"codex.ps1": "C:/node/codex.ps1"})
    runner = QueueRunner([CommandResult(("codex.ps1", "--version"), 0, stdout="codex 0.1.0")])

    result = codex.run(runner=runner, which=which, platform_system="Windows")

    assert result.status == Status.WARNING
    assert ".ps1 shim" in result.summary
