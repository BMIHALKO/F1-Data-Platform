"""
Extract race calendar data from Jolpica API.

This file retireives race metadata by season, flattens nested session fields, and returns recods ready for loading into staging.races
"""
import requests
import pandas as pd

from ingestion.load.postgres_loader import load_dataframe_to_table



BASE_URL = "https://api.jolpi.ca/ergast/f1"

def _session_date(session):
    return session.get("date") if session else None

def _session_time(session):
    return session.get("time") if session else None

def flatten_race(race):
    circuit = race.get("Circuit", {})

    first_practice = race.get("FirstPractice")
    second_practice = race.get("SecondPractice")
    third_practice = race.get("ThirdPractice")
    qualifying = race.get("Qualifying")
    sprint = race.get("Sprint")
    sprint_qualifying = race.get("SprintQualifying")

    return {
        "season": int(race.get("season")),
        "round_number": int(race.get("round")),
        "race_name": race.get("raceName"),
        "race_date": race.get("date"),
        "race_time": race.get("time"),
        "circuit_id": circuit.get("circuitId"),

        "fp1_date": _session_date(first_practice),
        "fp1_time": _session_time(first_practice),

        "fp2_date": _session_date(second_practice),
        "fp2_time": _session_time(second_practice),

        "fp3_date": _session_date(third_practice),
        "fp3_time": _session_time(third_practice),

        "qualifying_date": _session_date(qualifying),
        "qualifying_time": _session_time(qualifying),

        "sprint_date": _session_date(sprint),
        "sprint_time": _session_time(sprint),

        "sprint_qualifying_date": _session_date(sprint_qualifying),
        "sprint_qualifying_time": _session_time(sprint_qualifying),

        "profile_url": race.get("url"),
    }

# Season extraction
def extract_races_for_season(season):
    url = f"{BASE_URL}/{season}/races.json"
    params = {"limit": 100}

    response = requests.get(url, params = params, timeout = 30)
    response.raise_for_status()

    data = response.json()

    races = (
        data.get("MRData", {})
        .get("RaceTable", {})
        .get("Races", {})
    )

    return [flatten_race(race) for race in races]

# Multi-season extraction
def extract_races_for_seasons(seasons):
    all_races = []

    for season in seasons:
        all_races.extend(extract_races_for_season(season))

    return all_races