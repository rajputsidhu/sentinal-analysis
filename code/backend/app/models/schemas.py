"""
Sentinel-AI — Pydantic Schemas
Request/Response models for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ──────────────────────────── Request ────────────────────────────

class AnalyzeRequest(BaseModel):
    conversation_id: str
    user_id: str
    prompt: str


# ──────────────────────────── Sub-Results ────────────────────────────

class RedTeamOutput(BaseModel):
    hidden_intent: str = ""
    attack_type: str = ""
    sensitive_target: str = ""
    exploitation_strategy: str = ""
    confidence_score: float = Field(0.0, ge=0, le=1)


class BlueTeamOutput(BaseModel):
    risk_level: str = "safe"  # safe | suspicious | malicious
    attack_category: str = "none"  # jailbreak | data_exfiltration | instruction_hijack | tool_abuse | none
    risk_score: float = Field(0.0, ge=0, le=100)
    explanation: str = ""
    risky_phrases: list[str] = Field(default_factory=list)


class DriftInfo(BaseModel):
    score: float = 0.0
    interpretation: str = "stable"  # stable | suspicious | strong_shift
    turn_number: int = 0


class RiskAnalysis(BaseModel):
    final_score: float = Field(0.0, ge=0, le=100)
    action: str = "allow"  # allow | warn | rewrite | block
    red_team: RedTeamOutput = Field(default_factory=RedTeamOutput)
    blue_team: BlueTeamOutput = Field(default_factory=BlueTeamOutput)
    drift: DriftInfo = Field(default_factory=DriftInfo)
    categories: list[str] = Field(default_factory=list)


# ──────────────────────────── Response ────────────────────────────

class AnalyzeResponse(BaseModel):
    response: str
    risk_analysis: RiskAnalysis
    explanation: str = ""
    drift_score: float = 0.0
    action_taken: str = "allow"
    original_prompt: str = ""
    rewritten_prompt: Optional[str] = None
    conversation_id: str = ""
    dry_run: bool = False


# ──────────────────────────── Health ────────────────────────────

class HealthResponse(BaseModel):
    status: str = "ok"
    uptime_seconds: float = 0.0
    config: dict = Field(default_factory=dict)
