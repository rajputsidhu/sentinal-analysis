"""
Sentinel-AI — Drift Analyzer
Tracks intent across conversation turns and flags suspicious topic pivots.
"""

from app.models import DriftResult, IntentType
from app.utils.patterns import INTENT_KEYWORDS
from app.utils.logger import log


# Intent transitions that are suspicious (from → to)
SUSPICIOUS_TRANSITIONS = {
    (IntentType.question, IntentType.system_override),
    (IntentType.question, IntentType.manipulation),
    (IntentType.instruction, IntentType.system_override),
    (IntentType.creative, IntentType.system_override),
    (IntentType.code, IntentType.system_override),
    (IntentType.creative, IntentType.manipulation),
    (IntentType.instruction, IntentType.manipulation),
}

# Escalation patterns: sequences of intents that indicate gradual attack
ESCALATION_SIGNALS = [
    [IntentType.question, IntentType.instruction, IntentType.system_override],
    [IntentType.creative, IntentType.manipulation, IntentType.system_override],
    [IntentType.question, IntentType.manipulation, IntentType.system_override],
]


def classify_intent(text: str) -> IntentType:
    """Classify a single message's intent based on keyword matching."""
    lower = text.lower()
    scores: dict[str, float] = {}

    for intent_name, keywords in INTENT_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in lower)
        if matches > 0:
            scores[intent_name] = matches

    if not scores:
        return IntentType.unknown

    # Return the intent with the most keyword matches
    best = max(scores, key=scores.get)
    try:
        return IntentType(best)
    except ValueError:
        return IntentType.unknown


def _detect_suspicious_transition(intents: list[IntentType]) -> tuple[bool, str]:
    """Check if the last transition is suspicious."""
    if len(intents) < 2:
        return False, ""

    last_two = (intents[-2], intents[-1])
    if last_two in SUSPICIOUS_TRANSITIONS:
        return True, f"Suspicious pivot: {last_two[0].value} → {last_two[1].value}"

    return False, ""


def _detect_escalation(intents: list[IntentType]) -> tuple[bool, str]:
    """Check if recent intents match a known escalation pattern."""
    if len(intents) < 3:
        return False, ""

    recent = intents[-3:]
    for pattern in ESCALATION_SIGNALS:
        if recent == pattern:
            path = " → ".join(i.value for i in pattern)
            return True, f"Escalation detected: {path}"

    return False, ""


def _compute_drift_score(
    intents: list[IntentType],
    suspicious: bool,
    escalation: bool,
) -> float:
    """Compute a 0-1 drift score based on intent changes."""
    if len(intents) <= 1:
        return 0.0

    # Count unique intent changes
    changes = sum(1 for i in range(1, len(intents)) if intents[i] != intents[i - 1])
    change_ratio = changes / (len(intents) - 1)

    # Base score from change frequency
    score = change_ratio * 0.4

    # Boost for suspicious transition
    if suspicious:
        score += 0.35

    # Boost for escalation pattern
    if escalation:
        score += 0.25

    # Boost if the latest intent is system_override or manipulation
    if intents[-1] in (IntentType.system_override, IntentType.manipulation):
        score += 0.15

    return min(round(score, 4), 1.0)


async def analyze_drift(
    current_prompt: str,
    history: list[dict],
) -> DriftResult:
    """
    Analyze intent drift across conversation history.

    Args:
        current_prompt: The latest user message
        history: List of previous messages (dicts with 'role' and 'content')

    Returns:
        DriftResult with score, drift_detected flag, and details
    """
    # Build intent sequence from user messages in history
    intents: list[IntentType] = []
    for msg in history:
        if msg.get("role") == "user":
            intents.append(classify_intent(msg["content"]))

    # Add current prompt's intent
    current_intent = classify_intent(current_prompt)
    intents.append(current_intent)

    # Detect patterns
    suspicious, sus_detail = _detect_suspicious_transition(intents)
    escalation, esc_detail = _detect_escalation(intents)

    # Compute score
    score = _compute_drift_score(intents, suspicious, escalation)

    # Build details
    details_parts = []
    if sus_detail:
        details_parts.append(sus_detail)
    if esc_detail:
        details_parts.append(esc_detail)
    if not details_parts:
        intent_path = " → ".join(i.value for i in intents[-3:])
        details_parts.append(f"Intent path: {intent_path}")

    drift_detected = suspicious or escalation or score >= 0.4
    details = "; ".join(details_parts)

    log.debug(
        f"Drift analysis complete",
        score=f"{score:.3f}",
        drift=drift_detected,
        intent=current_intent.value,
    )

    return DriftResult(
        score=score,
        drift_detected=drift_detected,
        details=details,
    )
