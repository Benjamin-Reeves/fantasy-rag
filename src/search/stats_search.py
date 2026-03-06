"""Stats search wrapper around QueryParser and DatabaseManager."""

from typing import Any, List

from services.database import DatabaseManager
from services.query_parser import QueryParser
from search.models import StatsResult


class StatsSearch:
    """Search player_stats_documents using LLM-generated SQL."""

    def __init__(
        self,
        query_parser: QueryParser | None = None,
        database_manager: DatabaseManager | None = None,
    ):
        self.query_parser = query_parser or QueryParser()
        self.database_manager = database_manager or DatabaseManager()

    def search(self, query: str, limit: int = 10) -> List[StatsResult]:
        """
        Search player stats using natural language query.

        Args:
            query: Natural language question
            limit: Maximum number of results to return

        Returns:
            List of StatsResult objects
        """
        try:
            # Generate SQL query using LLM
            sql = self.query_parser.build_select_query(query)

            # Execute query
            raw_results = self.database_manager.search(sql_query=sql)

            # Convert to StatsResult objects
            results = [self._to_stats_result(r) for r in raw_results]

            # Limit results
            return results[:limit]

        except Exception as e:
            print(f"Error in stats search: {e}")
            return []

    def _to_stats_result(self, raw: dict[str, Any]) -> StatsResult:
        """Convert raw database result to StatsResult object."""
        # Build content from available stats if not provided
        content = raw.get("content", "")
        if not content:
            # Aggregation queries don't include content, so build from stats
            stats_parts = []

            # Check for aggregated stats (common in GROUP BY queries)
            for key in ["total_rushing_yards", "total_receiving_yards", "total_fantasy_points"]:
                if key in raw and raw[key] is not None:
                    display_name = key.replace("total_", "").replace("_", " ").title()
                    stats_parts.append(f"{display_name}: {raw[key]}")

            # If no aggregated stats, try individual game stats
            if not stats_parts:
                stat_fields = {
                    "rushing_yards": "Rush Yds",
                    "rushing_tds": "Rush TDs",
                    "receiving_yards": "Rec Yds",
                    "receiving_tds": "Rec TDs",
                    "receptions": "Rec",
                    "targets": "Targets",
                    "passing_yards": "Pass Yds",
                    "passing_tds": "Pass TDs",
                }
                for field, label in stat_fields.items():
                    if field in raw and raw[field] is not None and raw[field] != 0:
                        stats_parts.append(f"{label}: {raw[field]}")

            content = ", ".join(stats_parts) if stats_parts else ""

        return StatsResult(
            player_name=raw.get("player_name", ""),
            position=raw.get("position", ""),
            team=raw.get("team", ""),
            week=int(raw.get("week", 0)),
            season=int(raw.get("season", 0)),
            fantasy_points_ppr=float(raw["fantasy_points_ppr"])
            if raw.get("fantasy_points_ppr") is not None
            else None,
            content=content,
            relevance_score=0.0,  # TODO: Implement relevance scoring
        )
