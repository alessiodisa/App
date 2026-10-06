#!/usr/bin/env python3
"""
Pulls data (standings, roster+stats, upcoming matches) for each team in
TEAMS below from the calciotto.tv SportsPress REST API and writes it to
assets/data/<team>.json for the Sport page to render.

Dirigenza/staff are NOT scraped — Treviso United's are curated by hand in
assets/js/treviso-staff.js, since calciotto.tv's own listing doesn't match
how those people actually work with the team.

Run on a schedule by .github/workflows/update-classifica.yml (GitHub's own
network — this can't be run from a sandboxed dev environment that blocks
calciotto.tv).

Notes on the API (learned by probing, since it isn't documented):
- The `teams=<id>` query param on /players is silently ignored by this
  site's REST setup — it just returns the default unfiltered page. So
  players are found by fully paginating /players and filtering
  client-side on `current_teams`.
- Per-player season stats live at statistics[str(league_id)][str(season_id)].
- A team's own `leagues` field is NOT reliable for finding its *current*
  league — it turns out to list every league the team has ever played in
  (same pitfall as `current_teams` on players), not just the current one.
  So each team's current league is instead found by scanning all `tables`
  for the one whose row data contains the team's id — that table's
  `leagues` field is the real current league. Falls back to
  FALLBACK_LEAGUE_SLUG (Treviso's known league) if no table contains the
  team. The season is a single site-wide value (SEASON_SLUG), not resolved
  per-team.
"""
import html
import json
import os
import sys
from datetime import datetime, timezone

import requests

BASE = "https://calciotto.tv/wp-json/sportspress/v2"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; UnitedHubSiteBot/1.0)"}
SEASON_SLUG = "2026-2027"
FALLBACK_LEAGUE_SLUG = "serie-a-2026-2027"

TEAMS = [
    {
        "slug": "treviso-united-c8",
        "name_search": "TREVISO UNITED",
        "out_path": "assets/data/treviso-united.json",
        "source": "https://calciotto.tv/classifica-serie-a-2026-2027/",
    },
    {
        "slug": "nova-united",
        "name_search": "NOVA UNITED",
        "out_path": "assets/data/nova-united.json",
        "source": "https://calciotto.tv/team/nova-united/",
    },
]

# A shared, keep-alive session avoids a fresh TCP+TLS handshake per request,
# which otherwise dominates latency when paginating through many pages.
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def clean_text(s):
    """Decode HTML entities WordPress leaves in rendered titles (e.g. &#8217;)."""
    return html.unescape(s) if isinstance(s, str) else s


def get(path, params=None):
    r = SESSION.get(f"{BASE}/{path}", params=params or {}, timeout=20)
    r.raise_for_status()
    return r.json()


def get_all(path, params=None, max_pages=100, log_progress=False):
    """Paginate through a collection endpoint."""
    items = []
    page = 1
    params = dict(params or {})
    params["per_page"] = 100
    while page <= max_pages:
        params["page"] = page
        r = SESSION.get(f"{BASE}/{path}", params=params, timeout=20)
        if r.status_code == 400:  # WP returns 400 once past the last page
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        total_pages = int(r.headers.get("X-WP-TotalPages", "1"))
        if log_progress:
            print(f"  {path}: page {page}/{total_pages} ({len(items)} items so far)", flush=True)
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


def find_team(slug, name_search):
    teams = get("teams", {"slug": slug})
    if teams:
        return teams[0]
    print(f"  slug '{slug}' not found directly, searching by name '{name_search}'...", flush=True)
    all_teams = get_all("teams", {"_fields": "id,slug,title"})
    for t in all_teams:
        title = clean_text((t.get("title") or {}).get("rendered", ""))
        if name_search.upper() in title.upper():
            return get(f"teams/{t['id']}")
    raise RuntimeError(f"team not found: slug={slug} name_search={name_search}")


def resolve_season():
    seasons = get("seasons", {"slug": SEASON_SLUG})
    if not seasons:
        raise RuntimeError(f"season not found: {SEASON_SLUG}")
    return seasons[0]["id"]


def find_team_league(team_id, all_tables):
    """Find the current league this team plays in by locating the table
    whose row data includes the team's id — reliable, unlike the team's own
    `leagues` field (see module docstring)."""
    for t in all_tables:
        data = t.get("data") or {}
        if str(team_id) in data:
            league_ids = t.get("leagues") or []
            if league_ids:
                return league_ids[0]
    print(f"  team {team_id} not found in any table, using fallback league '{FALLBACK_LEAGUE_SLUG}'", flush=True)
    leagues = get("leagues", {"slug": FALLBACK_LEAGUE_SLUG})
    if not leagues:
        raise RuntimeError(f"team {team_id} not found in any table, and fallback league not found")
    return leagues[0]["id"]


