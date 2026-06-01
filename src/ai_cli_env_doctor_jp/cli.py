from __future__ import annotations

import argparse
from collections.abc import Iterable, Mapping, Sequence

from . import __version__
from .checks import CHECKS, DEFAULT_CHECKS, CheckFunction
from .models import CheckResult
from .report import render_json, render_text, should_fail_strict


def build_parser(check_names: Iterable[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-cli-env-doctor-jp",
        description="AI/CLI 開発環境のよくある詰まりどころを日本語で診断します。",
    )
    parser.add_argument(
        "--check",
        action="append",
        choices=sorted(check_names),
        help="実行するチェックを指定します。複数回指定できます。未指定なら全チェックを実行します。",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="診断結果を JSON で出力します。",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="警告、エラー、未検出がある場合に終了コード 1 を返します。",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def run_selected_checks(
    selected: Sequence[str] | None,
    registry: Mapping[str, CheckFunction] | None = None,
) -> list[CheckResult]:
    checks = registry or CHECKS
    names = tuple(selected) if selected else DEFAULT_CHECKS
    return [checks[name]() for name in names]


def main(
    argv: Sequence[str] | None = None,
    registry: Mapping[str, CheckFunction] | None = None,
) -> int:
    checks = registry or CHECKS
    parser = build_parser(checks.keys())
    args = parser.parse_args(argv)
    selected = tuple(args.check) if args.check else None
    results = run_selected_checks(selected, registry=checks)
    if args.json_output:
        print(render_json(results), end="")
    else:
        print(render_text(results), end="")
    if args.strict and should_fail_strict(results):
        return 1
    return 0
