import nflreadpy as nfl

from stats.ingestion import IngestionManager

years = [2019]

stat_ingestion: IngestionManager = IngestionManager()

for year in years:
    nfl_reader = nfl.load_player_stats(seasons=[year], summary_level="week")
    print(f"Loaded {len(nfl_reader)} player stats for {year} season.")

    stat_ingestion.ingest_player_stats(nfl_reader.to_pandas().to_dict(orient="records"))