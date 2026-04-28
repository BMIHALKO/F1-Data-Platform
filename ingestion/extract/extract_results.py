import pandas as pd
from ingestion.extract.jolpica_client import fetch_endpoint

def extract_results(season: int, round_number: int) -> pd.DataFrame:
    """
    Extract and flatten race results from the Jolpica F1 API

    Args:
        season: F1 season year, such as 2024
        round_number: Race round number, such as 1
    
    Returns:
        DataFrame matching staging.stg_results structure
    """

    endpoint = f"{season}/{round_number}/results"
    data = fetch_endpoint(endpoint)

    races = data["MRData"]["RaceTable"].get("Races", [])

    rows = []

    for race in races:
        race_name = race.get("raceName")
        race_date = race.get("date")

        for result in race.get("Results", []):
            driver = result.get("Driver", {})
            constructor = result.get("Constructor", {})
            fastest_lap = result.get("FastestLap", {})
            fastest_lap_time = fastest_lap.get("Time", {})

            rows.append(
                {
                    "season": int(season),
                    "round_number": int(round_number),
                    "race_name": race_name,
                    "race_date": race_date,
                    "car_number": result.get("number"),
                    "finishing_position": _safe_int(result.get("position")),
                    "position_text": result.get("positionText"),
                    "points": _safe_float(result.get("points")),
                    "driver_id": driver.get("driverId"),
                    "constructor_id": constructor.get("constructorId"),
                    "grid_position": _safe_int(result.get("grid")),
                    "laps_completed": _safe_int(result.get("laps")),
                    "race_status": result.get("status"),
                    "finish_time_millis": _safe_int(result.get("Time", {}).get("millis")),
                    "finish_time": result.get("Time", {}).get("time"),
                    "fastest_lap_rank": _safe_int(fastest_lap.get("rank")),
                    "fastest_lap_number": _safe_int(fastest_lap.get("lap")),
                    "fastest_lap_time": fastest_lap_time.get("time"),
                }
            )
    
    return pd.DataFrame(rows)

def _safe_int(value):
    if value is None or value == "":
        return None

    try:
        return int(value)
    
    except ValueError:
        return None

def _safe_float(value):
    if value is None or value == "":
        return None
    
    try:
        return float(value)
    
    except ValueError:
        return None