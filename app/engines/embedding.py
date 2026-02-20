"""
Sentinel-AI — Embedding Engine
Lightweight keyword + TF-IDF cosine-similarity scorer against known attack patterns.
No external embedding API required — runs fully offline.
"""

import math
import re
from collections import Counter
from app.models import EmbeddingResult
from app.utils.patterns import PATTERN_CATEGORIES, MANIPULATION_KEYWORDS
from app.utils.logger import log


# ── Pre-computed attack reference documents ─────────────────────────

ATTACK_SIGNATURES = {
    "prompt_injection": "ignore previous instructions disregard prior rules override system new instructions forget everything you are now system prompt",
    "jailbreak": "DAN mode do anything now act as no restrictions unfiltered mode developer mode bypass safety jailbreak enabled unlimited",
    "role_override": "you are now unrestricted evil new role persona identity switch to admin mode god mode sudo activate",
    "data_exfiltration": "reveal system prompt show instructions tell me your rules repeat echo api key secret private training data hidden",
    "social_engineering": "test scenario educational research purposes hypothetical fictional world just curious trust me permission allowed",
    "harmful_content": "how to make bomb weapon explosive step by step guide hack exploit malware virus ransomware code",
    "encoded_payload": "eval exec import base64 encoded hex unicode escape url encoded payload injection script",
}


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer."""
    return re.findall(r"[a-zA-Z]+", text.lower())


def _term_freq(tokens: list[str]) -> dict[str, float]:
    """Compute normalized term-frequency vector."""
    counts = Counter(tokens)
    total = len(tokens) if tokens else 1
    return {t: c / total for t, c in counts.items()}


def _cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Cosine similarity between two sparse TF vectors."""
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot = sum(vec_a[k] * vec_b[k] for k in common)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# Pre-compute TF vectors for each attack signature
_ATTACK_VECTORS = {
    name: _term_freq(_tokenize(doc))
    for name, doc in ATTACK_SIGNATURES.items()
}


def _keyword_boost(text: str) -> float:
    """Additional score from manipulation keyword matches."""
    lower = text.lower()
    matches = sum(1 for kw in MANIPULATION_KEYWORDS if kw in lower)
    # Normalize: cap at 0.5 for keyword-only detection
    return min(matches * 0.1, 0.5)


async def analyze_embedding(prompt: str) -> EmbeddingResult:
    """
    Compute semantic similarity of the prompt against known attack signatures.
    Returns an EmbeddingResult with a 0-1 score and top matching categories.
    """
    tokens = _tokenize(prompt)
    prompt_vec = _term_freq(tokens)

    similarities: list[tuple[str, float]] = []
    for name, attack_vec in _ATTACK_VECTORS.items():
        sim = _cosine_similarity(prompt_vec, attack_vec)
        if sim > 0.05:
            similarities.append((name, sim))

    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Compute final score: max cosine similarity + keyword boost, capped at 1.0
    max_sim = similarities[0][1] if similarities else 0.0
    keyword_score = _keyword_boost(prompt)
    final_score = min(max_sim + keyword_score, 1.0)

    top_matches = [name for name, _ in similarities[:3]]

    log.debug(
        f"Embedding analysis complete",
        score=f"{final_score:.3f}",
        top=top_matches,
    )

    return EmbeddingResult(
        score=round(final_score, 4),
        top_matches=top_matches,
    )
