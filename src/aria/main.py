"""ARIA command-line entry point."""
import argparse
from .config import Config
from .llm import OllamaClient
from .router import route_command


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
    print("Commands: /open Firefox | /voice | /voice-te | /voice-en | /help")
    while True:
        try:
            prompt = input("\nYou: ").strip()
            if prompt.lower() in {"exit", "quit", "bye"}:
                break
            if not prompt:
                continue
            if prompt.startswith("/"):
                command = prompt[1:].strip().lower()
                if command in {"voice", "voice-te", "voice-en"}:
                    try:
                        from .voice import listen_and_route
                        language = {"voice-te": "te", "voice-en": "en"}.get(command)
                        heard, action = listen_and_route(language=language)
                        print("Heard:", heard or "(nothing recognized)")
                        if action is not None:
                            print("ARIA:", action.message)
                    except Exception as exc:
                        print("Voice error:", exc)
                    continue
                result = route_command(prompt[1:])
                print("\nARIA:", result.message)
                continue
            if not client.health():
                print("Ollama is not reachable. Start Ollama and run aria --check.")
                continue
            print("\nARIA:", client.chat(prompt))
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as exc:
            print(f"ARIA error: {exc}")


if __name__ == "__main__":
    main()
