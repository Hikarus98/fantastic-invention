"""ARIA command-line entry point."""
import argparse
from .config import Config
from .llm import OllamaClient

def main() -> None:
    parser = argparse.ArgumentParser(description="ARIA local AI assistant")
    parser.add_argument("--check", action="store_true", help="check Ollama connection")
    args = parser.parse_args()
    client = OllamaClient(Config())
    if args.check:
        print("Ollama:", "connected" if client.health() else "not reachable")
        print("Model:", client.config.ollama_model)
        return
    print("ARIA | Local AI Assistant (Ctrl+C to exit)")
    if not client.health():
        print("Ollama is not reachable. Start Ollama and run aria --check.")
        return
    while True:
        try:
            prompt = input("\nYou: ").strip()
            if prompt.lower() in {"exit", "quit", "bye"}:
                break
            if prompt:
                print("\nARIA:", client.chat(prompt))
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as exc:
            print(f"ARIA error: {exc}")
