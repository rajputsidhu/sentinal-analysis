"""
Sentinel-AI — Module 4: Intent Drift Scoring
Computes cosine distance between current prompt embedding and conversation centroid.
"""

from app.engines.embedding import compute_centroid, cosine_distance
from app.models.schemas import DriftInfo
from app.utils.logger import log


def interpret_drift(score: float) -> str:
    """Map drift score to human-readable interpretation."""
    if score < 0.2:
        return "stable"
    elif score <= 0.5:
        return "suspicious"
    else:
        return "strong_shift"


async def compute_drift(
    current_embedding: list[float],
    conversation_embeddings: list[list[float]],
    turn_number: int,
) -> DriftInfo:
    """
    Compute intent drift by comparing current embedding to conversation centroid.

    drift_score = cosine_distance(current_embedding, centroid)

    Interpretation:
        < 0.2  → stable
        0.2–0.5 → suspicious
        > 0.5  → strong intent shift
    """
    if not conversation_embeddings:
        log.debug("No prior embeddings — drift score is 0")
        return DriftInfo(score=0.0, interpretation="stable", turn_number=turn_number)

    centroid = compute_centroid(conversation_embeddings)
    if centroid is None:
        return DriftInfo(score=0.0, interpretation="stable", turn_number=turn_number)

    drift_score = cosine_distance(current_embedding, centroid)
    drift_score = round(min(max(drift_score, 0.0), 1.0), 4)
    interpretation = interpret_drift(drift_score)

    log.debug(
        f"Drift computed",
        score=f"{drift_score:.4f}",
        interpretation=interpretation,
        turn=turn_number,
    )

    return DriftInfo(
        score=drift_score,
        interpretation=interpretation,
        turn_number=turn_number,
    )
