from __future__ import annotations

import platform
import shutil

from ..models import CheckResult, Status
from ..utils import CommandRunner, run_command
from .common import Which, check_version_tool


def _candidate_commands(platform_system: str) -> tuple[str, ...]:
    if platform_system.lower() == "windows":
        return ("codex.cmd", "codex.exe", "codex", "codex.ps1")
    return ("codex",)


def run(
    runner: CommandRunner = run_command,
    which: Which = shutil.which,
    platform_system: str | None = None,
) -> CheckResult:
    system = platform_system or platform.system()
    result = check_version_tool(
        name="codex",
        title="Codex CLI",
        commands=_candidate_commands(system),
        version_args=("--version",),
        missing_summary="Codex CLI が見つかりません。",
        missing_next_steps=(
            "Codex CLI を使う場合は、インストール先が PATH に入っているか確認してください。",
            "Windows では PowerShell の .ps1 shim より codex.cmd が安定する場合があります。",
        ),
        ok_summary_prefix="Codex CLI が利用できます",
        runner=runner,
        which=which,
    )
    if system.lower() == "windows" and result.status == Status.OK:
        command = next((item.value for item in result.evidence if item.label == "command"), "")
        if command.endswith(".ps1"):
            return CheckResult(
                name=result.name,
                title=result.title,
                status=Status.WARNING,
                summary="Codex CLI は見つかりましたが .ps1 shim が優先されています。",
                details=result.details
                + ("PowerShell の実行ポリシーによって .ps1 shim がブロックされる場合があります。",),
                next_steps=("PATH 上で codex.cmd が利用できるか確認してください。",),
                evidence=result.evidence,
            )
    return result
