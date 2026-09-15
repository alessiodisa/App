#!/usr/bin/env python3
"""Debug: inspect team object keys + compare players?teams= filter vs full scan."""
import json
import requests

BASE = "https://calciotto.tv/wp-json/sportspress/v2"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; UnitedSiteBot/1.0)"}


def get(path, params=None):
    r = requests.get(f"{BASE}/{path}", headers=HEADERS, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    teams = get("teams", {"slug": "treviso-united-c8"})
    team = teams[0]
    print("=== TEAM KEYS ===")
    print(sorted(team.keys()))
    for k in ["players", "roster", "staff"]:
        if k in team:
            print(f"{k}: {team[k]}")

    print("\n=== players?teams=8310 (filtered) ===")
    filtered = get("players", {"teams": 8310, "per_page": 100})
    print(f"count: {len(filtered)}")
    for p in filtered:
        print(" ", p["title"]["rendered"], "current_teams=", p.get("current_teams"), "teams=", p.get("teams"))

    print("\n=== Full scan (first 3 pages, filter by current_teams contains 8310) ===")
    found = []
    for page in range(1, 4):
        batch = get("players", {"per_page": 100, "page": page})
        if not batch:
            break
        for p in batch:
            if 8310 in (p.get("current_teams") or []):
                found.append(p["title"]["rendered"])
    print(f"found on first 3 pages: {len(found)}")
    print(found)


if __name__ == "__main__":
    main()
