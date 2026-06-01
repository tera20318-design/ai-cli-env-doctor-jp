from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Status(str, Enum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Evidence:
    label: str
    value: str

    def to_dict(self) -> dict[str, str]:
        return {"label": self.label, "value": self.value}


@dataclass(frozen=True)
class CheckResult:
    name: str
    title: str
    status: Status
    summary: str
    details: tuple[str, ...] = ()
    next_steps: tuple[str, ...] = ()
    evidence: tuple[Evidence, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "status": self.status.value,
            "summary": self.summary,
            "details": list(self.details),
            "next_steps": list(self.next_steps),
            "evidence": [item.to_dict() for item in self.evidence],
        }
