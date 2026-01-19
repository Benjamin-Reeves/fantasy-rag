"""Data ingestion module for player and team statistics."""
import json
from database import DatabaseManager
from embeddings import EmbeddingService


class PlayerStatsIngestion:
    """Handles ingestion of player statistics."""
    
    def __init__(self):
        """Initialize player stats ingestion."""
        self.db_manager = DatabaseManager()
        self.embedding_service = EmbeddingService()
    
    def ingest_player_stats(self, player_name, team, position, stats_data, season, week=None):
        """
        Ingest player statistics into the database.
        
        Args:
            player_name (str): Player name
            team (str): Team name
            position (str): Player position
            stats_data (dict): Dictionary of player statistics
            season (str): Season identifier (e.g., "2023-2024")
            week (int): Week number (optional)
        """
        try:
            # Create text representation for embedding
            stats_text = f"Player: {player_name}, Team: {team}, Position: {position}, Season: {season}"
            if week:
                stats_text += f", Week: {week}"
            
            # Add stats to text
            stats_text += f", Stats: {json.dumps(stats_data)}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(stats_text)
            
            # Store in database
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO player_stats (player_name, team, position, stats_data, season, week, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                player_name,
                team,
                position,
                json.dumps(stats_data),
                season,
                week,
                embedding
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Ingested stats for player: {player_name}")
        except Exception as e:
            print(f"Error ingesting player stats: {e}")
            raise
    
    def batch_ingest_players(self, players_data):
        """
        Ingest multiple player statistics.
        
        Args:
            players_data (list): List of player data dictionaries
        """
        for player in players_data:
            self.ingest_player_stats(
                player['name'],
                player['team'],
                player['position'],
                player['stats'],
                player['season'],
                player.get('week')
            )


class TeamStatsIngestion:
    """Handles ingestion of team statistics."""
    
    def __init__(self):
        """Initialize team stats ingestion."""
        self.db_manager = DatabaseManager()
        self.embedding_service = EmbeddingService()
    
    def ingest_team_stats(self, team_name, stats_data, season, week=None):
        """
        Ingest team statistics into the database.
        
        Args:
            team_name (str): Team name
            stats_data (dict): Dictionary of team statistics
            season (str): Season identifier (e.g., "2023-2024")
            week (int): Week number (optional)
        """
        try:
            # Create text representation for embedding
            stats_text = f"Team: {team_name}, Season: {season}"
            if week:
                stats_text += f", Week: {week}"
            
            # Add stats to text
            stats_text += f", Stats: {json.dumps(stats_data)}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(stats_text)
            
            # Store in database
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO team_stats (team_name, stats_data, season, week, embedding)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                team_name,
                json.dumps(stats_data),
                season,
                week,
                embedding
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Ingested stats for team: {team_name}")
        except Exception as e:
            print(f"Error ingesting team stats: {e}")
            raise
    
    def batch_ingest_teams(self, teams_data):
        """
        Ingest multiple team statistics.
        
        Args:
            teams_data (list): List of team data dictionaries
        """
        for team in teams_data:
            self.ingest_team_stats(
                team['name'],
                team['stats'],
                team['season'],
                team.get('week')
            )
