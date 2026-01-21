from sentence_transformers import SentenceTransformer

from core.config import settings


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