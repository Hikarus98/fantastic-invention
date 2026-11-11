"""Safe browser helpers: open URLs/searches through the user's default browser."""
from __future__ import annotations
import re
import webbrowser
from urllib.parse import quote_plus

_ALLOWED_SCHEMES=("http://","https://")

def normalize_url(value: str) -> str | None:
    text=value.strip()
    if not text: return None
    if re.match(r"^https?://",text,re.I):
        return text if text.lower().startswith(_ALLOWED_SCHEMES) else None
    # Only accept simple domain-like strings; do not interpret arbitrary text as a URL.
    if re.fullmatch(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?",text):
        return "https://"+text
    return None

def open_url(url: str) -> bool:
    normalized=normalize_url(url)
    return bool(normalized and webbrowser.open(normalized,new=2))

def search_web(query: str) -> bool:
    cleaned=query.strip()
    if not cleaned: return False
    return bool(webbrowser.open("https://www.google.com/search?q="+quote_plus(cleaned),new=2))
