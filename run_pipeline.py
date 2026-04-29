import time
import pandas as pd

from ingestion.extract.extract_results import extract_results
from ingestion.extract.extract_races import extract_races_for_seasons
from ingestion.extract.extract_drivers import extract_drivers
from ingestion.extract.extract_constructors import extract_constructors
from ingestion.extract.extract_circuits import extract_cicuits


from ingestion.extract.jolpica_client import get_available_rounds, get_available_seasons
from ingestion.load.postgres_loader import load_dataframe_to_table

def load_results(start_year = 2010):
    seasons = get_available_seasons(start_year = start_year)

    inserted_total = 0
    skipped_existing = 0
    skipped_empty = 0

    for season in seasons:
        rounds = get_available_rounds(season)

        season_rows = 0
        season_rounds_loaded = 0

        for round_number in rounds:
            df = extract_results(season, round_number)

            if df.empty:
                skipped_empty += 1
                continue

            rows_loaded = load_dataframe_to_table(df, "staging", "results")

            if rows_loaded == 0:
                skipped_existing += 1
            
            else:
                season_rows += rows_loaded
                season_rounds_loaded += 1
                inserted_total += rows_loaded
        
            time.sleep(2)
        
        print(f"{season} results loaded: {season_rows} row across {season_rounds_loaded} rounds.")
    
    print("\nResults Summary:")
    print(f"Rows inserted: {inserted_total}")
    print(f"Rounds skipped - already loaded: {skipped_existing}")
    print(f"Rounds skipped - no results available: {skipped_empty}")

def load_races(start_year = 2010):
    seasons = get_available_seasons(start_year = start_year)

    races = extract_races_for_seasons(seasons)
    races_df = pd.DataFrame(races)

    rows_loaded = load_dataframe_to_table(races_df, "staging", "races")

    print("\nRaces Summary:")
    print(f"Seasons checked: {seasons}")
    print(f"Race records extracted: {len(races)}")
    print(f"Race records inserted: {rows_loaded}")

def load_drivers():
    drivers = extract_drivers()
    drivers_df = pd.DataFrame(drivers)

    rows_loaded = load_dataframe_to_table(drivers_df, "staging", "drivers")

    print("\nDrivers Summary:")
    print(f"Driver records extracted: {len(drivers)}")
    print(f"Driver records inserted: {rows_loaded}")

def load_constructors():
    constructors = extract_constructors()
    constructors_df = pd.DataFrame(constructors)

    rows_loaded = load_dataframe_to_table(constructors_df, "staging", "constructors")

    print("\nConstructors Summary:")
    print(f"Constructor records extracted: {len(constructors)}")
    print(f"Constructor records inserted: {rows_loaded}")

def load_circuits():
    circuits = extract_cicuits()
    circuits_df = pd.DataFrame(circuits)

    rows_loaded = load_dataframe_to_table(circuits_df, "staging", "circuits")

    print("\nCircuits Summary:")
    print(f"Circuit records extracted: {len(circuits)}")
    print(f"Circuit records inserted: {rows_loaded}")

def main():
    """
    Run only the loads you want active right now
    
    load_results(start_year = 2010)

    load_races(start_year = 2010)
    """
    # load_drivers()
    # load_constructors()
    load_circuits()


if __name__ == "__main__":
    main()