from __future__ import annotations

import platform
import shutil

from ..models import CheckResult, Evidence, Status
from ..utils import CommandRunner, run_command
from .common import Which, find_first_command, read_version, version_text


def _npm_candidates(platform_system: str) -> tuple[str, ...]:
    if platform_system.lower() == "windows":
        return ("npm.cmd", "npm.exe", "npm", "npm.ps1")
    return ("npm",)


def _command_status(
    *,
    title: str,
    commands: tuple[str, ...],
    version_args: tuple[str, ...],
    runner: CommandRunner,
    which: Which,
) -> tuple[Status, tuple[Evidence, ...], str, tuple[str, ...]]:
    found = find_first_command(commands, which)
    if found is None:
        return Status.NOT_FOUND, (), f"{title} が見つかりません。", ()
    command_name, command_path = found
    result = read_version(command_path, version_args, runner=runner)
    evidence = (Evidence(f"{title}_command", command_name), Evidence(f"{title}_path", command_path))
    if result.timed_out:
        return Status.WARNING, evidence, f"{title} の確認がタイムアウトしました。", ()
    if result.returncode != 0:
        return (
            Status.ERROR,
            evidence,
            f"{title} のバージョン確認に失敗しました。",
            (f"終了コード: {result.returncode}",),
        )
    version = version_text(result)
    return Status.OK, (*evidence, Evidence(f"{title}_version", version)), f"{title}: {version}", ()


def run(
    runner: CommandRunner = run_command,
    which: Which = shutil.which,
    platform_system: str | None = None,
) -> CheckResult:
    system = platform_system or platform.system()
    node_status, node_evidence, node_summary, node_details = _command_status(
        title="node",
        commands=("node",),
        version_args=("--version",),
        runner=runner,
        which=which,
    )
    npm_status, npm_evidence, npm_summary, npm_details = _command_status(
        title="npm",
        commands=_npm_candidates(system),
        version_args=("--version",),
        runner=runner,
        which=which,
    )

    statuses = {node_status, npm_status}
    if Status.ERROR in statuses:
        status = Status.ERROR
        summary = "Node.js / npm の確認中にエラーがありました。"
    elif statuses == {Status.OK}:
        status = Status.OK
        summary = "Node.js と npm が利用できます。"
    elif Status.NOT_FOUND in statuses:
        status = Status.NOT_FOUND
        summary = "Node.js または npm が見つかりません。"
    else:
        status = Status.WARNING
        summary = "Node.js / npm の確認結果に警告があります。"

    details = (node_summary, npm_summary, *node_details, *npm_details)
    next_steps: tuple[str, ...]
    if status == Status.OK:
        next_steps = ("この項目は対応不要です。",)
    else:
        next_steps = (
            "Node.js を使う予定がある場合は、node と npm の PATH 設定を確認してください。",
            "Windows では npm.cmd を優先すると .ps1 実行ポリシー問題を避けやすいです。",
        )

    return CheckResult(
        name="node",
        title="Node.js / npm",
        status=status,
        summary=summary,
        details=details,
        next_steps=next_steps,
        evidence=(*node_evidence, *npm_evidence),
    )
