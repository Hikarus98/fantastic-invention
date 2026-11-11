"""Small command router for ARIA's first desktop-control milestone."""
from __future__ import annotations

import re
from dataclasses import dataclass
from .actions import execute_action


@dataclass(frozen=True)
class CommandResult:
    handled: bool
    success: bool
    message: str


_OPEN_PATTERNS = (
    re.compile(r"^(?:open|launch|start)\s+(.+?)$", re.IGNORECASE),
    re.compile(r"^open\s+(?:the\s+)?(.+?)\s+app$", re.IGNORECASE),
)


def route_command(command: str) -> CommandResult:
    """Route only known commands; everything else remains unexecuted."""
    cleaned = command.strip().rstrip(".!?")
    if not cleaned:
        return CommandResult(False, False, "I didn't receive a command.")

    if cleaned.lower() in {"help", "what can you do"}:
        return CommandResult(True, True, "Try: open Firefox, open Notepad, open Calculator, or open Explorer.")

    app = None
    for pattern in _OPEN_PATTERNS:
        match = pattern.match(cleaned)
        if match:
            app = match.group(1).strip().lower()
            break

    if app is None:
        return CommandResult(False, False, "I don't recognize that command. Nothing was executed.")

    # Normalize a few natural-language aliases.
    app = app.removeprefix("the ").removesuffix(" application")
    result = execute_action("open_application", name=app)
    return CommandResult(True, result.success, result.message)
