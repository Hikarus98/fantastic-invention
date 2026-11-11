"""Small local SQLite memory store for ARIA conversations and user facts."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime, timezone


class MemoryStore:
    """Persistent, local-only memory. No network access or automatic data upload."""

    def __init__(self, path: str | Path = "data/aria_memory.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL CHECK(role IN ('user','assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )""")

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def add_message(self, role: str, content: str) -> int:
        if role not in {"user", "assistant"}:
            raise ValueError("role must be user or assistant")
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO messages(role,content,created_at) VALUES(?,?,?)",
                (role, content, self._now()),
            )
            return int(cursor.lastrowid)

    def recent_messages(self, limit: int = 20) -> list[dict[str, str]]:
        if limit < 1:
            return []
        with self._connect() as db:
            rows = db.execute(
                "SELECT role,content,created_at FROM messages ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def remember(self, key: str, value: str) -> None:
        key = key.strip()
        if not key or not value.strip():
            raise ValueError("key and value must not be empty")
        with self._connect() as db:
            db.execute("""INSERT INTO facts(key,value,updated_at) VALUES(?,?,?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value,
                updated_at=excluded.updated_at""", (key, value.strip(), self._now()))

    def recall(self, key: str) -> str | None:
        with self._connect() as db:
            row = db.execute("SELECT value FROM facts WHERE key=?", (key.strip(),)).fetchone()
        return row["value"] if row else None

    def all_facts(self) -> dict[str, str]:
        with self._connect() as db:
            rows = db.execute("SELECT key,value FROM facts ORDER BY key").fetchall()
        return {row["key"]: row["value"] for row in rows}

    def clear(self) -> None:
        """Delete all saved messages and facts."""
        with self._connect() as db:
            db.execute("DELETE FROM messages")
            db.execute("DELETE FROM facts")
