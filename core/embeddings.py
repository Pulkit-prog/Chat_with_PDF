"""
Embedding generation with safe local fallback.
"""
import numpy as np
from config import Config


class EmbeddingGenerator:
    def __init__(self):
        self.dimension = Config.EMBEDDING_DIMENSION

    def embed_text(self, text: str):
        if not text or not text.strip():
            return None
        return self._local_embedding(text)

    def embed_texts(self, texts):
        if not texts:
            return []
        return [self._local_embedding(t) for t in texts if t.strip()]

    def embed_query(self, query: str):
        return self.embed_text(query)

    def _local_embedding(self, text: str):
        """
        Deterministic local embedding (stable, fast, reliable)
        """
        vec = np.zeros(self.dimension, dtype=np.float32)
        for i, b in enumerate(text.encode("utf-8")):
            vec[i % self.dimension] += b / 255.0
        return vec.tolist()

