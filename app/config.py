"""
Sentinel-AI Configuration
Loads settings from environment variables with sensible defaults.
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

    # Analysis mode
    analysis_mode: Literal["heuristic", "llm", "hybrid"] = "hybrid"

    # Threat thresholds (0.0 - 1.0)
    threat_threshold_warn: float = 0.4
    threat_threshold_block: float = 0.75

    # Session settings
    max_session_history: int = 20
    session_ttl_minutes: int = 60

    @property
    def dry_run(self) -> bool:
        """If no API key, run in dry-run mode (analysis only, placeholder LLM responses)."""
        return not self.openai_api_key or self.openai_api_key == "sk-your-key-here"

    @property
    def use_llm_analysis(self) -> bool:
        """Whether to use the Red-Team Simulation LLM for analysis."""
        return self.analysis_mode in ("llm", "hybrid") and not self.dry_run

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
