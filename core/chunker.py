"""
Semantic text chunking for RAG.
"""

from typing import List, Tuple
from config import Config


class SemanticChunker:
    """
    Splits text into overlapping chunks suitable for embedding & retrieval.
    """

    def __init__(
        self,
        chunk_size: int = Config.CHUNK_SIZE,
        overlap: int = Config.CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, metadata: dict) -> List[Tuple[str, dict]]:
        """
        Split text into overlapping chunks.

        Returns:
            List of (chunk_text, metadata)
        """
        if not text or not text.strip():
            return []

        words = text.split()
        chunks = []

        start = 0
        chunk_id = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words).strip()
            if chunk_text:
                meta = metadata.copy()
                meta["chunk_id"] = chunk_id
                meta["chunk_start"] = start
                meta["chunk_end"] = end

                chunks.append((chunk_text, meta))
                chunk_id += 1

            start += self.chunk_size - self.overlap

        return chunks

