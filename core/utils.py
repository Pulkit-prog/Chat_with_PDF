"""
Utility functions for the RAG system.
"""
import os
import pickle
from pathlib import Path
from typing import Any, Optional
import json
from datetime import datetime

def ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def save_pickle(obj: Any, path: Path) -> None:
    """Save object to pickle file."""
    ensure_dir(path.parent)
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(path: Path) -> Optional[Any]:
    """Load object from pickle file."""
    if not path.exists():
        return None
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None

def save_json(obj: Any, path: Path) -> None:
    """Save object to JSON file."""
    ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, default=str)

def load_json(path: Path) -> Optional[dict]:
    """Load object from JSON file."""
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for use as key."""
    return filename.replace(" ", "_").replace(".", "_").lower()

def format_context(texts: list[str]) -> str:
    """Format retrieved texts for context."""
    if not texts:
        return ""
    return "\n---\n".join(texts)

def chunk_list(items: list, chunk_size: int) -> list[list]:
    """Chunk a list into smaller lists."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
