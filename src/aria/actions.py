"""Controlled action registry for ARIA desktop actions."""
from dataclasses import dataclass
from .windows_control import launch_app, is_app_running

@dataclass(frozen=True)
class ActionOutcome:
    action: str
    success: bool
    verified: bool
    message: str

def open_application(name: str) -> ActionOutcome:
    r=launch_app(name)
    return ActionOutcome("open_application",r.success,r.verified,r.message)

def check_application(name: str) -> ActionOutcome:
    running=is_app_running(name)
    return ActionOutcome("check_application",running,running,f"{name} process is {'running' if running else 'not detected'}.")

ACTION_REGISTRY={"open_application":open_application,"check_application":check_application}

def execute_action(action_name: str, **kwargs) -> ActionOutcome:
    action=ACTION_REGISTRY.get(action_name)
    if action is None: return ActionOutcome(action_name,False,False,"Action is not registered; nothing executed.")
    try: return action(**kwargs)
    except TypeError as exc: return ActionOutcome(action_name,False,False,f"Invalid action arguments: {exc}")
