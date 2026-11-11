"""Safe, allowlisted Windows application launching.

No arbitrary shell commands are accepted. This module is Windows-only at runtime.
"""
from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class LaunchResult:
    success: bool
    app: str
    message: str


# Deliberately limited to common, low-risk desktop applications.
APP_ALLOWLIST: dict[str, tuple[str, ...]] = {
    "notepad": ("notepad.exe",),
    "calculator": ("calc.exe",),
    "explorer": ("explorer.exe",),
    "firefox": ("firefox", "firefox.exe"),
    "chrome": ("chrome", "chrome.exe"),
}


def launch_app(app_name: str) -> LaunchResult:
    """Launch an allowlisted app without invoking a shell."""
    key = app_name.strip().lower()
    if key not in APP_ALLOWLIST:
        return LaunchResult(False, key, f"'{app_name}' is not in ARIA's allowed app list.")

    if platform.system() != "Windows":
        return LaunchResult(False, key, "Windows app launching is available only on Windows.")

    candidates = APP_ALLOWLIST[key]
    try:
        # Windows resolves installed apps from PATH/App Paths; shell=False is intentional.
        subprocess.Popen(candidates, shell=False)
        return LaunchResult(True, key, f"Launch request sent for {key}.")
    except (OSError, subprocess.SubprocessError) as exc:
        # Some apps (e.g. Firefox) may need their registered App Paths entry.
        try:
            os.startfile(candidates[0])  # type: ignore[attr-defined]
            return LaunchResult(True, key, f"Launch request sent for {key}.")
        except (AttributeError, OSError) as fallback_exc:
            return LaunchResult(False, key, f"Could not launch {key}: {fallback_exc or exc}")
