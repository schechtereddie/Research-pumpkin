from datetime import datetime
from textwrap import indent

def _fmt_authors(authors):
    if not authors:
        return "—"
    if isinstance(authors, str):
        return authors
    return ", ".join(authors[:8]) + (" et al." if len(authors) > 8 else "")

def render_markdown(topic, wiki, arxiv, openalex, crossref):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"# Research Brief: {topic}")
    lines.append("")
    lines.append(f"_Generated {now}_")
    lines.append("---")

    if wiki:
        lines.append("## Executive Summary (Wikipedia)")
        lines.append("")
        lines.append(wiki["summary"].strip())
        if wiki.get("url"):
            lines.append(f"\n**Source:** {wiki['url']}")
        lines.append("")

    if arxiv:
        lines.append("## Recent arXiv Papers")
        for i, p in enumerate(arxiv, 1):
            lines.append(f"**{i}. {p['title']}**")
            lines.append(f"- Authors: {_fmt_authors(p['authors'])}")
            if p.get("published"):
                lines.append(f"- Published: {p['published']}")
            if p.get("link"):
                lines.append(f"- Link: {p['link']}")
            if p.get("summary"):
                lines.append("\n" + indent(p["summary"].strip(), "  "))
            lines.append("")
    if openalex:
        lines.append("## OpenAlex Highlights")
        for i, w in enumerate(openalex, 1):
            lines.append(f"**{i}. {w['title']}**")
            lines.append(f"- Authors: {_fmt_authors(w['authors'])}")
            meta = []
            if w.get("venue"): meta.append(w["venue"])
            if w.get("year"): meta.append(str(w["year"]))
            if meta:
                lines.append(f"- Venue/Year: {', '.join(meta)}")
            if w.get("cited_by_count") is not None:
                lines.append(f"- Citations: {w['cited_by_count']}")
            if w.get("url"):
                lines.append(f"- Link: {w['url']}")
            lines.append("")
    if crossref:
        lines.append("## Crossref (Recently Published)")
        for i, c in enumerate(crossref, 1):
            lines.append(f"**{i}. {c['title']}**")
            lines.append(f"- Authors: {_fmt_authors(c['authors'])}")
            meta = []
            if c.get("container"): meta.append(c["container"])
            if c.get("year"): meta.append(str(c["year"]))
            if meta:
                lines.append(f"- Journal/Year: {', '.join(meta)}")
            if c.get("doi"): lines.append(f"- DOI: https://doi.org/{c['doi']}")
            if c.get("url"): lines.append(f"- Link: {c['url']}")
            lines.append("")

    lines.append("---")
    lines.append("_Note: This is an automated brief. Verify critical claims before citing._")
    return "\n".join(lines)