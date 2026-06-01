from __future__ import annotations

from ai_cli_env_doctor_jp.checks import node
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_node_and_npm_found_with_cmd_preference() -> None:
    which = FakeWhich({"node": "C:/node/node.exe", "npm.cmd": "C:/node/npm.cmd"})
    runner = QueueRunner(
        [
            CommandResult(("node", "--version"), 0, stdout="v22.0.0"),
            CommandResult(("npm.cmd", "--version"), 0, stdout="10.0.0"),
        ]
    )

    result = node.run(runner=runner, which=which, platform_system="Windows")

    assert result.status == Status.OK
    assert which.calls[:2] == ["node", "npm.cmd"]
    assert "Node.js と npm" in result.summary


def test_node_missing_when_npm_missing() -> None:
    which = FakeWhich({"node": "C:/node/node.exe"})
    runner = QueueRunner([CommandResult(("node", "--version"), 0, stdout="v22.0.0")])

    result = node.run(runner=runner, which=which, platform_system="Windows")

    assert result.status == Status.NOT_FOUND
    assert "npm が見つかりません" in result.details[1]
