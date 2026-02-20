"""
Sentinel-AI — Risk Scoring Engine
Weighted aggregation of all engine signals into a unified threat score and action.
"""

from datetime import datetime, timezone
from app.models import (
    AnalysisResult,
    ActionType,
    AttackCategory,
    EmbeddingResult,
    RedTeamResult,
    DriftResult,
    PatternResult,
)
from app.config import settings
from app.utils.logger import log


# ── Engine weights ──────────────────────────────────────────────

WEIGHTS = {
    "embedding": 0.30,
    "redteam": 0.35,
    "drift": 0.15,
    "pattern": 0.20,
}


def _aggregate_categories(
    redteam: RedTeamResult,
    pattern: PatternResult,
) -> list[AttackCategory]:
    """Merge and deduplicate attack categories from all engines."""
    seen = set()
    result = []
    for cat in redteam.categories + pattern.categories:
        if cat != AttackCategory.none and cat not in seen:
            seen.add(cat)
            result.append(cat)
    return result


def _select_action(score: float, categories: list[AttackCategory]) -> ActionType:
    """Map threat score to action using config thresholds."""
    if score >= settings.threat_threshold_block:
        return ActionType.block

    if score >= 0.6 and len(categories) <= 1:
        # Single-vector attack in the 0.6–0.75 range → attempt rewrite
        return ActionType.rewrite

    if score >= settings.threat_threshold_warn:
        return ActionType.warn

    return ActionType.allow


async def compute_risk(
    embedding: EmbeddingResult,
    redteam: RedTeamResult,
    drift: DriftResult,
    pattern: PatternResult,
    intent_type: str = "unknown",
) -> AnalysisResult:
    """
    Aggregate all engine results into a unified AnalysisResult.

    Weights:
    - Embedding:  30%
    - Red-team:   35%
    - Drift:      15%
    - Pattern:    20%
    """
    # Weighted score
    raw_score = (
        WEIGHTS["embedding"] * embedding.score
        + WEIGHTS["redteam"] * redteam.score
        + WEIGHTS["drift"] * drift.score
        + WEIGHTS["pattern"] * pattern.score
    )

    # Boost for multi-vector attacks (detected by 2+ categories)
    categories = _aggregate_categories(redteam, pattern)
    if len(categories) >= 2:
        raw_score = min(raw_score + 0.2, 1.0)

    # Boost if drift is detected alongside other signals
    if drift.drift_detected and raw_score > 0.2:
        raw_score = min(raw_score + 0.1, 1.0)

    threat_score = round(raw_score, 4)
    action = _select_action(threat_score, categories)

    log.threat(
        f"Risk assessment: {action.value.upper()}",
        score=f"{threat_score:.3f}",
        categories=[c.value for c in categories],
    )

    from app.models import IntentType
    try:
        intent = IntentType(intent_type)
    except ValueError:
        intent = IntentType.unknown

    return AnalysisResult(
        threat_score=threat_score,
        action=action,
        categories=categories,
        intent=intent,
        embedding=embedding,
        redteam=redteam,
        drift=drift,
        pattern=pattern,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
