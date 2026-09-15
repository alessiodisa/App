#!/usr/bin/env python3
"""
Pulls Treviso United's current data (standings, roster+stats, staff,
upcoming matches) from the calciotto.tv SportsPress REST API and writes it
to assets/data/treviso-united.json for the Sport page to render.

Run on a schedule by .github/workflows/update-classifica.yml (GitHub's own
network — this can't be run from a sandboxed dev environment that blocks
calciotto.tv).

Notes on the API (learned by probing, since it isn't documented):
- The `teams=<id>` query param on /players and /staff is silently ignored
  by this site's REST setup — it just returns the default unfiltered page.
  So players are found by fully paginating /players and filtering
  client-side on `current_teams`. Staff has a shortcut: the team object
  itself exposes a `staff` field with the exact IDs to fetch.
- Per-player season stats live at statistics[str(league_id)][str(season_id)].
"""
import json
import os
import sys
from datetime import datetime, timezone

import requests

BASE = "https://calciotto.tv/wp-json/sportspress/v2"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; UnitedSiteBot/1.0)"}
TEAM_SLUG = "treviso-united-c8"
LEAGUE_SLUG = "serie-a-2026-2027"
SEASON_SLUG = "2026-2027"
OUT_PATH = "assets/data/treviso-united.json"


def get(path, params=None):
    r = requests.get(f"{BASE}/{path}", headers=HEADERS, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def get_all(path, params=None, max_pages=100):
    """Paginate through a collection endpoint."""
    items = []
    page = 1
    params = dict(params or {})
    params["per_page"] = 100
    while page <= max_pages:
        params["page"] = page
        r = requests.get(f"{BASE}/{path}", headers=HEADERS, params=params, timeout=30)
        if r.status_code == 400:  # WP returns 400 once past the last page
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        total_pages = int(r.headers.get("X-WP-TotalPages", "1"))
        if page >= total_pages:
            break
        page += 1
    return items


def class_value(class_list, prefix):
    """Extract e.g. 'forward' from 'sp_position-forward' in a class_list."""
    for c in class_list:
        if c.startswith(prefix):
            return c[len(prefix):]
    return None


POSITION_LABELS = {
    "goalkeeper": "Portiere",
    "defender": "Difensore",
    "midfielder": "Centrocampista",
    "forward": "Attaccante",
}

ROLE_LABELS = {
    "dirigente": "Dirigente",
    "allenatore": "Allenatore",
    "presidente": "Presidente",
    "capitano": "Capitano",
    "vice-presidente": "Vicepresidente",
    "direttore-sportivo": "Direttore Sportivo",
    "collaboratore-tecnico": "Collaboratore Tecnico",
}


def main():
    # --- League + season + team lookup ---
    leagues = get("leagues", {"slug": LEAGUE_SLUG})
    if not leagues:
        raise RuntimeError(f"league not found: {LEAGUE_SLUG}")
    league_id = leagues[0]["id"]

    seasons = get("seasons", {"slug": SEASON_SLUG})
    season_id = seasons[0]["id"] if seasons else None

    teams = get("teams", {"slug": TEAM_SLUG})
    if not teams:
        raise RuntimeError(f"team not found: {TEAM_SLUG}")
    team = teams[0]
    team_id = team["id"]

    # --- Standings table for the league ---
    tables = get("tables", {"leagues": league_id})
    table = None
    for t in tables:
        if league_id in (t.get("leagues") or []):
            table = t
            break
    if table is None and tables:
        table = tables[0]

    standings = []
    if table:
        for tid_str, row in table.get("data", {}).items():
            name = row.get("name", "")
            if isinstance(name, str) and name.isdigit():
                # data bug on their end: name field holds a raw team ID instead
                # of the team name. Resolve it via the teams endpoint.
                try:
                    resolved = get(f"teams/{name}")
                    name = resolved.get("title", {}).get("rendered", name)
                except Exception:
                    pass
            standings.append({
                "team_id": int(tid_str) if tid_str.isdigit() else tid_str,
                "pos": row.get("pos"),
                "name": name,
                "pts": row.get("pts"),
                "played": row.get("p"),
                "wins": row.get("w"),
                "draws": row.get("d"),
                "losses": row.get("l"),
                "for": row.get("f"),
                "against": row.get("a"),
                "gd": row.get("gd"),
                "is_treviso_united": int(tid_str) == team_id if tid_str.isdigit() else False,
            })
        standings.sort(key=lambda r: (int(r["pos"]) if str(r["pos"]).isdigit() else 999))

    # --- Roster: the `teams=` REST filter is broken (returns unfiltered
    # results), so scan the full players collection and filter client-side.
    all_players = get_all("players")
    players_raw = [p for p in all_players if team_id in (p.get("current_teams") or [])]

    players = []
    for p in players_raw:
        class_list = p.get("class_list", [])
        position = class_value(class_list, "sp_position-")
        stats = {}
        league_stats = (p.get("statistics") or {}).get(str(league_id), {})
        season_stats = league_stats.get(str(season_id)) if season_id else None
        if season_stats:
            stats = {
                "appearances": season_stats.get("appearances", 0),
                "goals": season_stats.get("goals", 0),
                "yellow_cards": season_stats.get("yellowcards", 0),
                "red_cards": season_stats.get("redcards", 0),
                "motm": season_stats.get("manofthematch", 0),
            }
        players.append({
            "name": p.get("title", {}).get("rendered", ""),
            "number": p.get("number") or None,
            "position": position,
            "position_label": POSITION_LABELS.get(position, position),
            "stats": stats,
        })

    position_order = {"goalkeeper": 0, "defender": 1, "midfielder": 2, "forward": 3}
    players.sort(key=lambda p: (position_order.get(p["position"], 9), p["name"]))

    # --- Staff / dirigenza: the team object gives the exact IDs directly. ---
    staff = []
    for staff_id in team.get("staff", []):
        try:
            s = get(f"staff/{staff_id}")
        except Exception:
            continue
        class_list = s.get("class_list", [])
        role = class_value(class_list, "sp_role-")
        staff.append({
            "name": s.get("title", {}).get("rendered", ""),
            "role": role,
            "role_label": ROLE_LABELS.get(role, (role or "").replace("-", " ").title()),
        })

    # --- Upcoming matches ---
    events_raw = get_all("events", {"search": "TREVISO UNITED"})
    now = datetime.now(timezone.utc)
    upcoming = []
    for e in events_raw:
        if team_id not in (e.get("teams") or []):
            continue
        try:
            event_dt = datetime.fromisoformat(e["date_gmt"]).replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if event_dt < now:
            continue
        title = e.get("title", {}).get("rendered", "")
        opponent = title.replace("TREVISO UNITED", "").replace(" vs ", "").strip()
        class_list = e.get("class_list", [])
        league_slug = class_value(class_list, "sp_league-")
        upcoming.append({
            "date": e["date_gmt"],
            "title": title,
            "opponent": opponent,
            "league": league_slug,
        })
    upcoming.sort(key=lambda m: m["date"])
    upcoming = upcoming[:6]

    output = {
        "generated_at": now.isoformat(),
        "source": "https://calciotto.tv/classifica-serie-a-2026-2027/",
        "team": {
            "name": team.get("title", {}).get("rendered", "TREVISO UNITED"),
            "link": team.get("link"),
        },
        "standings": standings,
        "players": players,
        "staff": staff,
        "upcoming_matches": upcoming,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"wrote {OUT_PATH}")
    print(f"standings rows: {len(standings)}, players: {len(players)} (scanned {len(all_players)} total), staff: {len(staff)}, upcoming: {len(upcoming)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
