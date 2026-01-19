"""Embedding generation service using OpenAI."""
from openai import OpenAI
from config import Config


class EmbeddingService:
    """Service for generating embeddings using OpenAI."""
    
    def __init__(self):
        """Initialize embedding service."""
        self.config = Config()
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
    
    def generate_embedding(self, text):
        """
        Generate embedding for given text.
        
        Args:
            text (str): Text to generate embedding for
            
        Returns:
            list: Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts):
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts (list): List of texts to generate embeddings for
            
        Returns:
            list: List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
