import time
import pandas as pd

from ingestion.extract.extract_results import extract_results
from ingestion.extract.extract_races import extract_races_for_seasons
from ingestion.extract.extract_drivers import extract_drivers
from ingestion.extract.extract_constructors import extract_constructors
from ingestion.extract.extract_circuits import extract_circuits
from ingestion.extract.extract_qualifying import extract_qualifying_for_season
from ingestion.extract.extract_constructor_standings import extract_constructor_standings_for_seasons
from ingestion.extract.extract_driver_standings import extract_driver_standings_for_seasons

from ingestion.extract.jolpica_client import get_available_rounds, get_available_seasons
from ingestion.load.postgres_loader import load_dataframe_to_table


START_YEAR = 1950
END_YEAR = 2009
REQUEST_DELAY_SECONDS = 2

SECTION_DELAY_SECONDS = 900

RESULTS_START_YEAR = 2001
QUALIFYING_START_YEAR = 1978
QUALIFYING_END_YEAR = 1995

CONSTRUCTOR_STANDINGS_START_YEAR = 1950
CONSTRUCTOR_STANDINGS_END_YEAR = 1959

RUN_RESULTS = False
RUN_RACES = False
RUN_DRIVERS = False
RUN_CONSTRUCTORS = False
RUN_CIRCUITS = False
RUN_QUALIFYING = True
RUN_CONSTRUCTOR_STANDINGS = True
RUN_DRIVER_STANDINGS = False



def elapsed_seconds(start_time):
    return time.time() -  start_time

def get_target_seasons(start_year=START_YEAR, end_year=END_YEAR):
    return [
        season
        for season in get_available_seasons(start_year=start_year)
        if season <= end_year
    ]


def load_records_to_staging(records, table_name):
    df = pd.DataFrame(records)
    return load_dataframe_to_table(df, "staging", table_name)


def print_summary(title, extracted_count, inserted_count):
    print(f"\n{title} Summary:")
    print(f"Records extracted: {extracted_count}")
    print(f"Records inserted: {inserted_count}")


def load_results():
    seasons = get_target_seasons(start_year = RESULTS_START_YEAR)

    inserted_total = 0
    skipped_existing = 0
    skipped_empty = 0

    for season in seasons:
        season_start_time = time.time()

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

            time.sleep(REQUEST_DELAY_SECONDS)

        print(
            f"{season} Round {round_number} complete | "
            f"Elapsed: {elapsed_seconds(season_start_time):.1f}s"
        )

    print("\nResults Summary:")
    print(f"Rows inserted: {inserted_total}")
    print(f"Rounds skipped - already loaded: {skipped_existing}")
    print(f"Rounds skipped - no results available: {skipped_empty}")


def load_races():
    section_start_time = time.time()

    seasons = get_target_seasons()

    races = extract_races_for_seasons(seasons)
    rows_loaded = load_records_to_staging(races, "races")

    print("\nRaces Summary:")
    print(f"Seasons checked: {seasons}")
    print(f"Race records extracted: {len(races)}")
    print(
        f"Race records inserted: {rows_loaded} | "
        f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
    )


def load_drivers():
    section_start_time = time.time()

    drivers = extract_drivers()
    rows_loaded = load_records_to_staging(drivers, "drivers")

    print("Drivers Summary:")
    print(f"Records extracted: {len(drivers)}")
    print(
        f"Drivers inserted: {rows_loaded} | "
        f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
    )


def load_constructors():
    section_start_time = time.time()

    constructors = extract_constructors()
    rows_loaded = load_records_to_staging(constructors, "constructors")

    print("Constructors Summary:")
    print(f"Records extracted: {len(constructors)}")
    print(
        f"Constructors inserted: {rows_loaded} | "
        f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
    )


def load_circuits():
    section_start_time = time.time()

    circuits = extract_circuits()
    rows_loaded = load_records_to_staging(circuits, "circuits")

    print("Circuits Summary:")
    print(f"Records extracted: {len(circuits)}")
    print(
        f"Circuits inserted: {rows_loaded} | "
        f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
    )


