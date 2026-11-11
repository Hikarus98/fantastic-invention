# ARIA task execution and verification

`aria.task_runner.TaskRunner` executes a sequence of `Step` objects in order. Every step has an execution callback and a verification callback. A step is only `succeeded` if execution returns true **and** verification returns true. Exceptions, execution failures, and verification failures stop the pipeline; later steps remain pending.

## Approval boundary

Set `requires_approval=True` for installers, elevated actions, destructive changes, or other sensitive operations. Supply an `approve(step)` callback; without approval the step is marked `needs_approval` and is not executed. This module does not itself download software, elevate privileges, or invent verification signals. Integrations must implement trustworthy checks (e.g. file exists, expected executable exists, process is present) and must not treat a launch request as proof of successful installation or startup.

## Example

```python
from aria.task_runner import Step, TaskRunner

steps = [
    Step("download", download_installer, verify_download),
    Step("install", run_installer, verify_installed, requires_approval=True),
    Step("launch", launch_app, verify_process),
]
report = TaskRunner().run(steps, approve=lambda step: ask_user(step.name))
for step in report.steps:
    print(step.name, step.status.value, step.detail)
```

This is orchestration infrastructure, not a complete natural-language computer-use agent. The current ARIA CLI does not yet expose this runner as a general “do everything” command.
