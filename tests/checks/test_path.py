from __future__ import annotations

import os

from ai_cli_env_doctor_jp.checks import path
from ai_cli_env_doctor_jp.models import Status


def test_path_ok() -> None:
    sep = os.pathsep
    existing = {"/bin", "/tools"}

    result = path.run(
        environ={"PATH": sep.join(["/bin", "/tools"])},
        is_dir=lambda value: value in existing,
        platform_system="Linux",
    )

    assert result.status == Status.OK


def test_path_warns_for_duplicate_missing_and_empty() -> None:
    sep = os.pathsep

    result = path.run(
        environ={"PATH": sep.join(["/Tools/Bin", "", "/tools/bin", "/missing"])},
        is_dir=lambda value: value.lower() == "/tools/bin",
        platform_system="Windows",
    )

    assert result.status == Status.WARNING
    assert "空エントリ: 1" in result.details
    assert "重複エントリ: 1" in result.details
    assert "存在しないディレクトリ: 1" in result.details


def test_path_allows_empty_environment_injection() -> None:
    result = path.run(environ={}, platform_system="Windows")

    assert result.status == Status.ERROR
