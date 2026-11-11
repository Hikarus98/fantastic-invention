# Conversational browser commands

ARIA recognizes a small set of explicit, safe phrases:

- `search for AI news`, `search AI news`, `find ChatGPT`, `look up Telugu AI jobs` — open a Google search.
- `go to example.com`, `visit example.com` — open a domain/HTTP(S) URL.
- `open a new tab` — ask the default browser to open a blank tab.
- `open Firefox`, `launch Notepad` — launch a registered application.

These are deterministic patterns, not unrestricted natural-language computer control. Unknown commands are rejected. Browser helpers use the system default browser; they do not yet manipulate an existing tab, click page elements, or type into arbitrary websites. Test locally with `pytest`.
