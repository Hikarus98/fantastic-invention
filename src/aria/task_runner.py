"""Sequential task runner with explicit execution and verification outcomes."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable

class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    NEEDS_APPROVAL = "needs_approval"
    SKIPPED = "skipped"

@dataclass
class Step:
    name: str
    execute: Callable[[], bool]
    verify: Callable[[], bool]
    requires_approval: bool = False
    status: StepStatus = StepStatus.PENDING
    detail: str = ""

@dataclass
class TaskReport:
    steps: list[Step] = field(default_factory=list)
    @property
    def succeeded(self) -> bool:
        return bool(self.steps) and all(s.status == StepStatus.SUCCEEDED for s in self.steps)
    @property
    def completed_count(self) -> int:
        return sum(s.status == StepStatus.SUCCEEDED for s in self.steps)

class TaskRunner:
    """Run steps in order; never mark success unless verification passes."""
    def run(self, steps: Iterable[Step], *, approve: Callable[[Step], bool] | None = None) -> TaskReport:
        report = TaskReport(list(steps))
        for step in report.steps:
            if step.requires_approval and (approve is None or not approve(step)):
                step.status = StepStatus.NEEDS_APPROVAL
                step.detail = "User approval is required; step was not executed."
                break
            step.status = StepStatus.RUNNING
            try:
                if not step.execute():
                    step.status = StepStatus.FAILED
                    step.detail = "Execution returned failure."
                    break
                if not step.verify():
                    step.status = StepStatus.FAILED
                    step.detail = "Execution was attempted, but verification failed."
                    break
                step.status = StepStatus.SUCCEEDED
                step.detail = "Executed and verified."
            except Exception as exc:
                step.status = StepStatus.FAILED
                step.detail = f"{type(exc).__name__}: {exc}"
                break
        return report
