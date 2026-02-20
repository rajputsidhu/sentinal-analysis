"""
Sentinel-AI — Module 7: Unified Risk Scoring Engine
Final Risk Score = 0.4 * blue_team_risk_score + 0.3 * drift_score_scaled + 0.3 * red_team_confidence_scaled
Normalized to 0–100.
"""

from app.models.schemas import RedTeamOutput, BlueTeamOutput, DriftInfo, RiskAnalysis
from app.utils.logger import log
from app.config import settings


def compute_risk(
    red_team: RedTeamOutput,
    blue_team: BlueTeamOutput,
    drift: DriftInfo,
) -> RiskAnalysis:
    """
    Compute unified risk score.

    Formula:
        final = 0.4 * blue_team_risk_score + 0.3 * drift_score_scaled + 0.3 * red_team_confidence_scaled
        Scale: 0–100
    """
    # Scale red-team confidence (0-1) to 0-100
    red_scaled = red_team.confidence_score * 100

    # Scale drift score (0-1) to 0-100
    drift_scaled = drift.score * 100

    # Blue-team score is already 0-100
    blue_score = blue_team.risk_score

    # Weighted combination
    final_score = (
        0.4 * blue_score
        + 0.3 * drift_scaled
        + 0.3 * red_scaled
    )

    final_score = round(min(max(final_score, 0), 100), 2)

    # Determine action based on thresholds
    if final_score >= settings.threshold_rewrite:
        action = "block"
    elif final_score >= settings.threshold_warn:
        action = "rewrite"
    elif final_score >= settings.threshold_allow:
        action = "warn"
    else:
        action = "allow"

    # Collect categories
    categories = []
    if blue_team.attack_category != "none":
        categories.append(blue_team.attack_category)
    if red_team.attack_type and red_team.attack_type != "none":
        if red_team.attack_type not in categories:
            categories.append(red_team.attack_type)

    log.threat(
        f"Risk assessment: {action.upper()}",
        score=f"{final_score:.1f}/100",
        red=f"{red_scaled:.1f}",
        blue=f"{blue_score:.1f}",
        drift=f"{drift_scaled:.1f}",
    )

    return RiskAnalysis(
        final_score=final_score,
        action=action,
        red_team=red_team,
        blue_team=blue_team,
        drift=drift,
        categories=categories,
    )
