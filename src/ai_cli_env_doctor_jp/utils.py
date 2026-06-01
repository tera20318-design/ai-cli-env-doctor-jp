from __future__ import annotations

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CommandResult:
    args: tuple[str, ...]
    returncode: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False


class CommandRunner(Protocol):
    def __call__(self, args: Sequence[str], timeout: float = 5.0) -> CommandResult:
        """Run a command and return captured output."""


def _clean_stream(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    return value.strip()


def run_command(args: Sequence[str], timeout: float = 5.0) -> CommandResult:
    try:
        completed = subprocess.run(
            list(args),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        return CommandResult(tuple(args), 127, stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            tuple(args),
            124,
            stdout=_clean_stream(exc.stdout),
            stderr=_clean_stream(exc.stderr) or "command timed out",
            timed_out=True,
        )
    return CommandResult(
        tuple(args),
        completed.returncode,
        stdout=_clean_stream(completed.stdout),
        stderr=_clean_stream(completed.stderr),
    )


def first_line(value: str) -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""
