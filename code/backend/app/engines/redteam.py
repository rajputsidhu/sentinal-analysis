"""
Sentinel-AI — Module 5: Red-Team Simulation LLM
Simulates attacker interpretation of user prompts.
Uses the exact red-team prompt from the spec.
"""

import json
from openai import AsyncOpenAI
from app.config import settings
from app.models.schemas import RedTeamOutput
from app.utils.patterns import PATTERN_CATEGORIES
from app.utils.logger import log


REDTEAM_SYSTEM_PROMPT = """You are a security adversary simulator.

Your task:
Given a user prompt and conversation context, assume the user is malicious.
Identify hidden objectives, attack strategy, and what the user might be trying to exploit.

Return structured JSON:

{
  "hidden_intent": "",
  "attack_type": "",
  "sensitive_target": "",
  "exploitation_strategy": "",
  "confidence_score": 0-1
}"""


async def run_redteam(prompt: str, conversation_history: str = "") -> RedTeamOutput:
    """
    Run Red-Team adversarial simulation.
    Uses LLM when available, falls back to heuristic.
    """
    if settings.use_llm:
        return await _llm_redteam(prompt, conversation_history)
    return _heuristic_redteam(prompt)


async def _llm_redteam(prompt: str, conversation_history: str) -> RedTeamOutput:
    """Call the LLM with the red-team prompt."""
    client = AsyncOpenAI(api_key=settings.openai_api_key)

    user_content = f"Conversation Context:\n{conversation_history}\n\nUser Prompt:\n{prompt}"

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": REDTEAM_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.1,
            max_tokens=400,
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        data = json.loads(raw)
        result = RedTeamOutput(
            hidden_intent=data.get("hidden_intent", ""),
            attack_type=data.get("attack_type", ""),
            sensitive_target=data.get("sensitive_target", ""),
            exploitation_strategy=data.get("exploitation_strategy", ""),
            confidence_score=round(float(data.get("confidence_score", 0.0)), 4),
        )
        log.debug(f"Red-team LLM complete", confidence=result.confidence_score, attack=result.attack_type)
        return result

    except Exception as e:
        log.error(f"Red-team LLM failed, using heuristic", error=str(e))
        return _heuristic_redteam(prompt)


def _heuristic_redteam(prompt: str) -> RedTeamOutput:
    """Pattern-based red-team fallback for dry-run mode."""
    matched_categories = []
    for cat_name, patterns in PATTERN_CATEGORIES.items():
        for pattern in patterns:
            if pattern.search(prompt):
                matched_categories.append(cat_name)
                break

    if not matched_categories:
        return RedTeamOutput(
            hidden_intent="none detected",
            attack_type="none",
            sensitive_target="none",
            exploitation_strategy="none detected",
            confidence_score=0.0,
        )

    confidence = min(len(matched_categories) * 0.25 + 0.2, 1.0)
    attack_type = matched_categories[0]

    return RedTeamOutput(
        hidden_intent=f"Possible {', '.join(matched_categories)} attempt",
        attack_type=attack_type,
        sensitive_target="system prompt / safety filters" if "data_exfiltration" in matched_categories or "instruction_hijack" in matched_categories else "safety guardrails",
        exploitation_strategy=f"Pattern match: {', '.join(matched_categories)}",
        confidence_score=round(confidence, 4),
    )
