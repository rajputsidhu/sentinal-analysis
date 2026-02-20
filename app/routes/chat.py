"""
Sentinel-AI — Chat Route
Main gateway endpoint: analyze → decide action → forward to LLM (or block) → respond.
"""

import uuid
from fastapi import APIRouter
from openai import AsyncOpenAI

from app.config import settings
from app.models import (
    ChatRequest, ChatResponse, SentinelMeta,
    AnalyzeRequest, AnalyzeResponse,
    ActionType, Message, PatternResult, AttackCategory,
)
from app.engines.embedding import analyze_embedding
from app.engines.redteam import analyze_redteam
from app.engines.drift import analyze_drift, classify_intent
from app.engines.risk_scorer import compute_risk
from app.engines.mitigation import mitigate_prompt
from app.engines.memory import memory
from app.utils.patterns import PATTERN_CATEGORIES
from app.utils.logger import log

router = APIRouter()


# ── Helpers ─────────────────────────────────────────────────────

def _run_pattern_scan(text: str) -> PatternResult:
    """Run regex pattern matching against all categories."""
    matched_categories: list[AttackCategory] = []
    matched_names: list[str] = []
    total = 0

    for cat_name, patterns in PATTERN_CATEGORIES.items():
        for pattern in patterns:
            if pattern.search(text):
                try:
                    matched_categories.append(AttackCategory(cat_name))
                except ValueError:
                    pass
                matched_names.append(cat_name)
                total += 1
                break

    score = min(total * 0.3, 1.0)
    if len(matched_categories) >= 2:
        score = min(score + 0.2, 1.0)

    return PatternResult(
        score=round(score, 4),
        matches=matched_names,
        categories=matched_categories,
    )


async def _call_main_llm(messages: list[dict], model: str | None = None) -> str:
    """Forward conversation to the main LLM and return response text."""
    if settings.dry_run:
        return (
            "[Sentinel dry-run] This is a placeholder response. "
            "Set OPENAI_API_KEY in .env to get real LLM responses."
        )

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    target_model = model or settings.openai_model

    response = await client.chat.completions.create(
        model=target_model,
        messages=messages,
    )
    return response.choices[0].message.content


async def _full_analysis(prompt: str, session_id: str):
    """Run all analysis engines and return unified result."""
    # Get conversation history for drift analysis
    history = memory.get_recent_messages(session_id, n=5)

    # Run engines concurrently (they're independent)
    import asyncio
    embedding_result, redteam_result, drift_result = await asyncio.gather(
        analyze_embedding(prompt),
        analyze_redteam(prompt),
        analyze_drift(prompt, history),
    )

    # Pattern scan (sync, fast)
    pattern_result = _run_pattern_scan(prompt)

    # Classify intent
    intent = classify_intent(prompt)

    # Aggregate into risk score
    analysis = await compute_risk(
        embedding=embedding_result,
        redteam=redteam_result,
        drift=drift_result,
        pattern=pattern_result,
        intent_type=intent.value,
    )

    return analysis


# ── Routes ──────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat gateway.
    1. Analyze the latest user message
    2. Decide action (allow / warn / rewrite / block)
    3. Forward to main LLM (or block)
    4. Store in memory
    5. Return response + full analysis metadata
    """
    session_id = request.session_id or str(uuid.uuid4())
    user_messages = [m for m in request.messages if m.role.value == "user"]

    if not user_messages:
        return ChatResponse(
            response="No user message provided.",
            sentinel=SentinelMeta(
                action=ActionType.allow,
                threat_score=0.0,
                categories=[],
                intent="unknown",
                session_id=session_id,
                analysis=None,
                dry_run=settings.dry_run,
            ),
        )

    latest_prompt = user_messages[-1].content
    log.info(f"Processing chat request", session_id=session_id, prompt_len=len(latest_prompt))

    # Run full analysis
    analysis = await _full_analysis(latest_prompt, session_id)

    # Store user message + analysis
    memory.add_message(session_id, user_messages[-1], analysis)

    # Decide action
    response_text = ""
    if analysis.action == ActionType.block:
        response_text = (
            "⛔ Your message has been blocked by Sentinel-AI. "
            "The security analysis detected a high-risk prompt that violates safety guidelines."
        )
        log.threat(f"BLOCKED", session_id=session_id, score=analysis.threat_score)

    elif analysis.action == ActionType.rewrite:
        # Rewrite the prompt and forward
        rewritten = await mitigate_prompt(latest_prompt)
        messages_to_send = [
            m.model_dump() for m in request.messages[:-1]
        ] + [{"role": "user", "content": rewritten}]
        response_text = await _call_main_llm(messages_to_send, request.model)
        log.warn(f"REWRITTEN and forwarded", session_id=session_id, score=analysis.threat_score)

    else:
        # Allow or Warn — forward as-is
        messages_to_send = [m.model_dump() for m in request.messages]
        response_text = await _call_main_llm(messages_to_send, request.model)

        if analysis.action == ActionType.warn:
            response_text = (
                "⚠️ [Sentinel Warning: This prompt triggered a moderate threat score. "
                f"Score: {analysis.threat_score:.2f}]\n\n" + response_text
            )
            log.warn(f"WARNING attached", session_id=session_id, score=analysis.threat_score)
        else:
            log.info(f"ALLOWED", session_id=session_id, score=analysis.threat_score)

    # Store assistant response
    memory.add_message(session_id, Message(role="assistant", content=response_text))

    return ChatResponse(
        response=response_text,
        sentinel=SentinelMeta(
            action=analysis.action,
            threat_score=analysis.threat_score,
            categories=analysis.categories,
            intent=analysis.intent,
            session_id=session_id,
            analysis=analysis,
            dry_run=settings.dry_run,
        ),
    )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analysis-only endpoint — runs all engines but does NOT forward to the main LLM."""
    session_id = request.session_id or str(uuid.uuid4())
    user_messages = [m for m in request.messages if m.role.value == "user"]

    if not user_messages:
        from app.models import AnalysisResult
        return AnalyzeResponse(
            analysis=AnalysisResult(),
            session_id=session_id,
        )

    latest_prompt = user_messages[-1].content
    log.info(f"Analyze-only request", session_id=session_id, prompt_len=len(latest_prompt))

    analysis = await _full_analysis(latest_prompt, session_id)
    memory.add_message(session_id, user_messages[-1], analysis)

    return AnalyzeResponse(
        analysis=analysis,
        session_id=session_id,
    )
