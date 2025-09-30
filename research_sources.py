import requests
import feedparser
from datetime import datetime
from dateutil import parser as dtparse

USER_AGENT = "Codespaces-Researcher/1.0 (https://github.com/)"

def _get_json(url, params=None):
    r = requests.get(url, params=params or {}, headers={"User-Agent": USER_AGENT}, timeout=20)
    r.raise_for_status()
    return r.json()

def _get_text(url, params=None):
    r = requests.get(url, params=params or {}, headers={"User-Agent": USER_AGENT}, timeout=20)
    r.raise_for_status()
    return r.text

def fetch_wikipedia(topic: str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(topic)}"
    try:
        data = _get_json(url)
        if 'extract' in data:
            return {
                "title": data.get("title", topic),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                "summary": data.get("extract"),
                "last_updated": data.get("timestamp")
            }
    except Exception:
        pass
    return None

def fetch_arxiv(topic: str, limit=8):
    q = f"search_query=all:{requests.utils.quote(topic)}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
    url = f"http://export.arxiv.org/api/query?{q}"
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries:
        items.append({
            "title": e.get("title", "").strip(),
            "authors": [a.name for a in e.get("authors", [])],
            "summary": e.get("summary", "").strip(),
            "link": e.get("link"),
            "published": e.get("published")
        })
    return items

def fetch_openalex(topic: str, limit=8):
    url = "https://api.openalex.org/works"
    params = {
        "search": topic,
        "per_page": limit,
        "sort": "publication_year:desc,cited_by_count:desc"
    }
    data = _get_json(url, params=params)
    out = []
    for w in data.get("results", []):
        title = w.get("title")
        year = w.get("publication_year")
        cited = w.get("cited_by_count")
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        authors = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
        venue = (w.get("host_venue") or {}).get("display_name")
        best_url = w.get("primary_location", {}).get("source", {}).get("host_organization_name") or w.get("open_access", {}).get("oa_url") or w.get("doi_url") or w.get("primary_location", {}).get("landing_page_url")
        out.append({
            "title": title, "authors": authors, "venue": venue, "year": year,
            "cited_by_count": cited, "url": best_url or (("https://doi.org/" + doi) if doi else None)
        })
    return out

def fetch_crossref(topic: str, limit=8):
    url = "https://api.crossref.org/works"
    params = {"query": topic, "rows": limit, "sort": "published", "order": "desc"}
    try:
        data = _get_json(url, params=params)
    except Exception:
        return []
    items = []
    for it in data.get("message", {}).get("items", []):
        title = (it.get("title") or [""])[0]
        authors = []
        for a in it.get("author", []) or []:
            name = " ".join([x for x in [a.get("given"), a.get("family")] if x])
            if name:
                authors.append(name)
        cont = it.get("container-title", [""])[0]
        year = None
        for fld in ("published-print", "published-online", "issued"):
            if it.get(fld, {}).get("date-parts"):
                year = it[fld]["date-parts"][0][0]
                break
        doi = it.get("DOI")
        url2 = it.get("URL")
        items.append({
            "title": title, "authors": authors, "container": cont,
            "year": year, "doi": doi, "url": url2
        })
    return items