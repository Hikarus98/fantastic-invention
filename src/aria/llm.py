"""Ollama chat client."""
import requests
from .config import Config

class OllamaClient:
    def __init__(self, config: Config | None = None, timeout: int = 120):
        self.config = config or Config()
        self.timeout = timeout

    def chat(self, prompt: str, system: str = "You are ARIA, a helpful local AI assistant.") -> str:
        response = requests.post(self.config.ollama_url, json={"model": self.config.ollama_model, "stream": False, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False
