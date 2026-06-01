from __future__ import annotations

import shutil
import sys

from ..models import CheckResult, Evidence, Status
from ..utils import CommandRunner, first_line, run_command
from .common import Which, find_first_command, read_version, version_text


def run(
    runner: CommandRunner = run_command,
    which: Which = shutil.which,
    version_info: tuple[int, int, int] | None = None,
    executable: str | None = None,
) -> CheckResult:
    current = version_info or (
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )
    current_executable = executable or sys.executable
    evidence = [
        Evidence("current_executable", current_executable),
        Evidence("current_version", ".".join(str(part) for part in current)),
    ]
    command_status = Status.OK
    command_details: tuple[str, ...] = ()
    command_next_steps: tuple[str, ...] = ("この項目は対応不要です。",)

    found = find_first_command(("python", "python3"), which)
    if found is not None:
        command_name, command_path = found
        result = read_version(command_path, ("--version",), runner=runner)
        evidence.extend((Evidence("command", command_name), Evidence("path", command_path)))
        if result.timed_out:
            command_status = Status.WARNING
            command_details = ("PATH 上の Python コマンドが 5秒以内に応答しませんでした。",)
            command_next_steps = ("別のターミナルで `python --version` を確認してください。",)
        elif result.returncode != 0:
            command_status = Status.WARNING
            command_details = (
                "PATH 上の Python コマンドのバージョン確認に失敗しました。",
                f"終了コード: {result.returncode}",
                first_line(result.stderr) or "stderr は空でした。",
            )
            command_next_steps = (
                "検出パスが壊れた shim や古いインストールでないか確認してください。",
            )
        else:
            command_version = version_text(result)
            evidence.append(Evidence("command_version", command_version))
            if not command_version:
                command_status = Status.WARNING
                command_details = ("Python コマンドのバージョン文字列が空でした。",)
                command_next_steps = ("別のターミナルで `python --version` を確認してください。",)

    if current < (3, 10, 0):
        return CheckResult(
            name="python",
            title="Python",
            status=Status.ERROR,
            summary="実行中の Python が 3.10 未満です。",
            details=("このツールは Python 3.10 以上を対象にしています。",),
            next_steps=("Python 3.10 以上の環境で実行してください。",),
            evidence=tuple(evidence),
        )

    details: tuple[str, ...] = ()
    if found is None:
        details = ("`python` または `python3` コマンドは PATH から見つかりませんでした。",)
        command_status = Status.WARNING
        command_next_steps = ("PATH の Python 設定を確認してください。",)
    elif command_details:
        details = command_details

    return CheckResult(
        name="python",
        title="Python",
        status=command_status,
        summary=f"実行中の Python は {current[0]}.{current[1]}.{current[2]} です。",
        details=details,
        next_steps=command_next_steps,
        evidence=tuple(evidence),
    )
