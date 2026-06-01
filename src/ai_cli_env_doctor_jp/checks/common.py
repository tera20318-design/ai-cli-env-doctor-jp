from __future__ import annotations

from collections.abc import Callable, Sequence

from ..models import CheckResult, Evidence, Status
from ..utils import CommandResult, CommandRunner, first_line, run_command

Which = Callable[[str], str | None]


def find_first_command(names: Sequence[str], which: Which) -> tuple[str, str] | None:
    for name in names:
        path = which(name)
        if path:
            return name, path
    return None


def read_version(
    command: str,
    args: Sequence[str],
    runner: CommandRunner = run_command,
    timeout: float = 5.0,
) -> CommandResult:
    return runner([command, *args], timeout=timeout)


def version_text(result: CommandResult) -> str:
    return first_line(result.stdout) or first_line(result.stderr)


def check_version_tool(
    *,
    name: str,
    title: str,
    commands: Sequence[str],
    version_args: Sequence[str],
    missing_summary: str,
    missing_next_steps: Sequence[str],
    ok_summary_prefix: str,
    runner: CommandRunner = run_command,
    which: Which,
) -> CheckResult:
    found = find_first_command(commands, which)
    if found is None:
        return CheckResult(
            name=name,
            title=title,
            status=Status.NOT_FOUND,
            summary=missing_summary,
            next_steps=tuple(missing_next_steps),
        )

    command_name, command_path = found
    result = read_version(command_path, version_args, runner=runner)
    evidence = (
        Evidence("command", command_name),
        Evidence("path", command_path),
    )

    if result.timed_out:
        return CheckResult(
            name=name,
            title=title,
            status=Status.WARNING,
            summary=f"{title} のバージョン確認がタイムアウトしました。",
            details=("コマンドは見つかりましたが、5秒以内に応答しませんでした。",),
            next_steps=(
                "インストールが壊れていないか、別のターミナルで同じコマンドを確認してください。",
            ),
            evidence=evidence,
        )

    if result.returncode != 0:
        stderr = first_line(result.stderr)
        return CheckResult(
            name=name,
            title=title,
            status=Status.ERROR,
            summary=f"{title} は見つかりましたが、バージョン確認に失敗しました。",
            details=(f"終了コード: {result.returncode}", stderr or "stderr は空でした。"),
            next_steps=(
                "検出パスの実体が古い shim や壊れたインストールでないか確認してください。",
            ),
            evidence=evidence,
        )

    version = version_text(result)
    if not version:
        return CheckResult(
            name=name,
            title=title,
            status=Status.WARNING,
            summary=f"{title} は見つかりましたが、バージョン文字列を取得できませんでした。",
            details=("コマンドは終了コード 0 を返しましたが、stdout/stderr が空でした。",),
            next_steps=(
                "壊れた shim や想定外のラッパーではないか、"
                "別のターミナルで同じコマンドを確認してください。",
            ),
            evidence=evidence,
        )
    return CheckResult(
        name=name,
        title=title,
        status=Status.OK,
        summary=f"{ok_summary_prefix}: {version}",
        next_steps=("この項目は対応不要です。",),
        evidence=(*evidence, Evidence("version", version or "")),
    )
