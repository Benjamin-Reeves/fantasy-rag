import psycopg2
from uuid import UUID
import numpy as np

from psycopg2 import extensions
from psycopg2.extras import register_uuid
from pgvector.psycopg2 import register_vector

from core.config import settings
from core.embedding_model import EmbeddingModel
from stats.models import PlayerStatsDocument

class DatabaseManager:
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    connection: extensions.connection = None
    embedding_model: EmbeddingModel
    
    def __init__(self, **data):
        super().__init__(**data)
        print(f"DB_USER: {settings.db_user}")
        self.db_user = settings.db_user
        self.db_password = settings.db_pass
        self.db_name = settings.db_name
        self.db_host = settings.db_host
        self.db_port = settings.db_port
        self.embedding_model = EmbeddingModel()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name
            )
            # Register UUID adapter for psycopg2
            register_uuid()
            # Register vector type for pgvector
            register_vector(self.connection)
            return self.connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
        
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            
    def get_content_(self) -> list[PlayerStatsDocument]:
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM documents;")
        rows = cursor.fetchall()
        documents = []
        for row in rows:
            doc = PlayerStatsDocument(
                id=row[0],
                content=row[1],
                embedding=row[2],
                player_name=row[3],
                player_id=row[4],
                position=row[5],
                team=row[6],
                week=row[7],
                season=row[8],
                fantasy_points_ppr=row[9],
                fantasy_points_std=row[10],
                passing_yards=row[11],
                passing_tds=row[12],
                rushing_yards=row[13],
                rushing_tds=row[14],
                receptions=row[15],
                receiving_yards=row[16],
                receiving_tds=row[17],
                targets=row[18],
                created_at=row[19]
            )
            documents.append(doc)
        cursor.close()
        return documents

    def search(self, query: str) -> list[str]:
        if not self.connection:
            self.connect()

        # Ensure any pending transactions are committed
        self.connection.commit()

        cursor = self.connection.cursor()

        query_embedding = self.embedding_model.encode(query)
        # Convert to numpy array for pgvector
        query_vec = np.array(query_embedding)

        print(f"Query embedding type: {type(query_vec)}, shape: {query_vec.shape}")

        try:
            cursor.execute("""
                SELECT id, content, embedding <=> %s::vector AS distance
                FROM player_stats_documents
                ORDER BY embedding <=> %s::vector
                LIMIT 5;
            """, (query_embedding, query_embedding))
            rows = cursor.fetchall()
            print(f"Query with ORDER BY returned {len(rows)} rows")

            results = []
            for row in rows:
                content = row[1]
                distance = row[2]
                print(f"  Distance: {distance:.4f} - {content[:80]}...")
                results.append(content)
            cursor.close()
            return results
        except Exception as e:
            print(f"Error during search: {e}")
            import traceback
            traceback.print_exc()
            cursor.close()
            return []
        