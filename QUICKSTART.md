# Fantasy Football RAG System - Quick Start Guide

## What Was Built

A complete Retrieval-Augmented Generation (RAG) system for fantasy football that allows you to:

1. **Ingest Data**: Store player statistics, team statistics, and news articles
2. **Vector Search**: Use pgvector for semantic similarity search
3. **AI Queries**: Ask natural language questions and get intelligent answers based on your data

## System Components

### Core Modules (1312 lines of Python code)

1. **config.py** - Configuration management from environment variables
2. **database.py** - PostgreSQL with pgvector initialization and management
3. **embeddings.py** - OpenAI embedding generation service
4. **ingest_stats.py** - Player and team statistics ingestion
5. **ingest_news.py** - News article ingestion with web scraping support
6. **rag.py** - Main RAG query interface with semantic search
7. **utils.py** - Utility functions (formatting, validation, fantasy point calculation)
8. **cli.py** - Command-line interface for all operations
9. **example.py** - Interactive example script with sample data
10. **test_fantasy_rag.py** - Unit tests for utility functions

### Supporting Files

- **requirements.txt** - Python dependencies
- **.env.example** - Environment variable template
- **.gitignore** - Git ignore configuration
- **docker-compose.yml** - Easy PostgreSQL + pgvector setup
- **setup.sh** - Automated setup script
- **README.md** - Comprehensive documentation
- **API_DOCS.md** - Complete API reference

## Quick Start (3 Steps)

### 1. Setup Environment

```bash
# Run the automated setup script
./setup.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fantasy_football
DB_USER=postgres
DB_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

### 3. Initialize Database

```bash
# Option A: Using Docker (easiest)
docker-compose up -d
python database.py

# Option B: Using existing PostgreSQL
# Make sure pgvector extension is installed
python database.py
```

## Usage Examples

### Try the Interactive Example

```bash
python example.py
```

This will let you:
- Ingest sample player, team, and news data
- Query the system with example questions

### Use the Command Line Interface

```bash
# Ingest a player
python cli.py ingest-player \
  --name "Patrick Mahomes" \
  --team "Kansas City Chiefs" \
  --position QB \
  --stats '{"passing_yards": 300, "touchdowns": 3}' \
  --season 2023

# Query the system
python cli.py query "How is Patrick Mahomes performing?" --show-context
```

### Use as a Python Library

```python
from rag import FantasyFootballRAG

# Initialize the RAG system
rag = FantasyFootballRAG()

# Ask a question
result = rag.query(
    question="Should I start Christian McCaffrey this week?",
    include_sources=['players', 'news'],
    top_k=3
)

print(result['answer'])
```

## Database Schema

Three main tables store vectorized data:

### player_stats
- Player name, team, position
- Statistics as JSON
- 1536-dimension vector embedding
- Season and week information

### team_stats
- Team name
- Statistics as JSON
- 1536-dimension vector embedding
- Season and week information

### news_articles
- Title, content, source, URL
- 1536-dimension vector embedding
- Publication date

All tables have IVFFlat indexes for fast vector similarity search.

## Architecture

```
User Query
    ↓
FantasyFootballRAG.query()
    ↓
Generate Query Embedding (OpenAI)
    ↓
Vector Similarity Search (pgvector)
    ├─→ Search player_stats
    ├─→ Search team_stats
    └─→ Search news_articles
    ↓
Retrieve Top-K Results
    ↓
Construct Context
    ↓
Generate Answer (GPT-3.5-turbo)
    ↓
Return Answer + Context + Sources
```

## Data Ingestion Flow

```
Raw Data (CSV, API, Web Scraping)
    ↓
Ingestion Module (ingest_stats.py / ingest_news.py)
    ↓
Format as Text
    ↓
Generate Embedding (OpenAI)
    ↓
Store in PostgreSQL with pgvector
```

## Key Features

✅ **Vector Similarity Search**: Find relevant data based on semantic meaning, not just keywords
✅ **Multi-Source Retrieval**: Combine player stats, team stats, and news in one query
✅ **Flexible Data Model**: Store any statistics as JSON
✅ **Batch Operations**: Efficiently ingest multiple records
✅ **CLI and Library**: Use via command line or import as Python package
✅ **Docker Support**: Easy database setup with Docker Compose
✅ **Web Scraping**: Automatically extract content from news URLs
✅ **Fantasy Points Calculator**: Built-in fantasy point calculation (Standard, PPR, Half-PPR)

## Performance Tips

- Use batch ingestion methods for multiple records
- Adjust `top_k` parameter based on needs (lower = faster)
- Consider connection pooling for high-volume applications
- Use Docker Compose for consistent development environment

## Testing

```bash
# Run unit tests
python -m unittest test_fantasy_rag.py -v
```

Tests cover utility functions, configuration, and embedding service.

## Next Steps

1. **Customize Data Sources**: Modify ingestion modules to pull from your preferred APIs
2. **Add More Stats**: Extend the stats dictionaries with additional metrics
3. **Tune Vector Search**: Adjust IVFFlat index parameters for your data size
4. **Build UI**: Create a web interface using Flask or FastAPI
5. **Add Caching**: Implement Redis for frequently asked queries
6. **Expand Scoring**: Add more fantasy point calculation systems

## Troubleshooting

**"No module named 'dotenv'"**: Run `pip install -r requirements.txt`

**"Database connection failed"**: Check your `.env` file and ensure PostgreSQL is running

**"pgvector extension not found"**: Install pgvector extension in PostgreSQL

**"OpenAI API error"**: Verify your `OPENAI_API_KEY` in `.env` file

## Resources

- **PostgreSQL**: https://www.postgresql.org/
- **pgvector**: https://github.com/pgvector/pgvector
- **OpenAI Embeddings**: https://platform.openai.com/docs/guides/embeddings
- **LangChain**: https://python.langchain.com/

## License

MIT License - See repository for details

---

**Built with**: Python 3.8+, PostgreSQL, pgvector, OpenAI API, LangChain

**Total Lines of Code**: 1312 Python lines + documentation
