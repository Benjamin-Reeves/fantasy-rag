class NewsArticleChunker:
    """Split long article content into overlapping character chunks for embeddings."""

    def __init__(self, max_chars: int = 1000, overlap_chars: int = 200, min_chars: int = 250):
        if overlap_chars >= max_chars:
            raise ValueError("overlap_chars must be smaller than max_chars")

        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
        self.min_chars = min_chars

    def chunk_text(self, text: str) -> list[str]:
        normalized = " ".join(text.split())
        if not normalized:
            return []

        if len(normalized) <= self.max_chars:
            return [normalized]

        step = self.max_chars - self.overlap_chars
        chunks: list[str] = []

        for start in range(0, len(normalized), step):
            raw_end = min(start + self.max_chars, len(normalized))
            end = raw_end

            # wanna end on a whitespace boundary for cleaner chunk text.
            if raw_end < len(normalized):
                boundary = normalized.rfind(" ", start + self.min_chars, raw_end)
                if boundary != -1:
                    end = boundary

            window = normalized[start:end].strip()
            if not window:
                break

            # we don't want something to short, so we will just add to the last 
            # chunk
            if len(window) < self.min_chars and chunks:
                chunks[-1] = f"{chunks[-1]} {window}"
                break

            chunks.append(window)

            if raw_end >= len(normalized):
                break

        return chunks
