"""User-editable ARIA personality and response preferences."""
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict, dataclass


@dataclass
class AssistantSettings:
    name: str = "ARIA"
    personality: str = "friendly, capable, calm, and proactive"
    response_style: str = "clear and concise"
    language: str = "match the user's language; support English and Telugu"
    system_prompt: str = ""

    def prompt(self) -> str:
        base = self.system_prompt.strip() or (
            f"You are {self.name}, a local AI assistant. Be {self.personality}. "
            f"Respond in a {self.response_style} way. {self.language}. "
            "Never claim to have performed an action unless a tool confirms it."
        )
        return base


class SettingsStore:
    def __init__(self, path: str | Path = "data/aria_settings.json"):
        self.path = Path(path)

    def load(self) -> AssistantSettings:
        if not self.path.exists():
            return AssistantSettings()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            allowed = AssistantSettings.__dataclass_fields__.keys()
            return AssistantSettings(**{k: v for k, v in raw.items() if k in allowed})
        except (OSError, json.JSONDecodeError, TypeError):
            return AssistantSettings()

    def save(self, settings: AssistantSettings) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(settings), indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
