"""
Persistent conversational memory management.
"""
from typing import List, Optional, Dict
from pathlib import Path
from config import Config
from core.utils import save_json, load_json, get_timestamp

class ConversationMemory:
    """Manage persistent conversation history with timestamps."""
    
    def __init__(self, store_path: Path = Config.MEMORY_STORE_PATH):
        self.store_path = store_path
        self.conversations = self._load_conversations()
    
    def _load_conversations(self) -> Dict[str, list]:
        """Load existing conversations from disk."""
        data = load_json(self.store_path)
        return data if data else {"turns": []}
    
    def add_turn(self, query: str, response: str, context_used: Optional[List[str]] = None) -> dict:
        """
        Add a conversation turn to memory.
        
        Args:
            query: User query
            response: Assistant response
            context_used: List of context sources used
        
        Returns:
            Turn metadata
        """
        turn = {
            'timestamp': get_timestamp(),
            'query': query,
            'response': response,
            'context_used': context_used or []
        }
        
        if 'turns' not in self.conversations:
            self.conversations['turns'] = []
        
        self.conversations['turns'].append(turn)
        self._save_conversations()
        
        return turn
    
    def get_history(self, limit: Optional[int] = None) -> List[dict]:
        """
        Get conversation history.
        
        Args:
            limit: Maximum number of turns to return
        
        Returns:
            List of conversation turns
        """
        turns = self.conversations.get('turns', [])
        if limit:
            return turns[-limit:]
        return turns
    
    def get_last_n_turns(self, n: int = 5) -> List[tuple[str, str]]:
        """
        Get last n query-response pairs.
        
        Args:
            n: Number of turns
        
        Returns:
            List of (query, response) tuples
        """
        turns = self.conversations.get('turns', [])
        pairs = []
        for turn in turns[-n:]:
            pairs.append((turn['query'], turn['response']))
        return pairs
    
    def get_context_string(self, limit: int = 3) -> str:
        """
        Get formatted context from recent turns.
        
        Args:
            limit: Number of turns
        
        Returns:
            Formatted context string
        """
        turns = self.get_last_n_turns(limit)
        if not turns:
            return ""
        
        context = "Recent conversation:\n"
        for i, (query, response) in enumerate(turns, 1):
            context += f"{i}. Q: {query}\n   A: {response[:100]}...\n"
        
        return context
    
    def clear(self):
        """Clear all conversations."""
        self.conversations = {"turns": []}
        self._save_conversations()
    
    def _save_conversations(self):
        """Save conversations to disk."""
        save_json(self.conversations, self.store_path)
    
    def get_size(self) -> int:
        """Get number of turns in memory."""
        return len(self.conversations.get('turns', []))