def scrape_team(team_cfg, all_players_slim, all_tables, season_id):
    slug = team_cfg["slug"]
    print(f"--- scraping {slug} ---", flush=True)
    team = find_team(slug, team_cfg["name_search"])
    team_id = team["id"]

    league_id = find_team_league(team_id, all_tables)
    print(f"  team_id={team_id} league_id={league_id} season_id={season_id}", flush=True)

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
            name = clean_text(row.get("name", ""))
            if isinstance(name, str) and name.isdigit():
                # data bug on their end: name field holds a raw team ID instead
                # of the team name. Resolve it via the teams endpoint.
                try:
                    resolved = get(f"teams/{name}")
                    name = clean_text(resolved.get("title", {}).get("rendered", name))
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
                "is_home_team": int(tid_str) == team_id if tid_str.isdigit() else False,
            })
        standings.sort(key=lambda r: (int(r["pos"]) if str(r["pos"]).isdigit() else 999))

    # --- Roster: filter the site-wide player list (passed in, fetched once
    # for all teams) client-side on `current_teams`. ---
    matching_ids = [p["id"] for p in all_players_slim if team_id in (p.get("current_teams") or [])]
    print(f"  found {len(matching_ids)} matching players, fetching full records...", flush=True)
    players_raw = []
    for pid in matching_ids:
        try:
            players_raw.append(get(f"players/{pid}"))
        except Exception:
            continue

    # `current_teams` turns out to reflect *ever* having been on this team
    # (whole club history), not this season's roster. The reliable signal is
    # whether the player has a stats record for the current league+season at
    # all — only actively-registered squad members get one (even a 0/0/0
    # one), so that's what actually narrows it down to the real roster.
    players = []
    for p in players_raw:
        class_list = p.get("class_list", [])
        position = class_value(class_list, "sp_position-")
        league_stats = (p.get("statistics") or {}).get(str(league_id), {})
        season_stats = league_stats.get(str(season_id)) if season_id else None
        if not season_stats:
            continue
        stats = {
            "appearances": season_stats.get("appearances", 0),
            "goals": season_stats.get("goals", 0),
            "yellow_cards": season_stats.get("yellowcards", 0),
            "red_cards": season_stats.get("redcards", 0),
            "motm": season_stats.get("manofthematch", 0),
        }
        players.append({
            "name": clean_text(p.get("title", {}).get("rendered", "")),
            "number": p.get("number") or None,
            "position": position,
            "position_label": POSITION_LABELS.get(position, position),
            "stats": stats,
        })

    position_order = {"goalkeeper": 0, "defender": 1, "midfielder": 2, "forward": 3}
    players.sort(key=lambda p: (position_order.get(p["position"], 9), p["name"]))

    # --- Upcoming matches ---
    events_raw = get_all("events", {"search": team_cfg["name_search"]})
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
        title = clean_text(e.get("title", {}).get("rendered", ""))
        opponent = title.replace(team_cfg["name_search"], "").replace(" vs ", "").strip()
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
        "source": team_cfg["source"],
        "team": {
            "name": clean_text(team.get("title", {}).get("rendered", team_cfg["name_search"])),
            "link": team.get("link"),
        },
        "standings": standings,
        "players": players,
        "upcoming_matches": upcoming,
    }

    out_path = team_cfg["out_path"]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  wrote {out_path}")
    print(f"  standings rows: {len(standings)}, players: {len(players)}, upcoming: {len(upcoming)}", flush=True)


def main():
    print("scanning players (shared across teams)...", flush=True)
    all_players_slim = get_all("players", {"_fields": "id,title,current_teams,class_list,number"}, log_progress=True)
    print(f"scanned {len(all_players_slim)} players total", flush=True)

    all_tables = get_all("tables")
    season_id = resolve_season()
    print(f"season_id={season_id}, {len(all_tables)} tables total", flush=True)

    failures = []
    for team_cfg in TEAMS:
        try:
            scrape_team(team_cfg, all_players_slim, all_tables, season_id)
        except Exception as e:
            print(f"ERROR scraping {team_cfg['slug']}: {e}", file=sys.stderr, flush=True)
            failures.append(team_cfg["slug"])

    if failures:
        print(f"WARNING: failed to scrape: {', '.join(failures)} (other teams still written)", file=sys.stderr, flush=True)
    if len(failures) == len(TEAMS):
        raise RuntimeError("all teams failed to scrape")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
