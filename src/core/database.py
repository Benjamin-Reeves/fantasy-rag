import re
from typing import Any

import psycopg2
from psycopg2 import sql
from psycopg2 import extensions
from psycopg2.extras import Json, execute_values, register_uuid

from core.config import settings


class DatabaseManager:
    """Thin Postgres wrapper for ingestion writes and read-only query execution."""

    def __init__(self):
        self.db_user = settings.db_user
        self.db_password = settings.db_pass
        self.db_name = settings.db_name
        self.db_host = settings.db_host
        self.db_port = settings.db_port
        self.connection: extensions.connection | None = None
        self._connection_read_only: bool | None = None

    def connect(self, read_only: bool = False) -> extensions.connection | None:
        if self.connection and self.connection.closed == 0 and self._connection_read_only == read_only:
            return self.connection

        self.disconnect()

        try:
            self.connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
            )
            register_uuid()
            self.connection.set_session(readonly=read_only, autocommit=read_only)
            self._connection_read_only = read_only
            return self.connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None
            self._connection_read_only = None
            return None

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
        self.connection = None
        self._connection_read_only = None

    def get_table_columns(self, table_name: str = "player_stats_documents", schema: str = "public") -> str:
        connection = self.connect(read_only=True)
        if not connection:
            return ""

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    (schema, table_name)
                )
                columns = cursor.fetchall()
                if not columns:
                    return ""

                # Format as simple list: "column_name: data_type"
                return "\n".join([f"{col[0]}: {col[1]}" for col in columns])
            except Exception as e:
                print(f"Error retrieving table schema for {schema}.{table_name}: {e}")
                return ""

    def search(self, sql_query: str) -> list[dict[str, Any]]:
        """Execute a single read-only SELECT query and return rows as dicts."""
        connection = self.connect(read_only=True)
        if not connection:
            return []

        try:
            safe_query = self._normalize_select(sql_query)
        except ValueError as e:
            print(f"Invalid SQL query: {e}")
            return []

        with connection.cursor() as cursor:
            try:
                cursor.execute(safe_query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description or []]
                return [dict(zip(columns, row)) for row in rows]
            except Exception as e:
                print(f"Error during read-only search execution: {e}")
                return []

    def upsert_blog_chunks(
        self,
        chunks: list[dict[str, Any]],
        table_name: str = "blog_documents",
        schema: str = "public",
    ) -> int:
        if not chunks:
            return 0

        connection = self.connect(read_only=False)
        if not connection:
            return 0

        insert_query = sql.SQL(
            """
            INSERT INTO {}.{} (
                source_url,
                canonical_url,
                title,
                chunk_index,
                content,
                embedding,
                metadata
            )
            VALUES %s
            ON CONFLICT (canonical_url, chunk_index) DO UPDATE SET
                source_url = EXCLUDED.source_url,
                title = EXCLUDED.title,
                content = EXCLUDED.content,
                embedding = EXCLUDED.embedding,
                metadata = EXCLUDED.metadata;
            """
        ).format(sql.Identifier(schema), sql.Identifier(table_name))

        values: list[tuple[Any, ...]] = []
        for chunk in chunks:
            try:
                vector_literal = self._to_vector_literal(chunk.get("embedding", []))
                values.append(
                    (
                        chunk.get("source_url", ""),
                        chunk.get("canonical_url", ""),
                        chunk.get("title"),
                        int(chunk.get("chunk_index", 0)),
                        chunk.get("content", ""),
                        vector_literal,
                        Json(chunk.get("metadata", {})),
                    )
                )
            except Exception as e:
                print(f"Skipping invalid blog chunk row: {e}")

        if not values:
            return 0

        try:
            with connection.cursor() as cursor:
                execute_values(
                    cursor,
                    insert_query.as_string(connection),
                    values,
                    template="(%s, %s, %s, %s, %s, %s::vector, %s)",
                    page_size=250,
                )
            connection.commit()
            return len(values)
        except Exception as e:
            connection.rollback()
            print(f"Error upserting blog chunks into {schema}.{table_name}: {e}")
            return 0

    @staticmethod
    def _normalize_select(sql_query: str) -> str:
        if not sql_query or not sql_query.strip():
            raise ValueError("SQL query is required")

        cleaned = DatabaseManager._strip_markdown_fences(sql_query).strip().rstrip(";").strip()
        if not cleaned:
            raise ValueError("SQL query is empty")

        if ";" in cleaned:
            raise ValueError("Only a single SQL statement is allowed")

        if not re.match(r"(?is)^select\b", cleaned):
            raise ValueError("Only SELECT statements are allowed")

        return f"{cleaned};"

    @staticmethod
    def _strip_markdown_fences(text: str) -> str:
        stripped = text.strip()
        if not stripped.startswith("```"):
            return stripped

        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()

    @staticmethod
    def _to_vector_literal(values: list[float]) -> str:
        if not values:
            raise ValueError("Embedding vector cannot be empty.")
        return "[" + ",".join(str(float(value)) for value in values) + "]"
