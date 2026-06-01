from __future__ import annotations

import platform
import shutil

from ..models import CheckResult, Evidence, Status
from ..utils import CommandRunner, first_line, run_command
from .common import Which, find_first_command, read_version


def run(
    runner: CommandRunner = run_command,
    which: Which = shutil.which,
    platform_system: str | None = None,
) -> CheckResult:
    system = platform_system or platform.system()
    found = find_first_command(("pwsh", "powershell.exe", "powershell"), which)
    if found is None:
        return CheckResult(
            name="powershell",
            title="PowerShell",
            status=Status.NOT_FOUND if system.lower() == "windows" else Status.UNKNOWN,
            summary="PowerShell が見つかりません。",
            details=("Windows 以外では必須チェックではありません。",)
            if system.lower() != "windows"
            else (),
            next_steps=("Windows で PowerShell を使う場合はインストール状態を確認してください。",),
        )

    command_name, command_path = found
    policy = read_version(
        command_path,
        ("-NoProfile", "-Command", "Get-ExecutionPolicy"),
        runner=runner,
    )
    evidence: tuple[Evidence, ...] = (
        Evidence("command", command_name),
        Evidence("path", command_path),
    )
    if policy.timed_out:
        return CheckResult(
            name="powershell",
            title="PowerShell",
            status=Status.WARNING,
            summary="PowerShell は見つかりましたが、実行ポリシー確認がタイムアウトしました。",
            next_steps=("別のターミナルで `Get-ExecutionPolicy` を確認してください。",),
            evidence=evidence,
        )
    if policy.returncode != 0:
        return CheckResult(
            name="powershell",
            title="PowerShell",
            status=Status.WARNING,
            summary="PowerShell は見つかりましたが、実行ポリシーを確認できませんでした。",
            details=(first_line(policy.stderr) or "stderr は空でした。",),
            next_steps=("PowerShell を直接開いて `Get-ExecutionPolicy` を確認してください。",),
            evidence=evidence,
        )

    policy_text = first_line(policy.stdout)
    evidence = (*evidence, Evidence("execution_policy", policy_text))
    risky = {"restricted", "allsigned"}
    if policy_text.lower() in risky:
        return CheckResult(
            name="powershell",
            title="PowerShell",
            status=Status.WARNING,
            summary=f"PowerShell の実行ポリシーは {policy_text} です。",
            details=(".ps1 shim がブロックされる可能性があります。",),
            next_steps=(
                "npm や Codex は .ps1 ではなく .cmd shim で実行できるか確認してください。",
                "実行ポリシーを変更する前に、組織や端末のセキュリティ方針を確認してください。",
            ),
            evidence=evidence,
        )

    return CheckResult(
        name="powershell",
        title="PowerShell",
        status=Status.OK,
        summary=f"PowerShell が利用できます。実行ポリシー: {policy_text or '不明'}",
        next_steps=("この項目は対応不要です。",),
        evidence=evidence,
    )
