from __future__ import annotations

from collections.abc import Sequence

from ai_cli_env_doctor_jp.utils import CommandResult


class FakeWhich:
    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping
        self.calls: list[str] = []

    def __call__(self, name: str) -> str | None:
        self.calls.append(name)
        return self.mapping.get(name)


class QueueRunner:
    def __init__(self, responses: list[CommandResult]) -> None:
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, args: Sequence[str], timeout: float = 5.0) -> CommandResult:
        self.calls.append(tuple(args))
        if not self.responses:
            return CommandResult(tuple(args), 1, stderr="no fake response")
        return self.responses.pop(0)
