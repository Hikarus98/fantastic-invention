# Local intent routing (current behavior)

The CLI now attempts the deterministic command router before sending plain text to Ollama.

1. A recognized allowlisted phrase (open an approved app, search/find/look up, visit/go to a URL, open a new tab) is handled as an action.
2. Unrecognized input is treated as a normal chat message and sent to the configured local Ollama model.
3. Slash-prefixed commands remain supported, including one-shot voice modes.

Safety boundary: Ollama is not currently allowed to invent or execute OS actions. The command router only executes its explicit patterns and action registry. This is intentionally conservative. A future natural-language planner can propose structured intents, but proposals must be validated against the same registry before execution.
