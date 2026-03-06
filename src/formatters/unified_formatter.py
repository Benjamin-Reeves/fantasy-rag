"""Rich formatter for unified search results."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from formatters.article_formatter import format_article_results
from formatters.stats_formatter import format_stats_results
from search.models import UnifiedSearchResult


def format_unified_result(result: UnifiedSearchResult, console: Console):
    """
    Display unified search result with Rich formatting.

    Args:
        result: UnifiedSearchResult object
        console: Rich Console instance
    """
    # Query header
    console.print(f"\n[bold cyan]Query:[/bold cyan] {result.query}\n")

    # Stats section
    if result.merged_results.stats_results:
        console.print("[bold green]📊 Player Stats:[/bold green]")
        stats_table = format_stats_results(result.merged_results.stats_results)
        console.print(stats_table)
        console.print()
    else:
        console.print("[dim]No player stats found for this query.[/dim]\n")

    # Articles section
    if result.merged_results.article_results:
        console.print("[bold blue]📰 Related Articles:[/bold blue]")
        article_panels = format_article_results(result.merged_results.article_results)
        for panel in article_panels:
            console.print(panel)
        console.print()
    else:
        console.print("[dim]No articles found for this query.[/dim]\n")

    # LLM synthesis
    if result.synthesized_answer:
        console.print("[bold magenta]🤖 Analysis:[/bold magenta]")
        analysis_panel = Panel(
            Markdown(result.synthesized_answer),
            border_style="magenta",
            padding=(1, 2),
        )
        console.print(analysis_panel)
    else:
        console.print("[dim]No analysis available.[/dim]")
