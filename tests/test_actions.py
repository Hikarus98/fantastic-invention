from unittest.mock import patch
from aria.actions import execute_action, open_application
from aria.windows_control import LaunchResult

def test_unknown_action_is_rejected():
    r=execute_action("run_shell",command="whoami")
    assert not r.success and not r.verified and "nothing executed" in r.message

@patch("aria.actions.launch_app",return_value=LaunchResult(True,"firefox","process detected",True))
def test_open_app_passes_verification(mock_launch):
    r=open_application("firefox")
    assert r.success and r.verified
    mock_launch.assert_called_once_with("firefox")

@patch("aria.actions.is_app_running",return_value=False)
def test_check_app_reports_not_detected(mock_check):
    r=execute_action("check_application",name="firefox")
    assert not r.success and not r.verified
