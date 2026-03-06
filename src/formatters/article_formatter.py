"""Rich formatter for article results."""

from typing import List

from rich.markdown import Markdown
from rich.panel import Panel

from search.models import ArticleResult


def format_article_results(results: List[ArticleResult]) -> List[Panel]:
    """
    Format article results as Rich panels.

    Args:
        results: List of ArticleResult objects

    Returns:
        List of Rich Panel objects
    """
    panels = []

    for i, result in enumerate(results, 1):
        # Truncate content for preview
        max_length = 300
        if len(result.content) > max_length:
            preview = result.content[:max_length] + "..."
        else:
            preview = result.content

        # Create markdown content
        content = Markdown(preview)

        # Create panel with title and metadata
        panel = Panel(
            content,
            title=f"[bold blue]{result.article_title}[/bold blue]",
            subtitle=f"[dim]{result.article_url} (chunk {result.chunk_int})[/dim]",
            border_style="blue",
            padding=(1, 2),
        )

        panels.append(panel)

    return panels
