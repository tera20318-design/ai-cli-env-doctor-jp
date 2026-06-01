from __future__ import annotations

import shutil

from ..models import CheckResult
from ..utils import CommandRunner, run_command
from .common import Which, check_version_tool


def run(runner: CommandRunner = run_command, which: Which = shutil.which) -> CheckResult:
    return check_version_tool(
        name="git",
        title="Git",
        commands=("git",),
        version_args=("--version",),
        missing_summary="git が見つかりません。",
        missing_next_steps=(
            "Git をインストールし、インストール後にターミナルを開き直してください。",
            "Windows では Git for Windows のインストールと PATH 設定を確認してください。",
        ),
        ok_summary_prefix="git が利用できます",
        runner=runner,
        which=which,
    )
