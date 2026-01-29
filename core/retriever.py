"""
Unified retrieval from PDF and memory stores.
"""
from typing import List, Tuple
from core.vectorstore import FAISSVectorStore
from core.embeddings import EmbeddingGenerator
from config import Config


class UnifiedRetriever:
    """Retrieve relevant content from PDF and conversation memory."""

    def __init__(self):
        self.embeddings = EmbeddingGenerator()

        self.pdf_store = FAISSVectorStore(
            index_path=Config.FAISS_INDEX_PATH,
            metadata_path=Config.FAISS_METADATA_PATH,
        )

        self.memory_store = FAISSVectorStore(
            index_path=Config.MEMORY_INDEX_PATH,
            metadata_path=Config.MEMORY_METADATA_PATH,
        )

    # ------------------------------------------------------------------
    # RETRIEVAL
    # ------------------------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k_pdf: int = Config.TOP_K_RETRIEVAL,
        top_k_memory: int = Config.MEMORY_TOP_K,
        threshold: float = Config.SIMILARITY_THRESHOLD,
    ) -> Tuple[List[str], List[dict]]:
        """
        Retrieve relevant texts from both PDF and memory stores.
        """
        query_embedding = self.embeddings.embed_query(query)
        if not query_embedding:
            return [], []

        pdf_results = self.pdf_store.search(query_embedding, k=top_k_pdf)
        memory_results = self.memory_store.search(query_embedding, k=top_k_memory)

        texts = []
        metadata = []

        for _, similarity, meta in pdf_results:
            if similarity >= threshold:
                texts.append(meta.get("text", ""))
                metadata.append(
                    {
                        "source": meta.get("source", "Unknown"),
                        "type": "pdf",
                        "similarity": float(similarity),
                    }
                )

        for _, similarity, meta in memory_results:
            if similarity >= threshold:
                texts.append(meta.get("text", ""))
                metadata.append(
                    {
                        "source": "Memory",
                        "type": "memory",
                        "timestamp": meta.get("timestamp", ""),
                        "similarity": float(similarity),
                    }
                )

        return texts, metadata

    # ------------------------------------------------------------------
    # PDF INDEXING  ✅ FIXED
    # ------------------------------------------------------------------

    def add_pdf_documents(self, documents: List[dict]) -> int:
        """
        Add PDF documents to vector store.

        Expected format:
        [
            {
                "text": "chunk text",
                "metadata": {...}
            },
            ...
        ]
        """
        if not documents:
            return 0

        texts = []
        metadata_list = []

        for doc in documents:
            text = doc.get("text")
            meta = doc.get("metadata", {})

            if text and text.strip():
                texts.append(text)
                meta["text"] = text  # store text for retrieval
                metadata_list.append(meta)

        if not texts:
            return 0

        embeddings = self.embeddings.embed_texts(texts)
        if not embeddings:
            return 0

        ids = self.pdf_store.add(embeddings, metadata_list)
        return len(ids)

    # ------------------------------------------------------------------
    # MEMORY INDEXING
    # ------------------------------------------------------------------

    def add_memory(self, text: str, timestamp: str) -> bool:
        """
        Add conversation to memory store.
        """
        embedding = self.embeddings.embed_text(text)
        if not embedding:
            return False

        metadata = {
            "text": text,
            "timestamp": timestamp,
            "source": "conversation",
        }

        ids = self.memory_store.add([embedding], [metadata])
        return len(ids) > 0

    # ------------------------------------------------------------------
    # STATS
    # ------------------------------------------------------------------

    def get_stats(self) -> dict:
        """Get retriever statistics."""
        return {
            "pdf_vectors": self.pdf_store.get_size(),
            "memory_vectors": self.memory_store.get_size(),
            "total_vectors": self.pdf_store.get_size()
            + self.memory_store.get_size(),
        }
