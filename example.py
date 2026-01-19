"""Example script demonstrating how to use the fantasy football RAG system."""
from ingest_stats import PlayerStatsIngestion, TeamStatsIngestion
from ingest_news import NewsIngestion
from rag import FantasyFootballRAG


def example_ingest_data():
    """Example of ingesting player stats, team stats, and news."""
    
    # Initialize ingestion services
    player_ingestion = PlayerStatsIngestion()
    team_ingestion = TeamStatsIngestion()
    news_ingestion = NewsIngestion()
    
    # Example: Ingest player statistics
    print("Ingesting player statistics...")
    example_players = [
        {
            'name': 'Patrick Mahomes',
            'team': 'Kansas City Chiefs',
            'position': 'QB',
            'stats': {
                'passing_yards': 4839,
                'touchdowns': 37,
                'interceptions': 13,
                'completion_percentage': 67.2,
                'rating': 105.2
            },
            'season': '2023',
            'week': None
        },
        {
            'name': 'Christian McCaffrey',
            'team': 'San Francisco 49ers',
            'position': 'RB',
            'stats': {
                'rushing_yards': 1459,
                'rushing_touchdowns': 14,
                'receptions': 67,
                'receiving_yards': 564,
                'receiving_touchdowns': 7
            },
            'season': '2023',
            'week': None
        }
    ]
    
    player_ingestion.batch_ingest_players(example_players)
    
    # Example: Ingest team statistics
    print("\nIngesting team statistics...")
    example_teams = [
        {
            'name': 'Kansas City Chiefs',
            'stats': {
                'wins': 11,
                'losses': 6,
                'points_per_game': 21.8,
                'points_allowed_per_game': 17.3,
                'total_yards_per_game': 343.7
            },
            'season': '2023',
            'week': None
        }
    ]
    
    team_ingestion.batch_ingest_teams(example_teams)
    
    # Example: Ingest news articles
    print("\nIngesting news articles...")
    example_articles = [
        {
            'title': 'Patrick Mahomes leads Chiefs to victory',
            'content': 'Patrick Mahomes threw for 320 yards and 3 touchdowns as the Kansas City Chiefs '
                      'defeated their division rivals. Mahomes showed excellent accuracy and decision-making '
                      'throughout the game, solidifying his position as one of the elite quarterbacks in the league.',
            'source': 'Fantasy Football News',
            'url': 'https://example.com/mahomes-victory',
            'published_date': None
        },
        {
            'title': 'Christian McCaffrey injury update',
            'content': 'San Francisco 49ers running back Christian McCaffrey is expected to be ready for '
                      'the upcoming game after missing practice earlier this week. The team medical staff has '
                      'cleared him to play, which is great news for fantasy owners.',
            'source': 'NFL Insider',
            'url': 'https://example.com/cmc-injury',
            'published_date': None
        }
    ]
    
    news_ingestion.batch_ingest_articles(example_articles)
    
    print("\nData ingestion complete!")


def example_query():
    """Example of querying the RAG system."""
    
    # Initialize RAG system
    rag = FantasyFootballRAG()
    
    # Example queries
    questions = [
        "How is Patrick Mahomes performing this season?",
        "Should I start Christian McCaffrey this week?",
        "What are the Chiefs' offensive stats?",
    ]
    
    print("\nQuerying the RAG system...\n")
    
    for question in questions:
        print(f"Question: {question}")
        result = rag.query(question, top_k=2)
        print(f"Answer: {result['answer']}\n")
        print("-" * 80)


if __name__ == "__main__":
    print("Fantasy Football RAG System - Example Usage\n")
    print("=" * 80)
    
    # Note: Make sure to set up your database and environment variables first
    print("\nPrerequisites:")
    print("1. Set up PostgreSQL with pgvector extension")
    print("2. Create a .env file with your database credentials and OpenAI API key")
    print("3. Run 'python database.py' to initialize the database\n")
    
    choice = input("What would you like to do?\n1. Ingest example data\n2. Query the system\n3. Both\nChoice (1/2/3): ")
    
    if choice == "1":
        example_ingest_data()
    elif choice == "2":
        example_query()
    elif choice == "3":
        example_ingest_data()
        print("\n" + "=" * 80 + "\n")
        example_query()
    else:
        print("Invalid choice. Please run the script again.")
