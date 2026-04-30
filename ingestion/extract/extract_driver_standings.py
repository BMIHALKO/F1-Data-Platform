"""
Extract driver standings data from the Jolpica API

This file retrieves driver championship standings by season, flatten driver and constructor fields, and returns records ready for loading into staging.driver_standings
"""

import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def to_int(value):
    return int(value) if value is not None else None

def flatten_driver_standings(season, standing):
    driver = standing.get("Driver", {})
    constructors = standing.get("Constructors", [])
    constructor = constructors[0] if constructors else {}

    return {
        "season": int(season),
        "standing_position": to_int(standing.get("position")),
        "position_text": standing.get("positionText"),
        "points": standing.get("points"),
        "wins": int(standing.get("wins")),
        "driver_id": driver.get("driverId"),
        "constructor_id": constructor.get("constructorId"),
    }

def extract_driver_standings(season):
    url = f"{BASE_URL}/{season}/driverStandings.json"
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
    
    driver_standings = standings_list[0].get("DriverStandings", [])

    return [
        flatten_driver_standings(season, standing)
        for standing in driver_standings
    ]

def extract_driver_standings_for_seasons(seasons):
    all_standings = []

    for season in seasons:
        all_standings.extend(extract_driver_standings(season))
    
    return all_standings

if __name__ == "__main__":
    standings = extract_driver_standings(2024)

    print(f"Extracted {len(standings)} driver standings records")

    for record in standings[:3]:
        print(record)