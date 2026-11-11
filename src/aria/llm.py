"""Ollama chat client with optional local conversation context."""
from __future__ import annotations

import requests
from .config import Config


class OllamaClient:
    def __init__(self, config: Config | None = None, timeout: int = 120):
        self.config = config or Config()
        self.timeout = timeout

    def chat(self, prompt: str, system: str = "You are ARIA, a helpful local AI assistant.",
             history: list[dict[str, str]] | None = None) -> str:
        messages = [{"role": "system", "content": system}]
        if history:
            for item in history:
                role, content = item.get("role"), item.get("content")
                if role in {"user", "assistant"} and isinstance(content, str):
                    messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": prompt})
        response = requests.post(
            self.config.ollama_url,
            json={"model": self.config.ollama_model, "stream": False, "messages": messages},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False
