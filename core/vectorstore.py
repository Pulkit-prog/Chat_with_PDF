"""
FAISS vector store for persistent document embeddings.
"""
from typing import List, Tuple
import faiss
import numpy as np
from pathlib import Path
from config import Config
from core.utils import save_pickle, load_pickle, ensure_dir


class FAISSVectorStore:
    """Persistent FAISS vector store for document embeddings."""

    def __init__(
        self,
        index_path: Path = None,
        metadata_path: Path = None,
        dimension: int = Config.EMBEDDING_DIMENSION,
    ):
        self.index_path = index_path or Config.FAISS_INDEX_PATH
        self.metadata_path = metadata_path or Config.FAISS_METADATA_PATH
        self.dimension = dimension

        self.index = None
        self.metadata: List[dict] = []

        self._load_index()

    # ------------------------------------------------------------------

    def _load_index(self):
        ensure_dir(self.index_path.parent)

        if self.index_path.exists() and self.metadata_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                self.metadata = load_pickle(self.metadata_path) or []
                print(f"✅ Loaded FAISS index with {len(self.metadata)} vectors")
                return
            except Exception as e:
                print(f"⚠️ Failed loading index: {e}")

        self._create_index()

    def _create_index(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

    # ------------------------------------------------------------------

    def add(self, embeddings: List[List[float]], metadata_list: List[dict]) -> List[int]:
        if not embeddings or not metadata_list:
            return []

        vectors = np.array(embeddings, dtype=np.float32)
        self.index.add(vectors)

        start_id = len(self.metadata)
        self.metadata.extend(metadata_list)
        self.save()

        return list(range(start_id, start_id + len(metadata_list)))

    # ------------------------------------------------------------------

    def search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[int, float, dict]]:
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_vector, min(k, self.index.ntotal))

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                similarity = 1.0 / (1.0 + distance)
                results.append((idx, similarity, self.metadata[idx]))

        return results

    # ------------------------------------------------------------------

    def save(self):
        ensure_dir(self.index_path.parent)
        faiss.write_index(self.index, str(self.index_path))
        save_pickle(self.metadata, self.metadata_path)

    def clear(self):
        self._create_index()
        self.save()

    def get_size(self) -> int:
        return self.index.ntotal
