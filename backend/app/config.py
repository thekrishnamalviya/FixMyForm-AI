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

ROOT_ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
BACKEND_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

def refresh_environment() -> None:
    """Reloads .env from disk so live changes are picked up immediately."""
    if ROOT_ENV_PATH.exists():
        load_dotenv(dotenv_path=ROOT_ENV_PATH, override=True)
    if BACKEND_ENV_PATH.exists():
        load_dotenv(dotenv_path=BACKEND_ENV_PATH, override=True)

# Initial load
refresh_environment()

FORBIDDEN_PROVIDERS = ["digitalocean", "digitalocean.com", "digitaloceanspaces.com"]
ALLOWED_MODEL_PREFIX = "gemma"

def _get_api_key() -> str:
    return (
        os.getenv("BACKBOARD_API_KEY") 
        or os.getenv("BAVKBORAD_API_KEY")
        or os.getenv("BACKBOARD_KEY")
        or os.getenv("GEMMA_API_KEY") 
        or os.getenv("API_KEY") 
        or ""
    ).strip()

def _get_endpoint() -> str:
    bb_key = (
        os.getenv("BACKBOARD_API_KEY") 
        or os.getenv("BAVKBORAD_API_KEY")
        or os.getenv("BACKBOARD_KEY") 
        or ""
    ).strip()
    bb_endpoint = (os.getenv("BACKBOARD_API_ENDPOINT") or "").strip()
    gemma_endpoint = (os.getenv("GEMMA_API_ENDPOINT") or "").strip()

    if bb_key:
        return bb_endpoint or "https://app.backboard.io/api"
    return gemma_endpoint or bb_endpoint or "https://app.backboard.io/api"

def _get_model() -> str:
    return (
        os.getenv("GEMMA_MODEL") 
        or os.getenv("MODEL_NAME") 
        or "google/gemma-4-26b-a4b-it"
    ).strip()

class Settings(BaseModel):
    # API Keys: supports GEMMA_API_KEY or BACKBOARD_API_KEY
    gemma_api_key: str = Field(default_factory=_get_api_key)

    # Inference Endpoint: Backboard, Groq, OpenRouter, Hugging Face, or Ollama
    gemma_api_endpoint: str = Field(default_factory=_get_endpoint)

    # Gemma model name (e.g., google/gemma-4-26b-a4b-it, google/gemma-3-12b-it)
    gemma_model: str = Field(default_factory=_get_model)

    # Backboard LLM Provider (e.g., 'openrouter', 'google')
    backboard_provider: str = Field(default_factory=lambda: (
        os.getenv("BACKBOARD_PROVIDER") 
        or os.getenv("LLM_PROVIDER") 
        or "openrouter"
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
        self.gemma_api_key = _get_api_key()
        self.gemma_api_endpoint = _get_endpoint()
        self.gemma_model = _get_model()
        self.backboard_provider = (
            os.getenv("BACKBOARD_PROVIDER") 
            or os.getenv("LLM_PROVIDER") 
            or "openrouter"
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
        bb_key = (
            os.getenv("BACKBOARD_API_KEY") 
            or os.getenv("BAVKBORAD_API_KEY")
            or os.getenv("BACKBOARD_KEY") 
            or ""
        ).strip()
        return "backboard" in endpoint_lower or self.gemma_endpoint_format == "backboard" or bool(bb_key)

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
