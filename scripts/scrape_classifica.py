#!/usr/bin/env python3
"""
Debug probe: fetches the calciotto.tv Serie A standings page and prints its
structure (tables, headings, links mentioning "treviso") so the real scraper
selectors can be written against the actual markup. Run via GitHub Actions,
where the network isn't blocked (unlike the sandboxed dev environment this
was authored in).
"""
import sys
import requests
from bs4 import BeautifulSoup

URL = "https://calciotto.tv/classifica-serie-a-2026-2027/"

def main():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; UnitedSiteBot/1.0)"}, timeout=30)
    print(f"status: {resp.status_code}")
    print(f"final url: {resp.url}")
    print(f"content-length: {len(resp.text)}")

    soup = BeautifulSoup(resp.text, "html.parser")

    print("\n=== TITLE ===")
    print(soup.title.string if soup.title else "(none)")

    print("\n=== TABLES ===")
    tables = soup.find_all("table")
    print(f"found {len(tables)} <table> elements")
    for i, t in enumerate(tables):
        rows = t.find_all("tr")
        print(f"\n--- table {i} ({len(rows)} rows) ---")
        for r in rows[:5]:
            cells = [c.get_text(strip=True) for c in r.find_all(["td", "th"])]
            print(cells)
        if len(rows) > 5:
            print(f"... ({len(rows)-5} more rows)")

    print("\n=== LINKS MENTIONING 'treviso' ===")
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if "treviso" in text.lower() or "treviso" in href.lower():
            print(f"{text!r} -> {href}")

    print("\n=== HEADINGS ===")
    for h in soup.find_all(["h1", "h2", "h3"]):
        print(f"{h.name}: {h.get_text(strip=True)}")

    print("\n=== ELEMENTS WITH CLASS CONTAINING 'classifica' OR 'standing' ===")
    for el in soup.find_all(class_=True):
        classes = " ".join(el.get("class", []))
        if "classifica" in classes.lower() or "standing" in classes.lower() or "table" in classes.lower():
            print(f"<{el.name} class='{classes}'> first 100 chars: {el.get_text(strip=True)[:100]!r}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
