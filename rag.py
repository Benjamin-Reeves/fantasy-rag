"""RAG query interface for fantasy football system."""
from openai import OpenAI
from database import DatabaseManager
from embeddings import EmbeddingService
from config import Config


class FantasyFootballRAG:
    """RAG system for fantasy football queries."""
    
    def __init__(self):
        """Initialize RAG system."""
        self.db_manager = DatabaseManager()
        self.embedding_service = EmbeddingService()
        self.config = Config()
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
    
    def search_player_stats(self, query, top_k=5):
        """
        Search for relevant player statistics.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            list: List of relevant player statistics
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Search in database
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT player_name, team, position, stats_data, season, week,
                   1 - (embedding <=> %s::vector) as similarity
            FROM player_stats
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top_k))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [
            {
                'player_name': row[0],
                'team': row[1],
                'position': row[2],
                'stats_data': row[3],
                'season': row[4],
                'week': row[5],
                'similarity': float(row[6])
            }
            for row in results
        ]
    
    def search_team_stats(self, query, top_k=5):
        """
        Search for relevant team statistics.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            list: List of relevant team statistics
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Search in database
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT team_name, stats_data, season, week,
                   1 - (embedding <=> %s::vector) as similarity
            FROM team_stats
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top_k))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [
            {
                'team_name': row[0],
                'stats_data': row[1],
                'season': row[2],
                'week': row[3],
                'similarity': float(row[4])
            }
            for row in results
        ]
    
    def search_news(self, query, top_k=5):
        """
        Search for relevant news articles.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            list: List of relevant news articles
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Search in database
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title, content, source, url, published_date,
                   1 - (embedding <=> %s::vector) as similarity
            FROM news_articles
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top_k))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [
            {
                'title': row[0],
                'content': row[1],
                'source': row[2],
                'url': row[3],
                'published_date': row[4],
                'similarity': float(row[5])
            }
            for row in results
        ]
    
    def query(self, question, include_sources=['players', 'teams', 'news'], top_k=3):
        """
        Query the RAG system with a question.
        
        Args:
            question (str): User question
            include_sources (list): Which sources to search (players, teams, news)
            top_k (int): Number of results per source
            
        Returns:
            dict: Answer and context
        """
        context_parts = []
        
        # Gather context from different sources
        if 'players' in include_sources:
            player_results = self.search_player_stats(question, top_k)
            if player_results:
                context_parts.append("PLAYER STATISTICS:")
                for result in player_results:
                    context_parts.append(
                        f"- {result['player_name']} ({result['team']}, {result['position']}): "
                        f"{result['stats_data']} (Season: {result['season']}, "
                        f"Similarity: {result['similarity']:.3f})"
                    )
        
        if 'teams' in include_sources:
            team_results = self.search_team_stats(question, top_k)
            if team_results:
                context_parts.append("\nTEAM STATISTICS:")
                for result in team_results:
                    context_parts.append(
                        f"- {result['team_name']}: {result['stats_data']} "
                        f"(Season: {result['season']}, Similarity: {result['similarity']:.3f})"
                    )
        
        if 'news' in include_sources:
            news_results = self.search_news(question, top_k)
            if news_results:
                context_parts.append("\nNEWS ARTICLES:")
                for result in news_results:
                    context_parts.append(
                        f"- {result['title']} ({result['source']}): "
                        f"{result['content'][:200]}... "
                        f"(Similarity: {result['similarity']:.3f})"
                    )
        
        context = "\n".join(context_parts)
        
        # Generate answer using GPT
        messages = [
            {
                "role": "system",
                "content": "You are a fantasy football expert assistant. Use the provided context "
                          "to answer questions about players, teams, and fantasy football news. "
                          "Be specific and cite relevant statistics when applicable."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        return {
            'answer': answer,
            'context': context,
            'sources': {
                'players': player_results if 'players' in include_sources else [],
                'teams': team_results if 'teams' in include_sources else [],
                'news': news_results if 'news' in include_sources else []
            }
        }
