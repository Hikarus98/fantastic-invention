"""Safe, allowlisted Windows application launching and basic process verification."""
from __future__ import annotations
import os, platform, subprocess, time
from dataclasses import dataclass

@dataclass(frozen=True)
class LaunchResult:
    success: bool
    app: str
    message: str
    verified: bool = False

APP_ALLOWLIST = {
    "notepad": ("notepad.exe",), "calculator": ("calc.exe",),
    "explorer": ("explorer.exe",), "firefox": ("firefox", "firefox.exe"),
    "chrome": ("chrome", "chrome.exe"),
}
PROCESS_NAMES = {
    "notepad": ("notepad.exe",), "calculator": ("calculator.exe", "calc.exe"),
    "explorer": ("explorer.exe",), "firefox": ("firefox.exe",),
    "chrome": ("chrome.exe",),
}

def is_app_running(app_name: str) -> bool:
    key=app_name.strip().lower()
    if key not in PROCESS_NAMES or platform.system() != "Windows": return False
    try:
        out=subprocess.run(["tasklist","/FO","CSV","/NH"],capture_output=True,text=True,timeout=5,shell=False).stdout.lower()
        return any(n.lower() in out for n in PROCESS_NAMES[key])
    except (OSError,subprocess.SubprocessError): return False

def launch_app(app_name: str, verify_timeout: float=3.0) -> LaunchResult:
    key=app_name.strip().lower()
    if key not in APP_ALLOWLIST: return LaunchResult(False,key,f"'{app_name}' is not in ARIA's allowed app list.")
    if platform.system() != "Windows": return LaunchResult(False,key,"Windows app launching is available only on Windows.")
    try: subprocess.Popen(APP_ALLOWLIST[key],shell=False)
    except (OSError,subprocess.SubprocessError) as exc:
        try: os.startfile(APP_ALLOWLIST[key][0])
        except (AttributeError,OSError) as fallback: return LaunchResult(False,key,f"Could not launch {key}: {fallback or exc}")
    deadline=time.monotonic()+max(0.0,verify_timeout)
    while time.monotonic()<deadline:
        if is_app_running(key): return LaunchResult(True,key,f"{key} process detected (window readiness not verified).",True)
        time.sleep(.2)
    return LaunchResult(True,key,f"Launch request sent for {key}; process not detected yet.",False)
