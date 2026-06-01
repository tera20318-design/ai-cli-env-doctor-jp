from __future__ import annotations

import os
import platform
from collections.abc import Callable, Mapping

from ..models import CheckResult, Evidence, Status


def _normalize(entry: str, case_insensitive: bool) -> str:
    normalized = os.path.normpath(entry.strip().strip('"'))
    return normalized.lower() if case_insensitive else normalized


def run(
    environ: Mapping[str, str] | None = None,
    is_dir: Callable[[str], bool] = os.path.isdir,
    platform_system: str | None = None,
) -> CheckResult:
    env = os.environ if environ is None else environ
    path_value = env.get("PATH") or env.get("Path") or ""
    if not path_value:
        return CheckResult(
            name="path",
            title="PATH",
            status=Status.ERROR,
            summary="PATH が空です。",
            next_steps=("ターミナルを開き直すか、OS の環境変数設定を確認してください。",),
        )

    entries = path_value.split(os.pathsep)
    empty_count = sum(1 for entry in entries if not entry.strip())
    system = platform_system or platform.system()
    case_insensitive = system.lower() == "windows"
    seen: set[str] = set()
    duplicate_count = 0
    missing_count = 0

    for entry in entries:
        stripped = entry.strip().strip('"')
        if not stripped:
            continue
        normalized = _normalize(stripped, case_insensitive)
        if normalized in seen:
            duplicate_count += 1
        else:
            seen.add(normalized)
        if not is_dir(stripped):
            missing_count += 1

    evidence = (
        Evidence("entry_count", str(len(entries))),
        Evidence("empty_entry_count", str(empty_count)),
        Evidence("duplicate_entry_count", str(duplicate_count)),
        Evidence("missing_directory_count", str(missing_count)),
    )

    if empty_count or duplicate_count or missing_count:
        return CheckResult(
            name="path",
            title="PATH",
            status=Status.WARNING,
            summary="PATH に整理した方がよい項目があります。",
            details=(
                f"空エントリ: {empty_count}",
                f"重複エントリ: {duplicate_count}",
                f"存在しないディレクトリ: {missing_count}",
            ),
            next_steps=(
                "まずは壊れているコマンドの検出パスを確認し、必要な PATH だけを残してください。",
                "このツールは PATH の内容を書き換えません。",
            ),
            evidence=evidence,
        )

    return CheckResult(
        name="path",
        title="PATH",
        status=Status.OK,
        summary="PATH の基本チェックは問題ありません。",
        next_steps=("この項目は対応不要です。",),
        evidence=evidence,
    )
