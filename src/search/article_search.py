"""Article semantic search using vector similarity."""

from typing import Any, List

from services.database import DatabaseManager
from services.embedding_model import EmbeddingModel
from search.models import ArticleResult


class ArticleSearch:
    """Semantic search over article_documents using pgvector."""

    def __init__(
        self,
        database_manager: DatabaseManager | None = None,
        embedding_model: EmbeddingModel | None = None,
    ):
        self.database_manager = database_manager or DatabaseManager()
        self.embedding_model = embedding_model or EmbeddingModel()

    def search(self, query: str, limit: int = 10) -> List[ArticleResult]:
        """
        Perform semantic search over article chunks.

        Args:
            query: Natural language question
            limit: Maximum number of results to return

        Returns:
            List of ArticleResult objects sorted by similarity
        """
        try:
            # Vectorize query
            query_embedding = self.embedding_model.encode(query)

            if not query_embedding or len(query_embedding) == 0:
                print("Warning: Empty embedding generated for query")
                return []

            # Convert embedding to PostgreSQL vector literal
            vector_literal = self.database_manager._to_vector_literal(query_embedding)

            # Construct vector similarity query
            sql = f"""
                SELECT
                    article_url,
                    article_title,
                    chunk_int,
                    content,
                    embedding <=> '{vector_literal}'::vector AS distance
                FROM article_documents
                WHERE embedding <=> '{vector_literal}'::vector < 0.65
                ORDER BY embedding <=> '{vector_literal}'::vector
                LIMIT {min(limit, 50)}
            """

            # Execute query
            raw_results = self.database_manager.search(sql_query=sql)

            # Convert to ArticleResult objects
            return [self._to_article_result(r) for r in raw_results]

        except Exception as e:
            print(f"Error in article search: {e}")
            return []

    def _to_article_result(self, raw: dict[str, Any]) -> ArticleResult:
        """Convert raw database result to ArticleResult object."""
        distance = float(raw.get("distance", 1.0))

        # Convert distance to relevance score (lower distance = higher relevance)
        # Distance is typically 0-2, so we invert and normalize to 0-1
        relevance_score = max(0.0, 1.0 - (distance / 2.0))

        return ArticleResult(
            article_url=raw.get("article_url", ""),
            article_title=raw.get("article_title", ""),
            chunk_int=int(raw.get("chunk_int", 0)),
            content=raw.get("content", ""),
            distance=distance,
            relevance_score=relevance_score,
        )
