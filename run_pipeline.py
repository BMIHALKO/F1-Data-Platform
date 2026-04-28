import time

from ingestion.extract.extract_results import extract_results
from ingestion.load.postgres_loader import load_dataframe_to_table
from ingestion.extract.jolpica_client import get_available_rounds, get_available_seasons


def main():
    seasons = get_available_seasons(start_year=2023)

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

        print(f"{season} season loaded: {season_rows} rows across {season_rounds_loaded} rounds.")

    print("\nPipeline summary")
    print(f"Rows inserted: {inserted_total}")
    print(f"Rounds skipped - already loaded: {skipped_existing}")
    print(f"Rounds skipped - no results available: {skipped_empty}")


if __name__ == "__main__":
    main()