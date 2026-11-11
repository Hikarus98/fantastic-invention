from unittest.mock import patch

from aria.router import route_command
from aria.windows_control import LaunchResult


def test_help_is_handled():
    result = route_command("help")
    assert result.handled and result.success
    assert "Firefox" in result.message


def test_unknown_command_is_not_executed():
    result = route_command("delete all my files")
    assert not result.handled
    assert not result.success


@patch("aria.router.launch_app", return_value=LaunchResult(True, "firefox", "Launch request sent"))
def test_open_firefox_routes_to_launcher(mock_launch):
    result = route_command("Open Firefox")
    mock_launch.assert_called_once_with("firefox")
    assert result.handled and result.success


@patch("aria.router.launch_app", return_value=LaunchResult(False, "paint", "not allowed"))
def test_disallowed_app_fails_safely(mock_launch):
    result = route_command("open Paint")
    mock_launch.assert_called_once_with("paint")
    assert result.handled and not result.success
