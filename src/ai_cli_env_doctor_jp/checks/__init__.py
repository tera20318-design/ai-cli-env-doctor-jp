from __future__ import annotations

from collections.abc import Callable

from ..models import CheckResult
from . import codex, git, node, path, powershell, python, uv

CheckFunction = Callable[[], CheckResult]

CHECKS: dict[str, CheckFunction] = {
    "git": git.run,
    "python": python.run,
    "node": node.run,
    "uv": uv.run,
    "codex": codex.run,
    "powershell": powershell.run,
    "path": path.run,
}

DEFAULT_CHECKS: tuple[str, ...] = ("python", "git", "node", "uv", "codex", "powershell", "path")
