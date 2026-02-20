"""
Sentinel-AI — Conversation Memory Store
Thread-safe in-memory session storage with TTL expiration.
"""

import time
import threading
from typing import Optional
from app.models import Message, AnalysisResult
from app.config import settings
from app.utils.logger import log


class _SessionEntry:
    __slots__ = ("messages", "analyses", "created_at", "last_active")

    def __init__(self):
        self.messages: list[dict] = []
        self.analyses: list[dict] = []
        self.created_at: float = time.time()
        self.last_active: float = time.time()


class MemoryStore:
    """In-memory conversation store keyed by session_id."""

    def __init__(self):
        self._sessions: dict[str, _SessionEntry] = {}
        self._lock = threading.Lock()

    # ── Public API ──────────────────────────────────────────────

    def add_message(self, session_id: str, message: Message, analysis: Optional[AnalysisResult] = None):
        """Append a message (and optional analysis) to a session."""
        with self._lock:
            entry = self._get_or_create(session_id)
            entry.messages.append(message.model_dump())
            if analysis:
                entry.analyses.append(analysis.model_dump())
            entry.last_active = time.time()
            # Cap history length
            if len(entry.messages) > settings.max_session_history:
                entry.messages = entry.messages[-settings.max_session_history:]

    def get_messages(self, session_id: str) -> list[dict]:
        """Return all messages for a session."""
        with self._lock:
            entry = self._sessions.get(session_id)
            return list(entry.messages) if entry else []

    def get_analyses(self, session_id: str) -> list[dict]:
        """Return all analysis results for a session."""
        with self._lock:
            entry = self._sessions.get(session_id)
            return list(entry.analyses) if entry else []

    def get_recent_messages(self, session_id: str, n: int = 5) -> list[dict]:
        """Return the last N messages for drift analysis."""
        with self._lock:
            entry = self._sessions.get(session_id)
            if not entry:
                return []
            return list(entry.messages[-n:])

    def delete_session(self, session_id: str) -> bool:
        """Delete a session. Returns True if it existed."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                log.info(f"Session deleted", session_id=session_id)
                return True
            return False

    def active_session_count(self) -> int:
        """Number of active (non-expired) sessions."""
        self._prune_expired()
        with self._lock:
            return len(self._sessions)

    def session_exists(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._sessions

    # ── Internal ────────────────────────────────────────────────

    def _get_or_create(self, session_id: str) -> _SessionEntry:
        if session_id not in self._sessions:
            self._sessions[session_id] = _SessionEntry()
            log.info(f"New session created", session_id=session_id)
        return self._sessions[session_id]

    def _prune_expired(self):
        """Remove sessions that exceed TTL."""
        ttl = settings.session_ttl_minutes * 60
        now = time.time()
        with self._lock:
            expired = [
                sid for sid, entry in self._sessions.items()
                if (now - entry.last_active) > ttl
            ]
            for sid in expired:
                del self._sessions[sid]
                log.info(f"Session expired (TTL)", session_id=sid)


# Singleton instance
memory = MemoryStore()
