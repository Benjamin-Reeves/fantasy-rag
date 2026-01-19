#!/usr/bin/env python3
"""Command-line interface for the fantasy football RAG system."""
import argparse
import sys
from database import DatabaseManager
from ingest_stats import PlayerStatsIngestion, TeamStatsIngestion
from ingest_news import NewsIngestion
from rag import FantasyFootballRAG


def setup_database(args):
    """Set up the database."""
    db = DatabaseManager()
    print("Creating database...")
    db.create_database()
    print("Initializing pgvector...")
    db.initialize_pgvector()
    print("Database setup complete!")


def ingest_player(args):
    """Ingest a player's statistics."""
    player_ingestion = PlayerStatsIngestion()
    
    stats = {}
    if args.stats:
        import json
        stats = json.loads(args.stats)
    
    player_ingestion.ingest_player_stats(
        player_name=args.name,
        team=args.team,
        position=args.position,
        stats_data=stats,
        season=args.season,
        week=args.week
    )
    print(f"Successfully ingested stats for {args.name}")


def ingest_team(args):
    """Ingest a team's statistics."""
    team_ingestion = TeamStatsIngestion()
    
    stats = {}
    if args.stats:
        import json
        stats = json.loads(args.stats)
    
    team_ingestion.ingest_team_stats(
        team_name=args.name,
        stats_data=stats,
        season=args.season,
        week=args.week
    )
    print(f"Successfully ingested stats for {args.name}")


def ingest_news_article(args):
    """Ingest a news article."""
    news_ingestion = NewsIngestion()
    
    if args.url and args.scrape:
        news_ingestion.scrape_and_ingest_article(
            url=args.url,
            source=args.source
        )
    else:
        news_ingestion.ingest_article(
            title=args.title,
            content=args.content,
            source=args.source,
            url=args.url or ""
        )
    print("Successfully ingested news article")


def query_system(args):
    """Query the RAG system."""
    rag = FantasyFootballRAG()
    
    sources = ['players', 'teams', 'news']
    if args.sources:
        sources = args.sources.split(',')
    
    result = rag.query(
        question=args.question,
        include_sources=sources,
        top_k=args.top_k
    )
    
    print("\n" + "=" * 80)
    print("ANSWER:")
    print("=" * 80)
    print(result['answer'])
    
    if args.show_context:
        print("\n" + "=" * 80)
        print("CONTEXT:")
        print("=" * 80)
        print(result['context'])


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Fantasy Football RAG System CLI'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up the database')
    setup_parser.set_defaults(func=setup_database)
    
    # Ingest player command
    player_parser = subparsers.add_parser('ingest-player', help='Ingest player statistics')
    player_parser.add_argument('--name', required=True, help='Player name')
    player_parser.add_argument('--team', required=True, help='Team name')
    player_parser.add_argument('--position', required=True, help='Player position')
    player_parser.add_argument('--stats', help='Stats as JSON string')
    player_parser.add_argument('--season', required=True, help='Season (e.g., 2023)')
    player_parser.add_argument('--week', type=int, help='Week number')
    player_parser.set_defaults(func=ingest_player)
    
    # Ingest team command
    team_parser = subparsers.add_parser('ingest-team', help='Ingest team statistics')
    team_parser.add_argument('--name', required=True, help='Team name')
    team_parser.add_argument('--stats', help='Stats as JSON string')
    team_parser.add_argument('--season', required=True, help='Season (e.g., 2023)')
    team_parser.add_argument('--week', type=int, help='Week number')
    team_parser.set_defaults(func=ingest_team)
    
    # Ingest news command
    news_parser = subparsers.add_parser('ingest-news', help='Ingest news article')
    news_parser.add_argument('--title', help='Article title')
    news_parser.add_argument('--content', help='Article content')
    news_parser.add_argument('--source', required=True, help='Article source')
    news_parser.add_argument('--url', help='Article URL')
    news_parser.add_argument('--scrape', action='store_true', help='Scrape content from URL')
    news_parser.set_defaults(func=ingest_news_article)
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query the RAG system')
    query_parser.add_argument('question', help='Question to ask')
    query_parser.add_argument('--sources', help='Comma-separated sources (players,teams,news)')
    query_parser.add_argument('--top-k', type=int, default=3, help='Number of results per source')
    query_parser.add_argument('--show-context', action='store_true', help='Show context used')
    query_parser.set_defaults(func=query_system)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
