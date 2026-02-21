"""
Sentinel-AI — Unified LLM Client
Supports both OpenAI and Google Gemini as LLM providers.
Includes retry logic for rate-limited APIs.
"""

import asyncio
import json
from app.config import settings
from app.utils.logger import log


async def chat_completion(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str:
    """
    Unified chat completion that routes to OpenAI or Gemini
    based on the LLM_PROVIDER setting.
    """
    provider = settings.llm_provider.lower()

    if provider == "gemini":
        return await _gemini_chat_with_retry(messages, temperature, max_tokens)
    elif provider == "groq":
        return await _groq_chat(messages, temperature, max_tokens)
    else:
        return await _openai_chat(messages, temperature, max_tokens)


async def _openai_chat(
    messages: list[dict],
    temperature: float,
    max_tokens: int,
) -> str:
    """Call OpenAI chat completion."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


async def _groq_chat(
    messages: list[dict],
    temperature: float,
    max_tokens: int,
) -> str:
    """Call Groq chat completion (OpenAI-compatible API)."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    response = await client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


async def _gemini_chat_with_retry(
    messages: list[dict],
    temperature: float,
    max_tokens: int,
    max_retries: int = 4,
) -> str:
    """Call Gemini with retry + backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            return await _gemini_chat(messages, temperature, max_tokens)
        except Exception as e:
            error_str = str(e)
            is_rate_limit = "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower()

            if is_rate_limit and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 3  # 3s, 6s, 9s
                log.warn(f"Gemini rate limit hit, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                raise


async def _gemini_chat(
    messages: list[dict],
    temperature: float,
    max_tokens: int,
) -> str:
    """Call Google Gemini chat completion."""
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)

    # Convert OpenAI message format to Gemini format
    system_instruction = ""
    gemini_history = []
    last_user_msg = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            system_instruction += content + "\n"
        elif role == "assistant":
            gemini_history.append({"role": "model", "parts": [content]})
        elif role == "user":
            last_user_msg = content
            gemini_history.append({"role": "user", "parts": [content]})

    # Build model with optional system instruction
    model_kwargs = {
        "model_name": settings.gemini_model,
        "generation_config": {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        },
    }
    if system_instruction.strip():
        model_kwargs["system_instruction"] = system_instruction.strip()

    model = genai.GenerativeModel(**model_kwargs)

    # Start chat with history (excluding the last user message)
    chat_history = gemini_history[:-1] if gemini_history else []
    cleaned_history = _clean_gemini_history(chat_history)

    chat = model.start_chat(history=cleaned_history)
    response = await chat.send_message_async(last_user_msg or "Hello")

    return response.text.strip()


def _clean_gemini_history(history: list[dict]) -> list[dict]:
    """Ensure history has alternating user/model roles for Gemini."""
    if not history:
        return []

    cleaned = []
    last_role = None

    for msg in history:
        role = msg["role"]
        if role == last_role:
            cleaned[-1]["parts"][0] += "\n" + msg["parts"][0]
        else:
            cleaned.append(msg)
            last_role = role

    return cleaned

