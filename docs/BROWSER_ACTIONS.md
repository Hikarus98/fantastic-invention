# ARIA Browser Actions

ARIA can open a validated URL or run a web search in the user's default browser.

- URL input accepts explicit HTTP(S) links or simple domain names.
- Search queries are URL-encoded and sent to Google Search.
- Browser navigation is performed by the default browser; ARIA does not inspect page contents.
- These are explicit commands; no arbitrary JavaScript or shell execution.

Python examples:
```python
from aria.browser_control import open_url, search_web
open_url("https://example.com")
search_web("local AI models")
```
