"""Standalone script for ingesting news articles into the database."""

import sys

from news_articles.ingestion import NewsArticleIngestion


def main():
    """
    Ingest news articles from URLs.

    Usage:
        python -m scripts.ingest_articles <url1> <url2> ...
    """
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.ingest_articles <url1> <url2> ...")
        print("\nExample:")
        print("  python -m scripts.ingest_articles https://espn.com/article1 https://espn.com/article2")
        sys.exit(1)

    urls = sys.argv[1:]
    print(f"Ingesting {len(urls)} article(s)...")

    ingestion = NewsArticleIngestion()
    stats = ingestion.ingest_urls(urls)

    print("\n" + "=" * 50)
    print("Ingestion Complete!")
    print("=" * 50)
    print(f"URLs requested: {stats['urls_requested']}")
    print(f"Pages scraped: {stats['pages_scraped']}")
    print(f"Chunks created: {stats['chunks_created']}")
    print(f"Chunks inserted: {stats['chunks_inserted']}")


if __name__ == "__main__":
    main()
