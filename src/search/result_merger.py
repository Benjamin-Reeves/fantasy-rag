"""Result merger for combining and ranking stats and article results."""

from typing import List

from search.models import ArticleResult, MergedResults, StatsResult


class ResultMerger:
    """Merge and rank results from stats and article searches."""

    def merge(
        self,
        stats_results: List[StatsResult],
        article_results: List[ArticleResult],
    ) -> MergedResults:
        """
        Merge results from both sources with intelligent ranking.

        Args:
            stats_results: Results from stats search
            article_results: Results from article search

        Returns:
            MergedResults with scored and interleaved results
        """
        # Score stats results (simple scoring for now)
        scored_stats = self._score_stats(stats_results)

        # Article results already have relevance_score from ArticleSearch
        scored_articles = article_results

        # For now, we'll keep them separate but both scored
        # Future enhancement: interleave based on scores
        total = len(scored_stats) + len(scored_articles)

        return MergedResults(
            stats_results=scored_stats,
            article_results=scored_articles,
            total_count=total,
        )

    def _score_stats(self, stats_results: List[StatsResult]) -> List[StatsResult]:
        """
        Score stats results based on relevance.

        For now, uses simple recency-based scoring.
        Future: Could use fantasy points, position relevance, etc.
        """
        if not stats_results:
            return []

        # Find max week/season for normalization
        max_season = max((r.season for r in stats_results), default=0)
        max_week = max((r.week for r in stats_results), default=0)

        scored = []
        for result in stats_results:
            # Simple scoring: recent games get higher scores
            season_score = result.season / max(max_season, 1)
            week_score = result.week / max(max_week, 1)

            # Combine scores (weighted toward recency)
            relevance_score = (season_score * 0.6) + (week_score * 0.4)

            # Update result with score
            result.relevance_score = relevance_score
            scored.append(result)

        # Sort by relevance score (highest first)
        return sorted(scored, key=lambda r: r.relevance_score, reverse=True)
