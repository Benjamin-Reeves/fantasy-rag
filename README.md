# Fantasy Football RAG System

A Retrieval-Augmented Generation (RAG) system for fantasy football that ingests player statistics, team data, and news articles, storing them in a pgvector database for intelligent querying.

## Features

- **Player Statistics Ingestion**: Store and query detailed player statistics
- **Team Statistics Ingestion**: Track team performance metrics
- **News Article Processing**: Ingest and search through fantasy football news
- **Vector Similarity Search**: Fast semantic search using pgvector
- **AI-Powered Responses**: Generate contextual answers using OpenAI GPT

## Architecture

The system consists of several key components:

1. **Database Layer** (`database.py`): PostgreSQL with pgvector extension for vector storage
2. **Embedding Service** (`embeddings.py`): OpenAI embeddings for text vectorization
3. **Data Ingestion** (`ingest_stats.py`, `ingest_news.py`): Modules for ingesting different data types
4. **RAG Query Interface** (`rag.py`): Main query interface that retrieves relevant context and generates answers
5. **Configuration** (`config.py`): Centralized configuration management

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ with pgvector extension
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Benjamin-Reeves/fantasy-rag.git
cd fantasy-rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install PostgreSQL and pgvector:
```bash
# For Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Install pgvector extension
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Edit `.env` with your credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fantasy_football
DB_USER=postgres
DB_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
VECTOR_DIMENSION=1536
```

6. Initialize the database:
```bash
python database.py
```

## Usage

### Basic Example

Run the example script to see the system in action:

```bash
python example.py
```

### Ingesting Player Statistics

```python
from ingest_stats import PlayerStatsIngestion

player_ingestion = PlayerStatsIngestion()

player_ingestion.ingest_player_stats(
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

### Ingesting Team Statistics

```python
from ingest_stats import TeamStatsIngestion

team_ingestion = TeamStatsIngestion()

team_ingestion.ingest_team_stats(
    team_name="Kansas City Chiefs",
    stats_data={
        'wins': 11,
        'losses': 6,
        'points_per_game': 21.8
    },
    season="2023"
)
```

### Ingesting News Articles

```python
from ingest_news import NewsIngestion

news_ingestion = NewsIngestion()

news_ingestion.ingest_article(
    title="Player Update",
    content="Latest news about player performance...",
    source="ESPN",
    url="https://example.com/article"
)
```

### Querying the RAG System

```python
from rag import FantasyFootballRAG

rag = FantasyFootballRAG()

result = rag.query(
    question="How is Patrick Mahomes performing this season?",
    include_sources=['players', 'teams', 'news'],
    top_k=3
)

print(result['answer'])
print(result['context'])
```

## Database Schema

The system uses three main tables:

### player_stats
- `id`: Primary key
- `player_name`: Player name
- `team`: Team name
- `position`: Player position
- `stats_data`: JSON stats data
- `season`: Season identifier
- `week`: Week number (optional)
- `embedding`: Vector embedding (1536 dimensions)
- `created_at`: Timestamp

### team_stats
- `id`: Primary key
- `team_name`: Team name
- `stats_data`: JSON stats data
- `season`: Season identifier
- `week`: Week number (optional)
- `embedding`: Vector embedding (1536 dimensions)
- `created_at`: Timestamp

### news_articles
- `id`: Primary key
- `title`: Article title
- `content`: Article content
- `source`: Article source
- `url`: Article URL
- `published_date`: Publication date
- `embedding`: Vector embedding (1536 dimensions)
- `created_at`: Timestamp

## API Reference

### FantasyFootballRAG

Main RAG query interface.

#### Methods

- `query(question, include_sources=['players', 'teams', 'news'], top_k=3)`: Query the system with a question
- `search_player_stats(query, top_k=5)`: Search for relevant player statistics
- `search_team_stats(query, top_k=5)`: Search for relevant team statistics
- `search_news(query, top_k=5)`: Search for relevant news articles

### PlayerStatsIngestion

Handles player statistics ingestion.

#### Methods

- `ingest_player_stats(player_name, team, position, stats_data, season, week=None)`: Ingest single player stats
- `batch_ingest_players(players_data)`: Ingest multiple player stats

### TeamStatsIngestion

Handles team statistics ingestion.

#### Methods

- `ingest_team_stats(team_name, stats_data, season, week=None)`: Ingest single team stats
- `batch_ingest_teams(teams_data)`: Ingest multiple team stats

### NewsIngestion

Handles news article ingestion.

#### Methods

- `ingest_article(title, content, source, url, published_date=None)`: Ingest single article
- `batch_ingest_articles(articles)`: Ingest multiple articles
- `scrape_and_ingest_article(url, source)`: Scrape and ingest article from URL

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.