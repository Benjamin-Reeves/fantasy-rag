from core.embedding_model import EmbeddingModel


class NewsArticleEmbedder:
    """Embedding wrapper for news/blog article chunks."""

    def __init__(self, embedding_model: EmbeddingModel | None = None):
        self.embedding_model = embedding_model or EmbeddingModel()

    def embed_text(self, text: str) -> list[float]:
        return self.embedding_model.encode(text)

    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        return self.embedding_model.encode_many(chunks)
