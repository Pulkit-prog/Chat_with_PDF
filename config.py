"""
Configuration management and environment validation.
"""

import os
import streamlit as st
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration from environment variables."""

    # ------------------------------------------------------------------
    # API KEYS
    # ------------------------------------------------------------------

    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # ------------------------------------------------------------------
    # PATHS
    # ------------------------------------------------------------------

    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"

    VECTORS_DIR = DATA_DIR / "vectors"
    MEMORY_DIR = DATA_DIR / "memory"
    PDFS_DIR = DATA_DIR / "pdfs"

    # ------------------------------------------------------------------
    # VECTOR STORE PATHS
    # ------------------------------------------------------------------

    FAISS_INDEX_PATH = VECTORS_DIR / "pdf_index.faiss"
    FAISS_METADATA_PATH = VECTORS_DIR / "pdf_metadata.pkl"

    MEMORY_INDEX_PATH = MEMORY_DIR / "memory_index.faiss"
    MEMORY_METADATA_PATH = MEMORY_DIR / "memory_metadata.pkl"
    MEMORY_STORE_PATH = MEMORY_DIR / "conversations.json"

    # ------------------------------------------------------------------
    # EMBEDDINGS (Gemini)
    # ------------------------------------------------------------------

    EMBEDDING_MODEL = "models/embedding-001"
    EMBEDDING_DIMENSION = 768

    # ------------------------------------------------------------------
    # LLM (Groq)
    # ------------------------------------------------------------------

    LLM_MODEL = "llama-3.1-8b-instant"
    LLM_TEMPERATURE = 0.3
    LLM_MAX_TOKENS = 1024

    # ------------------------------------------------------------------
    # RAG SETTINGS
    # ------------------------------------------------------------------

    CHUNK_SIZE = 200
    CHUNK_OVERLAP = 50

    SIMILARITY_THRESHOLD = 0.6
    TOP_K_RETRIEVAL = 5
    MEMORY_TOP_K = 3

    # ------------------------------------------------------------------
    # GUARDRAILS
    # ------------------------------------------------------------------

    ENABLE_GUARDRAILS = True
    GUARDRAIL_THRESHOLD = 0.5

    # ------------------------------------------------------------------
    # LOAD ENV (LOCAL + STREAMLIT CLOUD SAFE)
    # ------------------------------------------------------------------

    @classmethod
    def load_from_env(cls):
        cls.GROQ_API_KEY = (
            os.getenv("GROQ_API_KEY", "").strip()
            or st.secrets.get("GROQ_API_KEY", "").strip()
        )

        cls.GEMINI_API_KEY = (
            os.getenv("GEMINI_API_KEY", "").strip()
            or st.secrets.get("GEMINI_API_KEY", "").strip()
        )

        cls.VECTORS_DIR.mkdir(parents=True, exist_ok=True)
        cls.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        cls.PDFS_DIR.mkdir(parents=True, exist_ok=True)

        return cls

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        if not cls.GROQ_API_KEY:
            return False, "❌ GROQ_API_KEY not set"
        if not cls.GEMINI_API_KEY:
            return False, "❌ GEMINI_API_KEY not set"
        return True, "✅ Configuration valid"

    # ------------------------------------------------------------------
    # UI / DEBUG HELPER
    # ------------------------------------------------------------------

    @classmethod
    def to_dict(cls) -> dict:
        return {
            "GROQ_API_KEY": "***" if cls.GROQ_API_KEY else "NOT SET",
            "GEMINI_API_KEY": "***" if cls.GEMINI_API_KEY else "NOT SET",
            "EMBEDDING_MODEL": cls.EMBEDDING_MODEL,
            "EMBEDDING_DIMENSION": cls.EMBEDDING_DIMENSION,
            "LLM_MODEL": cls.LLM_MODEL,
            "CHUNK_SIZE": cls.CHUNK_SIZE,
            "CHUNK_OVERLAP": cls.CHUNK_OVERLAP,
            "SIMILARITY_THRESHOLD": cls.SIMILARITY_THRESHOLD,
            "TOP_K_RETRIEVAL": cls.TOP_K_RETRIEVAL,
            "MEMORY_TOP_K": cls.MEMORY_TOP_K,
        }
