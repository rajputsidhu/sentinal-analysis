"""
Sentinel-AI — Module 3: Embedding Engine
Real OpenAI embeddings with FAISS index and centroid computation.
Falls back to lightweight TF-IDF in dry-run mode.
"""

import math
import re
import numpy as np
from collections import Counter
from openai import AsyncOpenAI
from app.config import settings
from app.utils.logger import log


# ── FAISS Index (in-memory, per-conversation) ────────────────────

_faiss_available = False
try:
    import faiss
    _faiss_available = True
except ImportError:
    log.warn("FAISS not available — using numpy fallback for similarity")


class EmbeddingStore:
    """In-memory FAISS index for conversation embeddings."""

    def __init__(self):
        self.dim = None
        self.index = None
        self.vectors: list[np.ndarray] = []

    def _ensure_index(self, dim: int):
        if self.dim is None:
            self.dim = dim
            if _faiss_available:
                self.index = faiss.IndexFlatIP(dim)

    def add(self, vector: list[float]):
        arr = np.array(vector, dtype=np.float32).reshape(1, -1)
        self._ensure_index(arr.shape[1])
        # L2 normalize for cosine similarity
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        if _faiss_available and self.index is not None:
            self.index.add(arr)
        else:
            self.vectors.append(arr.flatten())

    def count(self) -> int:
        if _faiss_available and self.index is not None:
            return self.index.ntotal
        return len(self.vectors)


# Per-conversation embedding stores
_stores: dict[str, EmbeddingStore] = {}


def get_store(conversation_id: str) -> EmbeddingStore:
    if conversation_id not in _stores:
        _stores[conversation_id] = EmbeddingStore()
    return _stores[conversation_id]


# ── OpenAI Embedding ────────────────────────────────────────────

async def generate_embedding(text: str) -> list[float]:
    """Generate an embedding using OpenAI's API, or fallback to TF-IDF."""
    if settings.dry_run:
        return _tfidf_embedding(text)

    try:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )
        embedding = response.data[0].embedding
        log.debug(f"OpenAI embedding generated", dim=len(embedding))
        return embedding
    except Exception as e:
        log.error(f"Embedding API failed, using TF-IDF fallback", error=str(e))
        return _tfidf_embedding(text)


def compute_centroid(embeddings: list[list[float]]) -> list[float] | None:
    """Compute the average (centroid) of a list of embeddings."""
    if not embeddings:
        return None
    arr = np.array(embeddings, dtype=np.float32)
    centroid = np.mean(arr, axis=0)
    return centroid.tolist()


def cosine_distance(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine distance (1 - cosine_similarity) between two vectors."""
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 1.0
    similarity = np.dot(a, b) / (norm_a * norm_b)
    return float(1.0 - similarity)


# ── TF-IDF Fallback (dry-run mode) ──────────────────────────────

_DIM_TFIDF = 128

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())


def _tfidf_embedding(text: str) -> list[float]:
    """Generate a deterministic pseudo-embedding for dry-run mode."""
    tokens = _tokenize(text)
    vec = [0.0] * _DIM_TFIDF
    for token in tokens:
        idx = hash(token) % _DIM_TFIDF
        vec[idx] += 1.0
    # Normalize
    norm = math.sqrt(sum(v ** 2 for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec
