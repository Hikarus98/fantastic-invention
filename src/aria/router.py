"""Command router for ARIA's safe desktop/browser actions."""
from __future__ import annotations
import re
from dataclasses import dataclass
from .actions import execute_action
from .browser_control import open_url, search_web

@dataclass(frozen=True)
class CommandResult:
    handled: bool
    success: bool
    message: str

_OPEN_PATTERNS=(
 re.compile(r"^(?:open|launch|start)\s+(.+?)$",re.I),
 re.compile(r"^open\s+(?:the\s+)?(.+?)\s+app$",re.I),
)
_SEARCH_PATTERNS=(
 re.compile(r"^(?:search(?:\s+the\s+web)?\s+for|google|search)\s+(.+)$",re.I),
 re.compile(r"^(?:find|look\s+up|look\s+for)\s+(.+)$",re.I),
)
_URL_PATTERN=re.compile(r"^(?:go\s+to|navigate\s+to|visit)\s+(.+)$",re.I)
_NEW_TAB_PATTERN=re.compile(r"^(?:open\s+)?(?:a\s+)?new\s+tab$",re.I)

def route_command(command: str) -> CommandResult:
 cleaned=command.strip().rstrip(".!?")
 if not cleaned: return CommandResult(False,False,"I didn't receive a command.")
 if cleaned.lower() in {"help","what can you do"}:
  return CommandResult(True,True,"Try: open Firefox/Notepad, search for AI news, find ChatGPT, go to example.com, or open a new tab.")
 if _NEW_TAB_PATTERN.match(cleaned):
  ok=open_url("about:blank")
  return CommandResult(True,ok,"Opened a blank tab." if ok else "Could not open a new tab.")
 for pattern in _SEARCH_PATTERNS:
  match=pattern.match(cleaned)
  if match:
   ok=search_web(match.group(1))
   return CommandResult(True,ok,"Opened a web search for: "+match.group(1) if ok else "Could not open browser search.")
 match=_URL_PATTERN.match(cleaned)
 if match:
  ok=open_url(match.group(1))
  return CommandResult(True,ok,"Opened the requested website." if ok else "That URL wasn't accepted or browser opening failed.")
 app=None
 for pattern in _OPEN_PATTERNS:
  m=pattern.match(cleaned)
  if m: app=m.group(1).strip().lower(); break
 if app is None: return CommandResult(False,False,"I don't recognize that command. Nothing was executed.")
 app=app.removeprefix("the ").removesuffix(" application")
 result=execute_action("open_application",name=app)
 return CommandResult(True,result.success,result.message)
