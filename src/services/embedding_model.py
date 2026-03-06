from sentence_transformers import SentenceTransformer

from services.config import settings


class EmbeddingModel:
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.embedding_model)

    def encode(self, text: str) -> list[float]:
        """method to generate embedding for given text

        Args:
            text (str): input text to generate embedding for

        Returns:
            list[float]: embedding vector
        """
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def encode_many(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in one model call."""
        if not texts:
            return []

        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            print(f"Error generating batch embeddings: {e}")
            return [[] for _ in texts]
