#!/usr/bin/env python3
"""
Debug probe: the site (calciotto.tv) runs on WordPress + SportsPress
(confirmed via the team page's body classes: sp_team, sportspress, ...).
SportsPress usually exposes REST API routes under /wp-json/sportspress/v2/.
This checks which routes exist and what a Treviso United team/player/event
looks like as JSON, so the real scraper can use the API instead of scraping
HTML tables.
"""
import json
import sys
import requests

BASE = "https://calciotto.tv"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; UnitedSiteBot/1.0)"}


def get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        return r.status_code, r
    except Exception as e:
        return None, str(e)


def show(label, url, max_chars=3000):
    print(f"\n=== {label}: {url} ===")
    status, r = get(url)
    if status is None:
        print(f"request failed: {r}")
        return None
    print(f"status: {status}")
    if status != 200:
        print(r.text[:500])
        return None
    ctype = r.headers.get("content-type", "")
    print(f"content-type: {ctype}")
    if "json" in ctype:
        try:
            data = r.json()
            text = json.dumps(data, indent=2, ensure_ascii=False)
            print(text[:max_chars])
            if len(text) > max_chars:
                print(f"... ({len(text)-max_chars} more chars)")
            return data
        except Exception as e:
            print(f"json parse failed: {e}")
            print(r.text[:max_chars])
    else:
        print(r.text[:max_chars])
    return None


def main():
    # Discover all registered REST routes
    routes_data = show("WP-JSON ROOT (route discovery)", f"{BASE}/wp-json/", max_chars=200)
    root_status, root_resp = get(f"{BASE}/wp-json/")
    if root_status == 200:
        try:
            full = root_resp.json()
            routes = list(full.get("routes", {}).keys())
            sp_routes = [r for r in routes if "sportspress" in r.lower() or "/sp" in r.lower()]
            print("\n=== SPORTSPRESS-RELATED ROUTES ===")
            for r in sp_routes:
                print(r)
        except Exception as e:
            print(f"route listing failed: {e}")

    # Common SportsPress v2 endpoints
    for slug in ["teams", "players", "staff", "events", "leagues", "tables", "venues", "seasons"]:
        show(f"SPORTSPRESS {slug.upper()} (list)", f"{BASE}/wp-json/sportspress/v2/{slug}?per_page=5")

    # Try to find Treviso United specifically
    show("SEARCH TEAM 'treviso-united-c8'", f"{BASE}/wp-json/sportspress/v2/teams?slug=treviso-united-c8")
    show("SEARCH TABLE for Serie A 2026-2027", f"{BASE}/wp-json/sportspress/v2/tables?search=Serie%20A")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
