"""Unified search orchestrator for parallel stats and article search."""

from typing import List

from services.llm_service import LlmService
from search.article_search import ArticleSearch
from search.models import ArticleResult, MergedResults, StatsResult, UnifiedSearchResult
from search.result_merger import ResultMerger
from search.stats_search import StatsSearch


class UnifiedSearchOrchestrator:
    def __init__(
        self,
        stats_search: StatsSearch | None = None,
        article_search: ArticleSearch | None = None,
        result_merger: ResultMerger | None = None,
        llm_service: LlmService | None = None,
    ):
        self.stats_search = stats_search or StatsSearch()
        self.article_search = article_search or ArticleSearch()
        self.result_merger = result_merger or ResultMerger()
        self.llm_service = llm_service or LlmService()

    def search(
        self,
        query: str,
        limit: int = 10,
        stats_only: bool = False,
        articles_only: bool = False,
    ) -> UnifiedSearchResult:
        """
        Execute unified search across both data sources.

        Args:
            query: Natural language question
            limit: Maximum results per source
            stats_only: Only search stats (skip articles)
            articles_only: Only search articles (skip stats)

        Returns:
            UnifiedSearchResult with merged results and LLM synthesis
        """
        stats_results: List[StatsResult] = []
        article_results: List[ArticleResult] = []
        
        if not articles_only:
            stats_results = self._search_stats(query, limit)

        if not stats_only:
            article_results = self._search_articles(query, limit)

        # Merge results
        merged_results = self.result_merger.merge(stats_results, article_results)

        # Generate LLM synthesis
        synthesized_answer = self._synthesize_answer(query, merged_results)

        return UnifiedSearchResult(
            query=query,
            merged_results=merged_results,
            synthesized_answer=synthesized_answer,
        )

    def _search_stats(self, query: str, limit: int) -> List[StatsResult]:
        """Execute stats search (for parallel execution)."""
        try:
            return self.stats_search.search(query, limit)
        except Exception as e:
            print(f"Stats search failed: {e}")
            return []

    def _search_articles(self, query: str, limit: int) -> List[ArticleResult]:
        """Execute article search (for parallel execution)."""
        try:
            return self.article_search.search(query, limit)
        except Exception as e:
            print(f"Article search failed: {e}")
            return []

    def _synthesize_answer(self, query: str, merged_results: MergedResults) -> str:
        """Generate unified answer using LLM."""
        # Format stats data
        stats_data = ""
        if merged_results.stats_results:
            stats_data = "\n\n".join(
                [
                    f"- {r.player_name} ({r.position}, {r.team}): Week {r.week}, Season {r.season}"
                    + (f" - {r.fantasy_points_ppr:.1f} PPR points" if r.fantasy_points_ppr is not None else "")
                    + (f" - {r.content}" if r.content else "")
                    for r in merged_results.stats_results[:5]  # Limit for token efficiency
                ]
            )
        else:
            stats_data = "No player stats found for this query."

        # Format articles data
        articles_data = ""
        if merged_results.article_results:
            articles_data = "\n\n".join(
                [
                    f"- {r.article_title} ({r.article_url}):\n  {r.content[:300]}..."
                    for r in merged_results.article_results[:3]  # Limit for token efficiency
                ]
            )
        else:
            articles_data = "No news articles found for this query."

        # Build synthesis prompt
        prompt = f"""You are a fantasy football analytics assistant with access to both player statistics and news articles.

User Query: {query}

Player Statistics Data:
{stats_data}

News Articles Context:
{articles_data}

Provide a comprehensive, natural language answer combining insights from both sources. Be specific and cite relevant statistics and articles. If data is limited, acknowledge that and work with what's available."""

        try:
            return self.llm_service.complete_message(prompt, max_tokens=1000)
        except Exception as e:
            print(f"LLM synthesis failed: {e}")
            return "Unable to generate synthesized response. Please review the raw results above."
