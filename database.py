"""Database initialization and management for pgvector."""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config


class DatabaseManager:
    """Manages database connections and initialization."""
    
    def __init__(self):
        """Initialize database manager."""
        self.config = Config()
    
    def create_database(self):
        """Create the database if it doesn't exist."""
        try:
            # Connect to default postgres database to create our database
            conn = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (self.config.DB_NAME,)
            )
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(f'CREATE DATABASE {self.config.DB_NAME}')
                print(f"Database '{self.config.DB_NAME}' created successfully.")
            else:
                print(f"Database '{self.config.DB_NAME}' already exists.")
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error creating database: {e}")
            raise
    
    def initialize_pgvector(self):
        """Initialize pgvector extension and create tables."""
        try:
            conn = psycopg2.connect(self.config.db_connection_string)
            cursor = conn.cursor()
            
            # Enable pgvector extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
            
            # Create player stats table
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS player_stats (
                    id SERIAL PRIMARY KEY,
                    player_name VARCHAR(255) NOT NULL,
                    team VARCHAR(100),
                    position VARCHAR(50),
                    stats_data TEXT,
                    season VARCHAR(20),
                    week INTEGER,
                    embedding vector({self.config.VECTOR_DIMENSION}),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create team stats table
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS team_stats (
                    id SERIAL PRIMARY KEY,
                    team_name VARCHAR(100) NOT NULL,
                    stats_data TEXT,
                    season VARCHAR(20),
                    week INTEGER,
                    embedding vector({self.config.VECTOR_DIMENSION}),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create news articles table
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS news_articles (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(500),
                    content TEXT,
                    source VARCHAR(255),
                    url VARCHAR(1000),
                    published_date TIMESTAMP,
                    embedding vector({self.config.VECTOR_DIMENSION}),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for vector similarity search
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS player_stats_embedding_idx 
                ON player_stats USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS team_stats_embedding_idx 
                ON team_stats USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS news_articles_embedding_idx 
                ON news_articles USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("pgvector initialized and tables created successfully.")
        except Exception as e:
            print(f"Error initializing pgvector: {e}")
            raise
    
    def get_connection(self):
        """Get a database connection."""
        return psycopg2.connect(self.config.db_connection_string)


if __name__ == "__main__":
    db = DatabaseManager()
    db.create_database()
    db.initialize_pgvector()
