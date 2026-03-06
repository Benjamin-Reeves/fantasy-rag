# cli.py

from rich.console import Console

from services.database import DatabaseManager
from services.embedding_model import EmbeddingModel
from services.llm_service import LlmService
from services.query_parser import QueryParser
from formatters.unified_formatter import format_unified_result
from search.article_search import ArticleSearch
from search.result_merger import ResultMerger
from search.stats_search import StatsSearch
from search.unified_search import UnifiedSearchOrchestrator


def main():
    console = Console()
    console.print("[bold cyan]Fantasy RAG CLI[/bold cyan]")
    console.print("Type 'exit', 'quit', or press Ctrl+C to stop")
    console.print("-" * 50)

    # Initialize core services
    database = DatabaseManager()
    parser = QueryParser(database_manager=database)
    llm_service = LlmService()
    embedding_model = EmbeddingModel()

    # Initialize search layer
    stats_search = StatsSearch(parser, database)
    article_search = ArticleSearch(database, embedding_model)
    result_merger = ResultMerger()
    orchestrator = UnifiedSearchOrchestrator(
        stats_search, article_search, result_merger, llm_service
    )

    while True:
        try:
            question = input("\nYour question: ")

            if question.lower() in ["exit", "quit", "q"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if not question.strip():
                continue

            # Execute unified search
            result = orchestrator.search(question, limit=10)

            # Format and display with Rich
            format_unified_result(result, console)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
