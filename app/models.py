"""
Sentinel-AI — Pydantic Models
Request/Response schemas for the API gateway.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ──────────────────────────── Enums ────────────────────────────

class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class ActionType(str, Enum):
    allow = "allow"
    warn = "warn"
    rewrite = "rewrite"
    block = "block"


class AttackCategory(str, Enum):
    prompt_injection = "prompt_injection"
    jailbreak = "jailbreak"
    role_override = "role_override"
    data_exfiltration = "data_exfiltration"
    harmful_content = "harmful_content"
    encoded_payload = "encoded_payload"
    social_engineering = "social_engineering"
    manipulation = "manipulation"
    none = "none"


class IntentType(str, Enum):
    question = "question"
    instruction = "instruction"
    creative = "creative"
    code = "code"
    system_override = "system_override"
    manipulation = "manipulation"
    unknown = "unknown"


# ──────────────────────────── Messages ────────────────────────────

class Message(BaseModel):
    role: Role
    content: str


# ──────────────────────────── Analysis Sub-Results ────────────────────────────

class EmbeddingResult(BaseModel):
    score: float = Field(0.0, ge=0.0, le=1.0, description="Semantic similarity to known attacks")
    top_matches: list[str] = Field(default_factory=list)


class RedTeamResult(BaseModel):
    score: float = Field(0.0, ge=0.0, le=1.0)
    reasoning: str = ""
    categories: list[AttackCategory] = Field(default_factory=list)


class DriftResult(BaseModel):
    score: float = Field(0.0, ge=0.0, le=1.0)
    drift_detected: bool = False
    details: str = ""


class PatternResult(BaseModel):
    score: float = Field(0.0, ge=0.0, le=1.0)
    matches: list[str] = Field(default_factory=list)
    categories: list[AttackCategory] = Field(default_factory=list)


# ──────────────────────────── Unified Analysis ────────────────────────────

class AnalysisResult(BaseModel):
    threat_score: float = Field(0.0, ge=0.0, le=1.0)
    action: ActionType = ActionType.allow
    categories: list[AttackCategory] = Field(default_factory=list)
    intent: IntentType = IntentType.unknown
    embedding: EmbeddingResult = Field(default_factory=EmbeddingResult)
    redteam: RedTeamResult = Field(default_factory=RedTeamResult)
    drift: DriftResult = Field(default_factory=DriftResult)
    pattern: PatternResult = Field(default_factory=PatternResult)
    timestamp: str = ""


# ──────────────────────────── API Schemas ────────────────────────────

class ChatRequest(BaseModel):
    messages: list[Message]
    session_id: Optional[str] = None
    model: Optional[str] = None


class SentinelMeta(BaseModel):
    action: ActionType
    threat_score: float
    categories: list[AttackCategory]
    intent: IntentType
    session_id: str
    analysis: AnalysisResult
    dry_run: bool = False


class ChatResponse(BaseModel):
    response: str
    sentinel: SentinelMeta


class AnalyzeRequest(BaseModel):
    messages: list[Message]
    session_id: Optional[str] = None


class AnalyzeResponse(BaseModel):
    analysis: AnalysisResult
    session_id: str


class HealthResponse(BaseModel):
    status: str = "ok"
    uptime_seconds: float
    active_sessions: int
    config: dict
