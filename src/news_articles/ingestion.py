from datetime import date, datetime
from typing import Any

from psycopg2.extras import execute_values

from core.database import DatabaseManager
from core.scraper import WebsiteScraper
from news_articles.chunking import NewsArticleChunker
from news_articles.embedding import NewsArticleEmbedder


class NewsArticleIngestion:
    """Pipeline: scrape content, chunk text, embed chunks, and store in Postgres."""

    def __init__(
        self,
        database_manager: DatabaseManager | None = None,
        scraper: WebsiteScraper | None = None,
        chunker: NewsArticleChunker | None = None,
        embedder: NewsArticleEmbedder | None = None,
    ):
        self.database_manager = database_manager or DatabaseManager()
        self.scraper = scraper or WebsiteScraper()
        self.chunker = chunker or NewsArticleChunker()
        self.embedder = embedder or NewsArticleEmbedder()

    def ingest_urls(self, urls: list[str]) -> dict[str, int]:
        normalized_urls = [url.strip() for url in urls if url and url.strip()]
        if not normalized_urls:
            return {"urls_requested": 0, "pages_scraped": 0, "chunks_created": 0, "chunks_inserted": 0}

        connection = self.database_manager.connect(read_only=False)
        if not connection:
            return {
                "urls_requested": len(normalized_urls),
                "pages_scraped": 0,
                "chunks_created": 0,
                "chunks_inserted": 0,
            }

        pages_scraped = 0
        chunks_created = 0
        rows_to_insert: list[tuple[Any, ...]] = []

        for url in normalized_urls:
            page = self.scraper.scrape_page(url)
            if not page:
                continue

            pages_scraped += 1
            chunks = self.chunker.chunk_text(page.content)
            embeddings = self.embedder.embed_chunks(chunks)
            published_date = self._parse_published_date(page.metadata.get("published_time"))
            author = page.metadata.get("author")

            for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                if not embedding:
                    continue

                chunks_created += 1
                rows_to_insert.append(
                    (
                        chunk,
                        self.database_manager._to_vector_literal(embedding),
                        page.canonical_url,
                        page.title[:500] if page.title else None,
                        str(author)[:200] if author else None,
                        published_date,
                        None,
                        None,
                        chunk_index,
                    )
                )

        if not rows_to_insert:
            return {
                "urls_requested": len(normalized_urls),
                "pages_scraped": pages_scraped,
                "chunks_created": chunks_created,
                "chunks_inserted": 0,
            }

        insert_query = """
            INSERT INTO article_documents (
                content,
                embedding,
                article_url,
                article_title,
                article_author,
                published_date,
                mentioned_players,
                mentioned_teams,
                chunk_int
            )
            VALUES %s;
        """

        try:
            with connection.cursor() as cursor:
                execute_values(
                    cursor,
                    insert_query,
                    rows_to_insert,
                    template="(%s, %s::vector, %s, %s, %s, %s, %s, %s, %s)",
                    page_size=250,
                )
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error inserting article chunks: {e}")
            return {
                "urls_requested": len(normalized_urls),
                "pages_scraped": pages_scraped,
                "chunks_created": chunks_created,
                "chunks_inserted": 0,
            }

        return {
            "urls_requested": len(normalized_urls),
            "pages_scraped": pages_scraped,
            "chunks_created": chunks_created,
            "chunks_inserted": len(rows_to_insert),
        }

    def ingest_site(self, start_url: str, max_pages: int = 10, follow_links: bool = True) -> dict[str, int]:
        pages = self.scraper.scrape_site(start_url=start_url, max_pages=max_pages, follow_links=follow_links)
        return self.ingest_urls([page.source_url for page in pages])

    def query_similar_content(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Semantic retrieval over stored article chunks."""
        safe_limit = max(1, min(int(limit), 50))
        query_embedding = self.embedder.embed_text(query)
        if not query_embedding:
            return []

        try:
            vector_literal = self.database_manager._to_vector_literal(query_embedding)
        except ValueError:
            return []

        sql_query = f"""
            SELECT
                article_url,
                article_title,
                chunk_int,
                content,
                embedding <=> '{vector_literal}'::vector AS distance
            FROM article_documents
            ORDER BY embedding <=> '{vector_literal}'::vector
            LIMIT {safe_limit}
        """
        return self.database_manager.search(sql_query=sql_query)

    @staticmethod
    def _parse_published_date(raw_published_time: Any) -> date | None:
        if not raw_published_time:
            return None

        value = str(raw_published_time).strip()
        if not value:
            return None

        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            pass

        if len(value) >= 10:
            try:
                return date.fromisoformat(value[:10])
            except ValueError:
                return None

        return None
