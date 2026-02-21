"""
Sentinel-AI — Module 1: POST /analyze Route
Full pipeline: intake → memory → embed → drift → red-team → blue-team → score → mitigate → LLM → explain → log
"""

import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, RiskAnalysis
from app.engines.memory import get_or_create_conversation, load_conversation_history, load_embedding_history, save_message
from app.engines.embedding import generate_embedding, get_store
from app.engines.drift import compute_drift
from app.engines.redteam import run_redteam
from app.engines.blueteam import run_blueteam
from app.engines.risk_scorer import compute_risk
from app.engines.mitigation import rewrite_prompt
from app.engines.explainability import generate_explanation
from app.utils.llm_client import chat_completion
from app.utils.logger import log


router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest, db: AsyncSession = Depends(get_db)):
    """
    Full Sentinel-AI analysis pipeline.

    Flow:
        1. Intake request
        2. Load conversation memory
        3. Generate embedding
        4. Compute drift score
        5. Run Red-Team LLM
        6. Run Blue-Team LLM
        7. Compute unified risk score
        8. Decide action (allow/warn/rewrite/block)
        9. Rewrite if needed
        10. Forward to Main LLM if allowed
        11. Generate explanation
        12. Log everything
        13. Return response
    """
    prompt = request.prompt
    log.info(f"Analyzing prompt", conversation_id=request.conversation_id, user_id=request.user_id, length=len(prompt))

    # ── 2. Load Memory ──
    await get_or_create_conversation(db, request.conversation_id, request.user_id)
    history = await load_conversation_history(db, request.conversation_id)
    prior_embeddings = await load_embedding_history(db, request.conversation_id)
    turn_number = len(history) + 1

    # Build conversation context string for LLM prompts
    context_str = "\n".join(f"{m['role']}: {m['content']}" for m in history[-5:])

    # ── 3. Generate Embedding ──
    current_embedding = await generate_embedding(prompt)

    # Store in FAISS index
    store = get_store(request.conversation_id)
    store.add(current_embedding)

    # ── 4. Compute Drift ──
    drift_info = await compute_drift(current_embedding, prior_embeddings, turn_number)

    # ── 5. Red-Team LLM ──
    red_team_result = await run_redteam(prompt, context_str)

    # ── 6. Blue-Team LLM ──
    blue_team_result = await run_blueteam(prompt, red_team_result)

    # ── 7. Compute Risk Score ──
    risk_analysis = compute_risk(red_team_result, blue_team_result, drift_info)

    # ── 8+9. Mitigation ──
    rewritten = None
    final_prompt = prompt

    if risk_analysis.action == "rewrite":
        rewritten = await rewrite_prompt(prompt)
        final_prompt = rewritten
        log.info(f"Prompt rewritten", original_len=len(prompt), rewritten_len=len(rewritten))

    # ── 10. Forward to Main LLM ──
    response_text = ""
    if risk_analysis.action == "block":
        response_text = "⛔ This request has been blocked by Sentinel-AI security gateway. The prompt was identified as potentially malicious."
        log.threat(f"BLOCKED", score=f"{risk_analysis.final_score:.0f}", categories=risk_analysis.categories)
    elif settings.dry_run:
        response_text = "[Sentinel dry-run] Placeholder response. Set OPENAI_API_KEY for real LLM responses."
        log.info(f"Dry-run response", action=risk_analysis.action)
    else:
        response_text = await _call_main_llm(final_prompt, history)

    # ── 11. Generate Explanation ──
    explanation = await generate_explanation(prompt, risk_analysis)

    # ── 12. Log to Database ──
    await save_message(
        db,
        conversation_id=request.conversation_id,
        role="user",
        content=prompt,
        embedding=current_embedding,
        drift_score=drift_info.score,
        risk_score=risk_analysis.final_score,
        action=risk_analysis.action,
        red_team_result=red_team_result.model_dump(),
        blue_team_result=blue_team_result.model_dump(),
    )

    await save_message(
        db,
        conversation_id=request.conversation_id,
        role="assistant",
        content=response_text,
    )

    log.info(
        f"Analysis complete",
        action=risk_analysis.action,
        score=f"{risk_analysis.final_score:.0f}/100",
        drift=f"{drift_info.score:.3f}",
    )

    # ── 13. Return ──
    return AnalyzeResponse(
        response=response_text,
        risk_analysis=risk_analysis,
        explanation=explanation,
        drift_score=drift_info.score,
        action_taken=risk_analysis.action,
        original_prompt=prompt,
        rewritten_prompt=rewritten,
        conversation_id=request.conversation_id,
        dry_run=settings.dry_run,
    )


async def _call_main_llm(prompt: str, history: list[dict]) -> str:
    """Forward the (possibly rewritten) prompt to the main LLM."""
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})

    try:
        return await chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
    except Exception as e:
        log.error(f"Main LLM call failed", error=str(e))
        return f"[Error] Unable to generate response: {str(e)}"
