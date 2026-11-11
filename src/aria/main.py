"""ARIA command-line entry point."""
import argparse

from .config import Config
from .llm import OllamaClient
from .memory import MemoryStore
from .router import route_command


def main() -> None:
    parser = argparse.ArgumentParser(description="ARIA local AI assistant")
    parser.add_argument("--check", action="store_true", help="check Ollama connection")
    parser.add_argument("--no-memory", action="store_true", help="disable persistent chat history")
    parser.add_argument("--history", type=int, default=12, help="number of previous messages sent as context")
    args = parser.parse_args()
    client = OllamaClient(Config())
    memory = None if args.no_memory else MemoryStore()
    if args.check:
        print("Ollama:", "connected" if client.health() else "not reachable")
        print("Model:", client.config.ollama_model)
        return

    print("ARIA | Local AI Assistant (Ctrl+C to exit)")
    print("Conversation context:", "off" if memory is None else f"local memory ({args.history} messages)")
    print("Try natural commands: open Firefox, find ChatGPT, visit example.com")
    print("Slash commands: /voice | /voice-te | /voice-en | /help")
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
                        if memory and heard:
                            memory.add_message("user", heard)
                            if action:
                                memory.add_message("assistant", action.message)
                    except Exception as exc:
                        print("Voice error:", exc)
                    continue
                result = route_command(prompt[1:])
                print("\nARIA:", result.message)
                continue

            action = route_command(prompt)
            if action.handled:
                print("\nARIA:", action.message)
                if memory:
                    memory.add_message("user", prompt)
                    memory.add_message("assistant", action.message)
                continue
            if not client.health():
                print("Ollama is not reachable. Start Ollama and run aria --check.")
                continue
            history = memory.recent_messages(args.history) if memory and args.history > 0 else []
            reply = client.chat(prompt, history=history)
            print("\nARIA:", reply)
            if memory:
                memory.add_message("user", prompt)
                memory.add_message("assistant", reply)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as exc:
            print(f"ARIA error: {exc}")


if __name__ == "__main__":
    main()
