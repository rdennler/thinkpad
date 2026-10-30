# Plugins

Optional integrations. Each one is off until you set it up, and every skill that uses one declares it in `metadata.requires`.

| Plugin | Skills | Needs |
|---|---|---|
| Anki | `tp:anki` | Anki desktop with the AnkiConnect add-on. Docs: `anki/anki-readme.md`, `anki/anki-integration.md` |
| Claude in Chrome | `tp:reverse-engineer` (web targets) | The Claude-in-Chrome extension. Tool guidance: `../tool-guidance/claude-in-chrome.md` |
| Media tools | `tp:media` | `pdftotext` (poppler), `ffmpeg` |