def load_qualifying():
    section_start_time = time.time()
    
    seasons = get_target_seasons(start_year = QUALIFYING_START_YEAR, end_year = QUALIFYING_END_YEAR)

    total_extracted = 0
    total_inserted = 0

    for season in seasons:
        rounds = get_available_rounds(season)

        qualifying = extract_qualifying_for_season(season, rounds)
        rows_loaded = load_records_to_staging(qualifying, "qualifying")

        total_extracted += len(qualifying)
        total_inserted += rows_loaded

        print(
            f"{season} qualifying inserted: {rows_loaded} | "
            f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
        )

    print_summary("Qualifying", total_extracted, total_inserted)


def load_constructor_standings():
    section_start_time = time.time()
    
    seasons = get_target_seasons(start_year = CONSTRUCTOR_STANDINGS_START_YEAR, end_year = CONSTRUCTOR_STANDINGS_END_YEAR)

    standings = extract_constructor_standings_for_seasons(seasons)
    rows_loaded = load_records_to_staging(standings, "constructor_standings")

    print("\nConstructor Standings Summary:")
    print(f"Records extracted: {len(standings)}")
    print(
        f"Records inserted: {rows_loaded} | "
        f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
    )


def load_driver_standings():
    section_start_time = time.time()
    
    seasons = get_target_seasons()

    standings = extract_driver_standings_for_seasons(seasons)
    rows_loaded = load_records_to_staging(standings, "driver_standings")

    print("\nDriver Standings Summary:")
    print(f"Records extracted: {len(standings)}")
    print(
        f"Records inserted: {rows_loaded} | "
        f"Elapsed: {elapsed_seconds(section_start_time):.1f}s"
    )


def main():
    print("\n=== Starting Full F1 Staging Pipeline ===")
    print(f"Target seasons: {START_YEAR} to {END_YEAR}")

    if RUN_RESULTS:
        print("\n--- Loading Results ---")
        load_results()
        print(f"\nSleeping {SECTION_DELAY_SECONDS}s before next section...")
        time.sleep(SECTION_DELAY_SECONDS)
    else:
        print("\n--- Skipping Results ---")

    if RUN_RACES:
        print("\n--- Loading Races ---")
        load_races()
        print(f"\nSleeping {SECTION_DELAY_SECONDS}s before next section...")
        time.sleep(SECTION_DELAY_SECONDS)
    else:
        print("\n--- Skipping Races ---")

    if RUN_DRIVERS:
        print("\n--- Loading Drivers ---")
        load_drivers()
    else:
        print("\n--- Skipping Drivers ---")

    if RUN_CONSTRUCTORS:
        print("\n--- Loading Constructors ---")
        load_constructors()
    else:
        print("\n--- Skipping Constructors ---")

    if RUN_CIRCUITS:
        print("\n--- Loading Circuits ---")
        load_circuits()
    else:
        print("\n--- Skipping Circuits ---")

    if RUN_QUALIFYING:
        print("\n--- Loading Qualifying ---")
        load_qualifying()
        print(f"\nSleeping {SECTION_DELAY_SECONDS}s before next section...")
        time.sleep(SECTION_DELAY_SECONDS)
    else:
        print("\n--- Skipping Qualifying ---")

    if RUN_CONSTRUCTOR_STANDINGS:
        print("\n--- Loading Constructor Standings ---")
        load_constructor_standings()
        print(f"\nSleeping {SECTION_DELAY_SECONDS}s before next section...")
        time.sleep(SECTION_DELAY_SECONDS)
    else:
        print("\n--- Skipping Constructor Standings ---")

    if RUN_DRIVER_STANDINGS:
        print("\n--- Loading Driver Standings ---")
        load_driver_standings()
    else:
        print("\n--- Skipping Driver Standings ---")

    print("\n=== Pipeline Complete ===")


if __name__ == "__main__":
    main()