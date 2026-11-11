from pathlib import Path
from unittest.mock import patch
import pytest
from aria import windows_automation as wa


def test_windows_guard_on_non_windows():
    with patch.object(wa.sys, "platform", "linux"):
        with pytest.raises(OSError):
            wa.process_running("notepad.exe")


def test_installer_requires_approval_before_launch(tmp_path):
    installer=tmp_path/"setup.exe"
    installer.write_bytes(b"fake")
    with patch.object(wa.sys, "platform", "win32"):
        result=wa.run_installer(str(installer), approved=False)
    assert not result.success and "approval" in result.message.lower()


def test_installer_missing_path():
    with patch.object(wa.sys, "platform", "win32"):
        result=wa.run_installer("C:/missing/setup.exe", approved=True)
    assert not result.success and "not found" in result.message.lower()


def test_installed_executable_known_path(tmp_path):
    exe=tmp_path/"app.exe"
    exe.write_bytes(b"fake")
    with patch.object(wa.sys, "platform", "win32"):
        result=wa.installed_executable([str(exe)])
    assert result.success and result.value == str(exe.resolve())
