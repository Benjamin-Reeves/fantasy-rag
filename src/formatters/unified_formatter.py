"""Rich formatter for unified search results."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

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
