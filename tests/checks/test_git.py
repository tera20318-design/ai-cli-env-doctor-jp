from __future__ import annotations

from ai_cli_env_doctor_jp.checks import git
from ai_cli_env_doctor_jp.models import Status
from ai_cli_env_doctor_jp.utils import CommandResult
from tests.conftest import FakeWhich, QueueRunner


def test_git_found() -> None:
    runner = QueueRunner([CommandResult(("git", "--version"), 0, stdout="git version 2.53.0")])

    result = git.run(runner=runner, which=FakeWhich({"git": "C:/Git/bin/git.exe"}))

    assert result.status == Status.OK
    assert "git が利用できます" in result.summary


def test_git_missing() -> None:
    result = git.run(which=FakeWhich({}))

    assert result.status == Status.NOT_FOUND
    assert "Git をインストール" in result.next_steps[0]
