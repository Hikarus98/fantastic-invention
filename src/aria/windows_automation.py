"""Explicit Windows automation primitives with safe defaults.

These helpers are Windows-only at runtime. They never run arbitrary shell text.
"""
from __future__ import annotations
import os
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

@dataclass(frozen=True)
class AutomationResult:
    success: bool
    message: str
    value: str | None = None


def _windows_only() -> None:
    if sys.platform != "win32":
        raise OSError("This action is available only on Windows.")


def download_file(url: str, destination: str, *, timeout: int = 60) -> AutomationResult:
    """Download HTTP(S) to a chosen path; reject non-web schemes and overwrite."""
    _windows_only()
    if not url.lower().startswith(("https://", "http://")):
        return AutomationResult(False, "Only HTTP(S) download URLs are accepted.")
    target = Path(destination).expanduser().resolve()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={"User-Agent": "ARIA-assistant/1.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response, target.open("wb") as out:
            while True:
                chunk = response.read(1024 * 128)
                if not chunk: break
                out.write(chunk)
        if not target.is_file() or target.stat().st_size == 0:
            return AutomationResult(False, "Download returned an empty or missing file.", str(target))
        return AutomationResult(True, f"Downloaded ({target.stat().st_size} bytes).", str(target))
    except Exception as exc:
        try: target.unlink(missing_ok=True)
        except Exception: pass
        return AutomationResult(False, f"Download failed: {exc}")


def launch_program(executable: str, args: Sequence[str] = (), *, wait_seconds: float = 2.0) -> AutomationResult:
    """Launch a specific executable path (not a shell command) and check process lifetime."""
    _windows_only()
    path = Path(executable).expanduser()
    if not path.is_file():
        return AutomationResult(False, f"Executable does not exist: {path}")
    try:
        proc = subprocess.Popen([str(path), *map(str, args)], shell=False)
        time.sleep(max(0.0, wait_seconds))
        code = proc.poll()
        if code is not None:
            return AutomationResult(False, f"Process exited quickly with code {code}.", str(proc.pid))
        return AutomationResult(True, "Process is still running after launch check.", str(proc.pid))
    except Exception as exc:
        return AutomationResult(False, f"Launch failed: {exc}")


def process_running(image_name: str) -> AutomationResult:
    """Check Windows process list for a basename using tasklist output."""
    _windows_only()
    name = Path(image_name).name.lower()
    if not name or name in {".", ".."}:
        return AutomationResult(False, "Provide a process image name.")
    try:
        result = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=15, check=True)
        running = any(line.lower().startswith('"' + name + '"') for line in result.stdout.splitlines())
        return AutomationResult(running, f"{name} {'is running' if running else 'was not found'}.", name)
    except Exception as exc:
        return AutomationResult(False, f"Process check failed: {exc}")


def installed_executable(paths: Sequence[str]) -> AutomationResult:
    """Check a finite list of known executable paths; no broad disk crawling."""
    _windows_only()
    for candidate in paths:
        p = Path(candidate).expanduser()
        if p.is_file():
            return AutomationResult(True, f"Found installed executable: {p}", str(p.resolve()))
    return AutomationResult(False, "No executable found in the supplied paths.")


def run_installer(installer: str, *, approved: bool = False, args: Sequence[str] = ()) -> AutomationResult:
    """Start installer only after explicit approval; do not silently elevate or auto-click UI."""
    _windows_only()
    if not approved:
        return AutomationResult(False, "Installer execution requires explicit user approval.")
    path = Path(installer).expanduser()
    if not path.is_file():
        return AutomationResult(False, f"Installer not found: {path}")
    try:
        proc = subprocess.Popen([str(path), *map(str, args)], shell=False)
        return AutomationResult(True, "Installer launched; completion must be checked separately.", str(proc.pid))
    except Exception as exc:
        return AutomationResult(False, f"Installer launch failed: {exc}")
