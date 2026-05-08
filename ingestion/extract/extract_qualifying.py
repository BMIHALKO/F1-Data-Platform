"""
Extract qualifying results data from the Jolpica API

This file retrieves qualifying session results by season and round, flattens nested driver/constructor fields, and returns records ready for loading into staging.qualifying
"""

import requests
import time

BASE_URL = "https://api.jolpi.ca/ergast/f1"

HOURLY_LIMIT = 500
QUALIFYING_REQUEST_COUNT = 0


def flatten_qualifying_results(race, result):
    driver = result.get("Driver", {})
    constructor = result.get("Constructor", {})

    return {
        "season": int(race.get("season")),
        "round_number": int(race.get("round")),
        "race_name": race.get("raceName"),
        "race_date": race.get("date"),
        "car_number": result.get("number"),
        "qualifying_position": int(result.get("position")),
        "driver_id": driver.get("driverId"),
        "constructor_id": constructor.get("constructorId"),
        "q1_time": result.get("Q1"),
        "q2_time" : result.get("Q2"),
        "q3_time": result.get("Q3"),
    }

def extract_qualifying(season, round_number):
    url = f"{BASE_URL}/{season}/{round_number}/qualifying.json"
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

    races = (
        data.get("MRData", {})
        .get("RaceTable", {})
        .get("Races", [])
    )

    if not races:
        return []
    
    race = races[0]
    qualifying_results = race.get("QualifyingResults", [])

    return [
        flatten_qualifying_results(race, result)
        for result in qualifying_results
    ]

def extract_qualifying_for_season(season, rounds):
    global QUALIFYING_REQUEST_COUNT

    all_qualifying = []

    for round_index, round_number in enumerate(rounds, start = 1):
        all_qualifying.extend(
            extract_qualifying(season, round_number)
        )

        QUALIFYING_REQUEST_COUNT += 1
        remaining = HOURLY_LIMIT - QUALIFYING_REQUEST_COUNT

        print(
            f"{season} qualifying round {round_index}/{len(rounds)} "
            f"(round) {round_number} | "
            f"Estimated hourly budget remaining: {remaining}/500"
        )

        time.sleep(2)
    
    return all_qualifying

if __name__ == "__main__":
    qualifying = extract_qualifying(2024, 1)

    print(f"Extracted {len(qualifying)} qualifying recrods")

    for record in qualifying[:3]:
        print(record)