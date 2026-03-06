
from dataclasses import fields, asdict
from services.database import DatabaseManager
from stats.models import PlayerStatsDocument


class IngestionManager:
    database_manager: DatabaseManager

    def __init__(self, **data):
        super().__init__(**data)
        self.database_manager = DatabaseManager()

    def ingest_player_stats(self, stats_data: list[dict]):
        if not self.database_manager.connection:
            self.database_manager.connect()
        cursor = self.database_manager.connection.cursor()

        field_mapping = {
            "player_display_name": "player_name",
        }

        valid_fields = {field.name for field in fields(PlayerStatsDocument)}

        for stat in stats_data:
            try:
                print(f"Ingesting stat for player {stat['player_display_name']}...")
                
                stat_mapped = {field_mapping.get(k, k): v for k, v in stat.items()}
                
                stat_filtered = {k: v for k, v in stat_mapped.items() if k in valid_fields}

                player: PlayerStatsDocument = PlayerStatsDocument(
                    **stat_filtered
                )
                player_dict = asdict(player)
                
                # Exclude id, database handles it
                player_dict.pop('id', None)
                
                columns = ", ".join(player_dict.keys())
                placeholders = ", ".join(["%s"] * len(player_dict))
                values = tuple(player_dict.values())
                cursor.execute(
                    f"INSERT INTO player_stats_documents ({columns}) VALUES ({placeholders})",
                    values,
                )
                print(f"Inserted stat for player {stat['player_display_name']} into database.")
            except Exception as e:
                self.database_manager.connection.rollback()
                print(
                    f"Error ingesting stat for player {stat['player_display_name']}: {e}"
                )
        self.database_manager.connection.commit()
        cursor.close()
