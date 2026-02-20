"""
Sentinel-AI — Configuration
Settings loaded from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # Server
    port: int = 8000

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"

    # Database
    database_url: str = "sqlite+aiosqlite:///./sentinel.db"

    # Analysis mode
    analysis_mode: Literal["heuristic", "llm", "hybrid"] = "hybrid"

    # Scoring thresholds (0–100)
    threshold_allow: int = 40
    threshold_warn: int = 70
    threshold_rewrite: int = 85

    # Session
    max_conversation_history: int = 20
    session_ttl_minutes: int = 60

    @property
    def dry_run(self) -> bool:
        """If no API key, run in dry-run mode."""
        return not self.openai_api_key or self.openai_api_key == "sk-your-key-here"

    @property
    def use_llm(self) -> bool:
        """Whether LLM-based analysis is available."""
        return self.analysis_mode in ("llm", "hybrid") and not self.dry_run

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
