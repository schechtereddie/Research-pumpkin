#!/usr/bin/env python3
import argparse
from pathlib import Path
from research_sources import fetch_wikipedia, fetch_arxiv, fetch_openalex, fetch_crossref
from render import render_markdown

def main():
    parser = argparse.ArgumentParser(description="Lightweight research gatherer that outputs a Markdown report.")
    parser.add_argument("topic", help="Research topic (quoted if spaced)")
    parser.add_argument("--limit", type=int, default=8, help="Max items per source")
    parser.add_argument("--outfile", default="report.md", help="Output Markdown file")
    args = parser.parse_args()

    topic = args.topic.strip()
    limit = max(1, args.limit)

    print(f"🔎 Researching: {topic!r}")

    wiki = fetch_wikipedia(topic)
    arxiv = fetch_arxiv(topic, limit=limit)
    openalex = fetch_openalex(topic, limit=limit)
    crossref = fetch_crossref(topic, limit=limit)

    report = render_markdown(topic, wiki, arxiv, openalex, crossref)
    Path(args.outfile).write_text(report, encoding="utf-8")

    print(f"✅ Wrote {args.outfile}")
    print("Tip: Open it in the Markdown preview (Ctrl/Cmd+Shift+V).")

if __name__ == "__main__":
    main()