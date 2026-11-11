from aria.task_runner import Step, StepStatus, TaskRunner


def test_success_requires_execution_and_verification():
    calls=[]
    report=TaskRunner().run([Step("download",lambda: calls.append("run") or True,lambda: calls.append("verify") or True)])
    assert calls == ["run","verify"]
    assert report.succeeded and report.completed_count == 1
    assert report.steps[0].status == StepStatus.SUCCEEDED


def test_verification_failure_is_not_success():
    report=TaskRunner().run([Step("install",lambda: True,lambda: False),Step("launch",lambda: True,lambda: True)])
    assert not report.succeeded
    assert report.steps[0].status == StepStatus.FAILED
    assert report.steps[1].status == StepStatus.PENDING
    assert "verification" in report.steps[0].detail.lower()


def test_approval_gate_stops_before_execution():
    called=[]
    step=Step("installer",lambda: called.append(True) or True,lambda: True,requires_approval=True)
    report=TaskRunner().run([step],approve=lambda _:False)
    assert not called
    assert step.status == StepStatus.NEEDS_APPROVAL
    assert not report.succeeded


def test_exception_stops_pipeline():
    def explode(): raise RuntimeError("boom")
    report=TaskRunner().run([Step("first",explode,lambda:True),Step("second",lambda:True,lambda:True)])
    assert report.steps[0].status == StepStatus.FAILED
    assert report.steps[1].status == StepStatus.PENDING
