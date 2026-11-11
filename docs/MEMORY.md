# ARIA local memory

ARIA now has a local SQLite memory store in `src/aria/memory.py`.

## Usage

```python
from aria.memory import MemoryStore

memory = MemoryStore()  # data/aria_memory.sqlite3
memory.add_message("user", "Hello")
memory.add_message("assistant", "Hi!")
memory.remember("preferred_name", "Rishith")
print(memory.recall("preferred_name"))
print(memory.recent_messages(limit=10))
```

## Privacy and behavior

- SQLite file stays on this computer unless you manually copy/share it.
- Conversation logging is **not automatically enabled** in the CLI yet.
- Facts are explicitly stored by calling `remember`; ARIA does not infer/save them.
- Call `clear()` to delete all stored messages and facts.
- Avoid saving passwords, API keys, financial credentials, or sensitive personal data.
- This is persistence infrastructure, not yet automatic context injection into Ollama.
