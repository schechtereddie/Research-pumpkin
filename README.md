# 🧪 Codespaces Researcher

Spin up a Codespace, run one command, get a Markdown research brief with citations
from **Wikipedia**, **arXiv**, **OpenAlex**, and **Crossref** — no API keys.

## Quick start (in a GitHub Codespace)

1. Click **Code → Codespaces → Create codespace on main**.
2. Wait for the devcontainer to finish (it auto-installs dependencies).
3. Run:

```bash
python app.py "quantum error correction" --limit 6 --outfile report.md
```

Then open `report.md` and use the Markdown preview (Ctrl/Cmd+Shift+V).

## Examples

```bash
python app.py "semaglutide weight loss"
python app.py "graph neural networks" --limit 5
python app.py "Seattle housing affordability" --outfile seattle-housing.md
```

## Notes
- No paid APIs. Wikipedia REST, arXiv Atom feed, OpenAlex, Crossref JSON.
- Output is Markdown so you can diff, review, or export to PDF in your editor.
- Results are best-effort; always fact-check before publishing externally.
