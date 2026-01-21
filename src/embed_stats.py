import nflreadpy as nfl

from stats.ingestion import IngestionManager

nfl_reader = nfl.load_player_stats(seasons=[2025], summary_level="week")
print(f"Loaded {len(nfl_reader)} player stats for 2025 season.")

stat_ingestion: IngestionManager = IngestionManager()

print("Beginning ingestion of player stats...")

stat_ingestion.ingest_player_stats(nfl_reader.to_pandas().to_dict(orient="records"))