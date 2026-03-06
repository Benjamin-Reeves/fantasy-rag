"""Data models for search results and unified search responses."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class StatsResult:
    """Result from player stats search."""
    player_name: str
    position: str
    team: str
    week: int
    season: int
    fantasy_points_ppr: Optional[float]
    content: str
    relevance_score: float = 0.0


@dataclass
class ArticleResult:
    """Result from article semantic search."""
    article_url: str
    article_title: str
    chunk_int: int
    content: str
    distance: float  # Vector similarity distance
    relevance_score: float = 0.0


@dataclass
class MergedResults:
    """Combined results from stats and articles."""
    stats_results: List[StatsResult]
    article_results: List[ArticleResult]
    total_count: int


@dataclass
class UnifiedSearchResult:
    """Complete unified search result with LLM synthesis."""
    query: str
    merged_results: MergedResults
    synthesized_answer: str
