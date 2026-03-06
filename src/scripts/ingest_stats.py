"""Standalone script for ingesting player stats into the database."""

import sys

import nflreadpy as nfl

from stats.ingestion import IngestionManager


def main():
    """
    Ingest player stats from NFL data.

    Usage:
        python -m scripts.ingest_stats [year]

    If no year is provided, defaults to 2019.
    """
    # Get year from command line or use default
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print(f"Error: Invalid year '{sys.argv[1]}'. Please provide a valid year.")
            sys.exit(1)
    else:
        year = 2019

    print(f"Loading player stats for {year} season...")

    # Load NFL data
    try:
        nfl_reader = nfl.load_player_stats(seasons=[year], summary_level="week")
        print(f"Loaded {len(nfl_reader)} player stats for {year} season.")
    except Exception as e:
        print(f"Error loading NFL data: {e}")
        sys.exit(1)

    # Ingest stats
    print("Beginning ingestion of player stats...")
    stat_ingestion = IngestionManager()

    try:
        stat_ingestion.ingest_player_stats(
            nfl_reader.to_pandas().to_dict(orient="records")
        )
        print("\n" + "=" * 50)
        print("Ingestion Complete!")
        print("=" * 50)
        print(f"Successfully ingested {year} season player stats.")
    except Exception as e:
        print(f"Error during ingestion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
