"""Fantasy Football RAG System.

A Retrieval-Augmented Generation system for fantasy football that stores
player statistics, team data, and news articles in a pgvector database for
intelligent querying.
"""

__version__ = "1.0.0"

# Import classes for package-level access
# Note: These imports may fail if dependencies are not installed
try:
    from config import Config
    from database import DatabaseManager
    from embeddings import EmbeddingService
    from rag import FantasyFootballRAG
    from ingest_stats import PlayerStatsIngestion, TeamStatsIngestion
    from ingest_news import NewsIngestion
    
    __all__ = [
        'Config',
        'DatabaseManager',
        'EmbeddingService',
        'FantasyFootballRAG',
        'PlayerStatsIngestion',
        'TeamStatsIngestion',
        'NewsIngestion',
    ]
except ImportError:
    # Dependencies not installed, package can still be imported
    __all__ = []
