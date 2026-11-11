"""Environment-based ARIA configuration."""
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    whisper_model: str = os.getenv("WHISPER_MODEL", "small")
    whisper_device: str = os.getenv("WHISPER_DEVICE", "auto")
    whisper_compute_type: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
    sample_rate: int = int(os.getenv("SAMPLE_RATE", "16000"))

    @property
    def ollama_url(self) -> str:
        return f"{self.ollama_host}/api/chat"
