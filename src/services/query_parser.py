import re

from services.database import DatabaseManager
from services.llm_service import LlmService


class QueryParser:
    """Generate a safe SQL SELECT statement for player_stats_documents using an LLM."""

    _PROMPT_TEMPLATE = """You are a PostgreSQL query generator for fantasy football analysis.

You are given a user question and the live table DDL.
Return exactly one SQL statement.

Hard requirements:
- Output SQL only. No markdown, no commentary.
- Return exactly one statement.
- The statement must start with SELECT.
- Query only public.player_stats_documents (or player_stats_documents).
- Never use write operations (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE).
- Include LIMIT <= 200.
- Use only columns that exist in the table details.
- Use ILIKE for case-insensitive text matching when matching player/team names.
- If the question is vague, return a sensible default query sorted by season DESC, week DESC with LIMIT 25.

Query patterns to recognize:
1. AGGREGATION queries (best/top player in a season/multi-week period):
   - Questions like "best RB in 2019", "top WR in 2023", "highest scoring QB this season"
   - Use GROUP BY player_name (and optionally position, team if needed)
   - Use SUM() for cumulative stats (rushing_yards, receiving_yards, receptions, targets, etc.)
   - Use AVG() only if explicitly asking for averages
   - Use COUNT(*) or COUNT(DISTINCT week) if asking about games played
   - ORDER BY the most relevant aggregated stat (usually SUM(fantasy_points_ppr) or the stat in question)
   - Example: SELECT player_name, position, team, SUM(rushing_yards) as total_rushing_yards, SUM(rushing_tds) as total_rushing_tds, SUM(fantasy_points_ppr) as total_fantasy_points FROM player_stats_documents WHERE season = 2019 AND position = 'RB' GROUP BY player_name, position, team ORDER BY total_fantasy_points DESC LIMIT 10;

2. DETAIL queries (specific week/game performance):
   - Questions like "how did player X do in week 5", "show me week 1 stats"
   - Do NOT use GROUP BY or aggregation functions
   - Select individual game rows with relevant columns
   - ORDER BY as appropriate (usually by fantasy_points_ppr DESC or week)
   - Example: SELECT player_name, team, week, fantasy_points_ppr, rushing_yards, rushing_tds FROM player_stats_documents WHERE player_name ILIKE '%name%' AND season = 2023 ORDER BY week;

3. COMPARISON queries (comparing players):
   - Questions like "compare player X and player Y", "who is better between X and Y"
   - Determine if comparing season totals (use GROUP BY) or week-by-week (no GROUP BY)
   - Use WHERE player_name ILIKE '%X%' OR player_name ILIKE '%Y%'
   - For season comparisons, aggregate with GROUP BY player_name

User Question:
{query}

Table details:
{details}
"""

    _FALLBACK_QUERY = (
        "SELECT player_name, position, team, week, season, fantasy_points_ppr, "
        "fantasy_points_std, content "
        "FROM player_stats_documents "
        "ORDER BY season DESC, week DESC "
        "LIMIT 25;"
    )

    _DISALLOWED_SQL_PATTERN = re.compile(
        r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|comment|copy|vacuum|analyze|call|do|execute)\b",
        flags=re.IGNORECASE,
    )

    def __init__(self, database_manager: DatabaseManager | None = None):
        self.llm_service = LlmService()
        self.database_manager = database_manager or DatabaseManager()

    def build_select_query(self, query: str) -> str:
        table_details = self.database_manager.get_table_columns(
            table_name="player_stats_documents",
            schema="public",
        )
        if not table_details:
            raise ValueError("Failed to retrieve table details.")

        prompt = self._PROMPT_TEMPLATE.format(query=query.strip(), details=table_details)
        raw_response = self.llm_service.complete_message(prompt=prompt, max_tokens=500, temperature=0.0)
        return self._normalize_and_validate_query(raw_response)

    def _normalize_and_validate_query(self, raw_sql: str) -> str:
        if not raw_sql:
            return self._FALLBACK_QUERY

        cleaned = self._strip_markdown_fences(raw_sql).strip().rstrip(";").strip()
        if not cleaned:
            return self._FALLBACK_QUERY

        # Disallow stacked statements.
        if ";" in cleaned:
            return self._FALLBACK_QUERY

        if not re.match(r"(?is)^select\b", cleaned):
            return self._FALLBACK_QUERY

        if self._DISALLOWED_SQL_PATTERN.search(cleaned):
            return self._FALLBACK_QUERY

        if not re.search(r"(?is)\bfrom\s+(?:public\.)?\"?player_stats_documents\"?\b", cleaned):
            return self._FALLBACK_QUERY

        cleaned = self._enforce_limit(cleaned)
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
    def _enforce_limit(sql: str) -> str:
        limit_match = re.search(r"(?is)\blimit\s+(\d+)\b", sql)
        if not limit_match:
            return f"{sql} LIMIT 25"

        limit_value = int(limit_match.group(1))
        if limit_value <= 200:
            return sql

        return re.sub(r"(?is)\blimit\s+\d+\b", "LIMIT 200", sql, count=1)
