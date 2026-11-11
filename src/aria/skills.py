"""Explicit, local skill registry for ARIA (no dynamic code execution)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    handler: Callable[..., Any]


class SkillRegistry:
    """Register Python callables explicitly; invoke only known skill names."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, name: str, description: str, handler: Callable[..., Any]) -> None:
        key = name.strip().lower()
        if not key or not callable(handler):
            raise ValueError("skill name and callable handler are required")
        if key in self._skills:
            raise ValueError(f"skill already registered: {key}")
        self._skills[key] = Skill(key, description.strip(), handler)

    def list_skills(self) -> list[dict[str, str]]:
        return [
            {"name": skill.name, "description": skill.description}
            for skill in sorted(self._skills.values(), key=lambda item: item.name)
        ]

    def run(self, name: str, **kwargs: Any) -> Any:
        skill = self._skills.get(name.strip().lower())
        if skill is None:
            raise KeyError(f"unknown skill: {name}")
        return skill.handler(**kwargs)


def build_default_registry() -> SkillRegistry:
    """Return safe built-in skills that wrap existing registered actions."""
    from .actions import execute_action

    registry = SkillRegistry()
    registry.register(
        "open_app",
        "Open an allowlisted Windows application by its configured name.",
        lambda app_name: execute_action("open_application", name=app_name),
    )
    registry.register(
        "check_app",
        "Check whether a configured application process is running.",
        lambda app_name: execute_action("check_application", name=app_name),
    )
    return registry
