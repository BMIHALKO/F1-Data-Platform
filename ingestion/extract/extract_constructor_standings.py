"""
Extract constructor standings data from the Jolpica API.

This files retrieves constructor championship standings by season, flattens constructor fields, and returns records, ready for loading into staging.constructor_standings
"""

import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def flatten_constructor_standings(season, standing):
    constructor = standing.get("Constructor", {})

    return {
        "season": int(season),
        "standing_position": int(standing.get("position")),
        "position_text": standing.get("positionText"),
        "points": standing.get("points"),
        "wins": int(standing.get("wins")),
        "constructor_id": constructor.get("constructorId"),
    }

def extract_constructor_standings(season):
    url = f"{BASE_URL}/{season}/constructorStandings.json"
    params = {
        "limit": 100
    }

    response = requests.get(url, params = params, timeout = 30)

    if response.status_code == 429:
        raise RuntimeError(
            "Jolpica rate limit reached. Stop retrying and try again later."
        )
    
    response.raise_for_status()

    data = response.json()

    standings_list = (
        data.get("MRData", {})
        .get("StandingsTable", {})
        .get("StandingsLists", [])
    )

    if not standings_list:
        return []
    
    constructor_standings = standings_list[0].get("ConstructorStandings", [])

    return [
        flatten_constructor_standings(season, standing)
        for standing in constructor_standings
    ]

def extract_constructor_standings_for_seasons(seasons):
    all_standings = []

    for season in seasons:
        all_standings.extend(
            extract_constructor_standings(season)
        )
    
    return all_standings

if __name__ == "__main__":
    standings = extract_constructor_standings(2024)

    print(f"Extracted {len(standings)} constructor standings records")

    for record in standings[:3]:
        print(record)