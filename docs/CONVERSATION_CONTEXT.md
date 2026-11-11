# ARIA conversation context

The CLI now stores user/assistant chat turns in the local SQLite memory and sends
a bounded recent history to Ollama on later chat prompts.

- Default: memory enabled, last 12 messages included.
- Disable: `aria --no-memory` (does not delete existing database).
- Change context window: `aria --history 20`.
- Data location: `data/aria_memory.sqlite3`.
- Memory is local; messages are sent to your configured Ollama server as context.
- Deterministic computer commands are still handled by the router, not sent to
  Ollama as executable instructions.

Only chat turns and voice utterances are logged in this CLI path; slash help and
other slash commands are not included. This is a simple recent-history window,
not semantic retrieval or automatic fact extraction.
