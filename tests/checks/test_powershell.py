from __future__ import annotations

from ai_cli_env_doctor_jp.checks import powershell
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_powershell_policy_ok() -> None:
    runner = QueueRunner(
        [
            CommandResult(
                ("pwsh", "-NoProfile", "-Command", "Get-ExecutionPolicy"), 0, stdout="RemoteSigned"
            )
        ]
    )

    result = powershell.run(
        runner=runner,
        which=FakeWhich({"pwsh": "/usr/bin/pwsh"}),
        platform_system="Windows",
    )

    assert result.status == Status.OK
    assert "RemoteSigned" in result.summary


def test_powershell_restricted_warns() -> None:
    runner = QueueRunner(
        [
            CommandResult(
                ("powershell.exe", "-NoProfile", "-Command", "Get-ExecutionPolicy"),
                0,
                stdout="Restricted",
            )
        ]
    )

    result = powershell.run(
        runner=runner,
        which=FakeWhich({"powershell.exe": "C:/Windows/System32/powershell.exe"}),
        platform_system="Windows",
    )

    assert result.status == Status.WARNING
    assert ".ps1 shim" in result.details[0]
