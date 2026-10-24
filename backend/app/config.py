"""Configuration module for FixMyForm AI.

Strict Requirements:
1. Gemma is the ONLY AI model allowed for document understanding and analysis.
2. DigitalOcean is explicitly forbidden as an AI provider.
3. Proprietary model APIs and non-Gemma models are strictly rejected.
4. API key is read securely from backend environment variables (.env) via python-dotenv.
5. Never expose raw API keys in logs or client-facing responses.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

def refresh_environment() -> None:
    """Reloads .env from disk so live changes are picked up immediately."""
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH, override=True)
    else:
        load_dotenv(override=True)

# Initial load
refresh_environment()

FORBIDDEN_PROVIDERS = ["digitalocean", "digitalocean.com", "digitaloceanspaces.com"]
ALLOWED_MODEL_PREFIX = "gemma"

class Settings(BaseModel):
    # API Keys: supports GEMMA_API_KEY or BACKBOARD_API_KEY
    gemma_api_key: str = Field(default_factory=lambda: (
        os.getenv("BACKBOARD_API_KEY") 
        or os.getenv("GEMMA_API_KEY") 
        or os.getenv("API_KEY") 
        or ""
    ).strip())

    # Inference Endpoint: Backboard, Groq, OpenRouter, Hugging Face, or Ollama
    gemma_api_endpoint: str = Field(default_factory=lambda: (
        os.getenv("BACKBOARD_API_ENDPOINT")
        or os.getenv("GEMMA_API_ENDPOINT")
        or "https://app.backboard.io/api"
    ).strip())

    # Gemma model name (e.g., google/gemma-4, google/gemma-3-12b-it, gemma2-9b-it)
    gemma_model: str = Field(default_factory=lambda: (
        os.getenv("GEMMA_MODEL") 
        or os.getenv("MODEL_NAME") 
        or "google/gemma-4"
    ).strip())

    # Backboard LLM Provider (e.g., 'google', 'openrouter')
    backboard_provider: str = Field(default_factory=lambda: (
        os.getenv("BACKBOARD_PROVIDER") 
        or os.getenv("LLM_PROVIDER") 
        or "google"
    ).strip().lower())

    # Format override: 'auto', 'backboard', or 'openai_compatible'
    gemma_endpoint_format: str = Field(default_factory=lambda: (
        os.getenv("GEMMA_ENDPOINT_FORMAT") or "auto"
    ).strip().lower())

    # Local Tesseract OCR path
    tesseract_cmd: Optional[str] = Field(default_factory=lambda: os.getenv("TESSERACT_CMD", None))

    # Limits
    max_upload_size_mb: int = 25
    demo_mode_forced: bool = Field(default_factory=lambda: (
        os.getenv("DEMO_MODE_FORCED", "false").lower() in ("true", "1", "yes")
    ))

    def reload(self) -> None:
        """Refreshes settings from current environment."""
        refresh_environment()
        self.gemma_api_key = (
            os.getenv("BACKBOARD_API_KEY") 
            or os.getenv("GEMMA_API_KEY") 
            or os.getenv("API_KEY") 
            or ""
        ).strip()
        self.gemma_api_endpoint = (
            os.getenv("BACKBOARD_API_ENDPOINT")
            or os.getenv("GEMMA_API_ENDPOINT")
            or "https://app.backboard.io/api"
        ).strip()
        self.gemma_model = (
            os.getenv("GEMMA_MODEL") 
            or os.getenv("MODEL_NAME") 
            or "google/gemma-4"
        ).strip()
        self.backboard_provider = (
            os.getenv("BACKBOARD_PROVIDER") 
            or os.getenv("LLM_PROVIDER") 
            or "google"
        ).strip().lower()

    def is_gemma_configured(self) -> bool:
        """Returns True if a valid API key is present and demo mode is not forced."""
        self.reload()
        if self.demo_mode_forced:
            return False
        return bool(self.gemma_api_key and len(self.gemma_api_key) > 5)

    def is_backboard(self) -> bool:
        """Detects whether endpoint is Backboard API."""
        endpoint_lower = self.gemma_api_endpoint.lower()
        return "backboard" in endpoint_lower or self.gemma_endpoint_format == "backboard"

    def get_masked_api_key(self) -> str:
        """Returns securely masked API key (never reveals secret)."""
        if not self.gemma_api_key:
            return "not-configured"
        if len(self.gemma_api_key) <= 8:
            return "****"
        return f"{self.gemma_api_key[:4]}****{self.gemma_api_key[-4:]}"

    def validate_constraints(self) -> None:
        """Enforces architectural constraints:
        - DigitalOcean is strictly forbidden.
        - Gemma is the only model allowed.
        """
        endpoint_lower = self.gemma_api_endpoint.lower()
        for forbidden in FORBIDDEN_PROVIDERS:
            if forbidden in endpoint_lower:
                raise ValueError(
                    f"Violation of strict constraint: Provider '{forbidden}' is not permitted. "
                    "Use official Gemma endpoints (Backboard, Groq, OpenRouter, or Ollama)."
                )

        model_lower = self.gemma_model.lower()
        if ALLOWED_MODEL_PREFIX not in model_lower:
            raise ValueError(
                f"Violation of strict constraint: Model '{self.gemma_model}' is not a Gemma model. "
                "FixMyForm AI is strictly designed to use Gemma exclusively. "
                "Do not silently use another AI model."
            )

settings = Settings()
try:
    settings.validate_constraints()
except Exception as e:
    print(f"[CONFIGURATION WARNING] {e}")
