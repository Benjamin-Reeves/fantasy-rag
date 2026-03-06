"""Rich formatter for player stats results."""

from typing import List

from rich.table import Table

from search.models import StatsResult


def format_stats_results(results: List[StatsResult]) -> Table:
    """
    Format stats results as a Rich table.

    Args:
        results: List of StatsResult objects

    Returns:
        Rich Table object
    """
    table = Table(
        title="Player Stats",
        show_header=True,
        header_style="bold magenta",
        show_lines=False,
    )

    # Add columns
    table.add_column("Player", style="cyan", no_wrap=True)
    table.add_column("Pos", style="blue", width=4)
    table.add_column("Team", style="green", width=4)
    table.add_column("Week", justify="right", width=5)
    table.add_column("Season", justify="right", width=6)
    table.add_column("PPR Pts", justify="right", style="yellow", width=8)

    # Add rows
    for result in results:
        ppr_points = (
            f"{result.fantasy_points_ppr:.1f}"
            if result.fantasy_points_ppr is not None
            else "N/A"
        )

        table.add_row(
            result.player_name,
            result.position,
            result.team,
            str(result.week),
            str(result.season),
            ppr_points,
        )

    return table
