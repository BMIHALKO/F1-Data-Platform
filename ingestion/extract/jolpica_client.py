import requests
import time

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def fetch_endpoint(endpoint: str) -> dict:
    """
    Fetch JSON data from a Jolpica F1 API endpoint.
    Supports query strings like: seasons?limit=100&offset=30
    """
    if "?" in endpoint:
        path, query = endpoint.split("?", 1)
        url = f"{BASE_URL}/{path}.json?{query}"
    else:
        url = f"{BASE_URL}/{endpoint}.json"

    max_retries = 3

    for attempt in range(max_retries):
        response = requests.get(url, timeout=30)

        if response.status_code == 429:
            wait_seconds = 10 * (attempt + 1)
            print(f"Rate limited. Waiting {wait_seconds} seconds before retrying...")
            time.sleep(wait_seconds)
            continue

        response.raise_for_status()
        return response.json()

    response.raise_for_status()

def get_available_rounds(season: int) -> list[int]:
    """
    Returns available F1 rounds from the Jolpica API
    """
    data = fetch_endpoint(str(season))
    races = data["MRData"]["RaceTable"].get("Races", [])

    return [int(race["round"]) for race in races]

def get_available_seasons(start_year: int = 2024) -> list[int]:
    """
    Return available F1 seasons from Jolpica, filtered by minimum year.
    Handles paginated API results.
    """
    all_seasons = []
    limit = 30
    offset = 0

    while True:
        data = fetch_endpoint(f"seasons?limit={limit}&offset={offset}")
        seasons = data["MRData"]["SeasonTable"].get("Seasons", [])

        if not seasons:
            break

        all_seasons.extend(int(season["season"]) for season in seasons)

        total = int(data["MRData"].get("total", 0))
        offset += limit

        if offset >= total:
            break

    return [season for season in sorted(all_seasons) if season >= start_year]