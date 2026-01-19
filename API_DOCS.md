# Fantasy Football RAG System API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Configuration](#configuration)
3. [Database Management](#database-management)
4. [Embedding Service](#embedding-service)
5. [Data Ingestion](#data-ingestion)
6. [RAG Query Interface](#rag-query-interface)
7. [Utilities](#utilities)
8. [Command Line Interface](#command-line-interface)

## Overview

The Fantasy Football RAG System provides a complete solution for storing and querying fantasy football data using vector embeddings and semantic search.

## Configuration

### Config Class

**Module:** `config.py`

**Description:** Manages application configuration from environment variables.

#### Properties

- `DB_HOST` (str): Database host address (default: 'localhost')
- `DB_PORT` (int): Database port (default: 5432)
- `DB_NAME` (str): Database name (default: 'fantasy_football')
- `DB_USER` (str): Database user (default: 'postgres')
- `DB_PASSWORD` (str): Database password
- `OPENAI_API_KEY` (str): OpenAI API key for embeddings and chat
- `VECTOR_DIMENSION` (int): Embedding vector dimension (default: 1536)

#### Methods

##### `db_connection_string`

Returns the PostgreSQL connection string.

**Returns:** `str` - Connection string in format `postgresql://user:password@host:port/dbname`

**Example:**
```python
from config import Config

config = Config()
conn_string = config.db_connection_string
```

## Database Management

### DatabaseManager Class

**Module:** `database.py`

**Description:** Handles database creation, initialization, and connections.

#### Methods

##### `create_database()`

Creates the database if it doesn't exist.

**Returns:** None

**Raises:** Exception if database creation fails

**Example:**
```python
from database import DatabaseManager

db = DatabaseManager()
db.create_database()
```

##### `initialize_pgvector()`

Initializes pgvector extension and creates all required tables.

**Creates Tables:**
- `player_stats`: Player statistics with embeddings
- `team_stats`: Team statistics with embeddings
- `news_articles`: News articles with embeddings

**Returns:** None

**Raises:** Exception if initialization fails

**Example:**
```python
db.initialize_pgvector()
```

##### `get_connection()`

Returns a database connection.

**Returns:** `psycopg2.connection` - Active database connection

**Example:**
```python
conn = db.get_connection()
cursor = conn.cursor()
# ... use connection ...
cursor.close()
conn.close()
```

## Embedding Service

### EmbeddingService Class

**Module:** `embeddings.py`

**Description:** Generates text embeddings using OpenAI's API.

#### Methods

##### `generate_embedding(text)`

Generates embedding for a single text.

**Parameters:**
- `text` (str): Text to generate embedding for

**Returns:** `list` - Embedding vector (1536 dimensions)

**Raises:** Exception if embedding generation fails

**Example:**
```python
from embeddings import EmbeddingService

service = EmbeddingService()
embedding = service.generate_embedding("Patrick Mahomes QB stats")
```

##### `generate_embeddings_batch(texts)`

Generates embeddings for multiple texts efficiently.

**Parameters:**
- `texts` (list): List of text strings

**Returns:** `list` - List of embedding vectors

**Example:**
```python
texts = ["Player 1 stats", "Player 2 stats", "Player 3 stats"]
embeddings = service.generate_embeddings_batch(texts)
```

## Data Ingestion

### PlayerStatsIngestion Class

**Module:** `ingest_stats.py`

**Description:** Handles ingestion of player statistics.

#### Methods

##### `ingest_player_stats(player_name, team, position, stats_data, season, week=None)`

Ingests statistics for a single player.

**Parameters:**
- `player_name` (str): Player's full name
- `team` (str): Team name
- `position` (str): Player position (QB, RB, WR, TE, K, DEF)
- `stats_data` (dict): Dictionary of statistics
- `season` (str): Season identifier (e.g., "2023" or "2023-2024")
- `week` (int, optional): Week number

**Returns:** None

**Example:**
```python
from ingest_stats import PlayerStatsIngestion

ingestion = PlayerStatsIngestion()
ingestion.ingest_player_stats(
    player_name="Patrick Mahomes",
    team="Kansas City Chiefs",
    position="QB",
    stats_data={
        'passing_yards': 4839,
        'touchdowns': 37,
        'interceptions': 13,
        'completion_percentage': 67.2
    },
    season="2023"
)
```

##### `batch_ingest_players(players_data)`

Ingests multiple players at once.

**Parameters:**
- `players_data` (list): List of player dictionaries with keys: name, team, position, stats, season, week

**Returns:** None

**Example:**
```python
players = [
    {
        'name': 'Patrick Mahomes',
        'team': 'Kansas City Chiefs',
        'position': 'QB',
        'stats': {'passing_yards': 4839, 'touchdowns': 37},
        'season': '2023'
    },
    # ... more players
]
ingestion.batch_ingest_players(players)
```

### TeamStatsIngestion Class

**Module:** `ingest_stats.py`

**Description:** Handles ingestion of team statistics.

#### Methods

##### `ingest_team_stats(team_name, stats_data, season, week=None)`

Ingests statistics for a single team.

**Parameters:**
- `team_name` (str): Team name
- `stats_data` (dict): Dictionary of team statistics
- `season` (str): Season identifier
- `week` (int, optional): Week number

**Returns:** None

**Example:**
```python
from ingest_stats import TeamStatsIngestion

ingestion = TeamStatsIngestion()
ingestion.ingest_team_stats(
    team_name="Kansas City Chiefs",
    stats_data={
        'wins': 11,
        'losses': 6,
        'points_per_game': 21.8,
        'points_allowed_per_game': 17.3
    },
    season="2023"
)
```

### NewsIngestion Class

**Module:** `ingest_news.py`

**Description:** Handles ingestion of news articles.

#### Methods

##### `ingest_article(title, content, source, url, published_date=None)`

Ingests a single news article.

**Parameters:**
- `title` (str): Article title
- `content` (str): Article content
- `source` (str): Source publication
- `url` (str): Article URL
- `published_date` (datetime, optional): Publication date

**Returns:** None

**Example:**
```python
from ingest_news import NewsIngestion

ingestion = NewsIngestion()
ingestion.ingest_article(
    title="Patrick Mahomes leads Chiefs to victory",
    content="Full article content here...",
    source="ESPN",
    url="https://espn.com/article"
)
```

##### `scrape_and_ingest_article(url, source)`

Scrapes an article from a URL and ingests it.

**Parameters:**
- `url` (str): Article URL
- `source` (str): Source publication

**Returns:** None

**Example:**
```python
ingestion.scrape_and_ingest_article(
    url="https://espn.com/nfl/story/_/id/12345",
    source="ESPN"
)
```

## RAG Query Interface

### FantasyFootballRAG Class

**Module:** `rag.py`

**Description:** Main query interface for the RAG system.

#### Methods

##### `search_player_stats(query, top_k=5)`

Searches for relevant player statistics.

**Parameters:**
- `query` (str): Search query
- `top_k` (int): Number of results to return (default: 5)

**Returns:** `list` - List of player stat dictionaries with similarity scores

**Example:**
```python
from rag import FantasyFootballRAG

rag = FantasyFootballRAG()
results = rag.search_player_stats("best quarterbacks", top_k=5)
for result in results:
    print(f"{result['player_name']}: {result['similarity']}")
```

##### `search_team_stats(query, top_k=5)`

Searches for relevant team statistics.

**Parameters:**
- `query` (str): Search query
- `top_k` (int): Number of results to return (default: 5)

**Returns:** `list` - List of team stat dictionaries with similarity scores

##### `search_news(query, top_k=5)`

Searches for relevant news articles.

**Parameters:**
- `query` (str): Search query
- `top_k` (int): Number of results to return (default: 5)

**Returns:** `list` - List of news article dictionaries with similarity scores

##### `query(question, include_sources=['players', 'teams', 'news'], top_k=3)`

Main query method that retrieves context and generates an answer.

**Parameters:**
- `question` (str): User's question
- `include_sources` (list): Sources to search (default: ['players', 'teams', 'news'])
- `top_k` (int): Number of results per source (default: 3)

**Returns:** `dict` - Dictionary with keys:
  - `answer` (str): Generated answer
  - `context` (str): Retrieved context used for answer
  - `sources` (dict): Detailed source information

**Example:**
```python
result = rag.query(
    question="Should I start Patrick Mahomes this week?",
    include_sources=['players', 'news'],
    top_k=3
)
print(result['answer'])
```

## Utilities

### Utility Functions

**Module:** `utils.py`

#### `format_player_stats(stats_dict)`

Formats player statistics into a readable string.

**Parameters:**
- `stats_dict` (dict or str): Statistics dictionary or JSON string

**Returns:** `str` - Formatted statistics

#### `validate_stats_data(stats_data)`

Validates statistics data format.

**Parameters:**
- `stats_data` (dict): Statistics dictionary

**Returns:** `bool` - True if valid, False otherwise

#### `parse_season(season_str)`

Parses season string into standardized format.

**Parameters:**
- `season_str` (str): Season string (e.g., "2023" or "2023-2024")

**Returns:** `str` - Standardized season string

#### `calculate_fantasy_points(stats, scoring_system='standard')`

Calculates fantasy points from statistics.

**Parameters:**
- `stats` (dict): Player statistics
- `scoring_system` (str): Scoring system ('standard', 'ppr', 'half-ppr')

**Returns:** `float` - Calculated fantasy points

**Example:**
```python
from utils import calculate_fantasy_points

stats = {
    'rushing_yards': 100,
    'rushing_touchdowns': 1,
    'receptions': 5,
    'receiving_yards': 50
}
points = calculate_fantasy_points(stats, 'ppr')
print(f"Fantasy Points: {points}")
```

## Command Line Interface

**Module:** `cli.py`

### Commands

#### Setup Database

```bash
python cli.py setup
```

Initializes the database and creates all necessary tables.

#### Ingest Player Statistics

```bash
python cli.py ingest-player \
  --name "Patrick Mahomes" \
  --team "Kansas City Chiefs" \
  --position QB \
  --stats '{"passing_yards": 300, "touchdowns": 3}' \
  --season 2023
```

#### Ingest Team Statistics

```bash
python cli.py ingest-team \
  --name "Kansas City Chiefs" \
  --stats '{"wins": 11, "losses": 6}' \
  --season 2023
```

#### Ingest News Article

```bash
python cli.py ingest-news \
  --title "Latest News" \
  --content "Article content here" \
  --source "ESPN" \
  --url "https://espn.com/article"
```

#### Query the System

```bash
python cli.py query "Should I start Patrick Mahomes?" \
  --sources players,news \
  --top-k 3 \
  --show-context
```

## Error Handling

All classes raise exceptions when errors occur. Wrap calls in try-except blocks:

```python
try:
    rag = FantasyFootballRAG()
    result = rag.query("Your question here")
    print(result['answer'])
except Exception as e:
    print(f"Error: {e}")
```

## Performance Considerations

- Use `batch_ingest_*` methods for ingesting multiple items
- Use `generate_embeddings_batch` for multiple embeddings
- Adjust `top_k` parameter based on your needs (higher values = slower but more comprehensive)
- Consider using connection pooling for high-volume applications
