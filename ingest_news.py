"""News article ingestion module."""
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from database import DatabaseManager
from embeddings import EmbeddingService


class NewsIngestion:
    """Handles ingestion of news articles."""
    
    def __init__(self):
        """Initialize news ingestion."""
        self.db_manager = DatabaseManager()
        self.embedding_service = EmbeddingService()
    
    def ingest_article(self, title, content, source, url, published_date=None):
        """
        Ingest a news article into the database.
        
        Args:
            title (str): Article title
            content (str): Article content
            source (str): Article source
            url (str): Article URL
            published_date (datetime): Publication date (optional)
        """
        try:
            # Create text representation for embedding
            article_text = f"Title: {title}\n\nContent: {content}\n\nSource: {source}"
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(article_text)
            
            # Store in database
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO news_articles (title, content, source, url, published_date, embedding)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                title,
                content,
                source,
                url,
                published_date or datetime.now(),
                embedding
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Ingested article: {title}")
        except Exception as e:
            print(f"Error ingesting article: {e}")
            raise
    
    def batch_ingest_articles(self, articles):
        """
        Ingest multiple news articles.
        
        Args:
            articles (list): List of article dictionaries
        """
        for article in articles:
            self.ingest_article(
                article['title'],
                article['content'],
                article['source'],
                article['url'],
                article.get('published_date')
            )
    
    def scrape_and_ingest_article(self, url, source):
        """
        Scrape an article from a URL and ingest it.
        
        Args:
            url (str): Article URL
            source (str): Article source
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract title
            title = soup.find('h1')
            title = title.get_text().strip() if title else "No title"
            
            # Try to extract article content
            # This is a basic implementation - you may need to customize for specific sites
            article_body = soup.find('article') or soup.find('div', class_='content')
            if article_body:
                paragraphs = article_body.find_all('p')
                content = '\n\n'.join([p.get_text().strip() for p in paragraphs])
            else:
                content = "Content extraction failed"
            
            # Ingest the article
            self.ingest_article(title, content, source, url)
            
        except Exception as e:
            print(f"Error scraping article from {url}: {e}")
            raise
