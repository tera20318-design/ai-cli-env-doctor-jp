from __future__ import annotations

import shutil

from ..models import CheckResult
from ..utils import CommandRunner, run_command
from .common import Which, check_version_tool


def run(runner: CommandRunner = run_command, which: Which = shutil.which) -> CheckResult:
    return check_version_tool(
        name="uv",
        title="uv",
        commands=("uv",),
        version_args=("--version",),
        missing_summary="uv が見つかりません。",
        missing_next_steps=(
            "uv を使う予定がある場合は、公式手順でインストールしてください。",
            "このツールは uv を必須とはしません。使っていない場合は無視できます。",
        ),
        ok_summary_prefix="uv が利用できます",
        runner=runner,
        which=which,
    )
