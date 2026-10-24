"""Gemma Document Intelligence Service for FixMyForm AI.

Strictly integrates Google Gemma as the ONLY AI model for form understanding and analysis.
Adheres to strict project constraints:
1. Only Gemma models allowed (Gemma 4 / Gemma 3 variants).
2. DigitalOcean is strictly rejected as an AI provider.
3. Proprietary model APIs are not integrated.
4. Supports Backboard API (https://app.backboard.io/api) with X-API-Key and standard endpoints.
5. Verifies whether Gemma is available through configured provider (no silent fallback).
6. Demands explicit source grounding for deadlines, required fields, and required documents.
7. Produces bilingual explanations (Simple English & Hindi/Hinglish).
8. Real API request validation: Do not claim model works until a real API request succeeds.
"""

import os
import json
import re
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import httpx

from app.config import settings
from app.models import (
    FormAnalysisResult,
    DeadlineItem,
    RequiredDocumentItem,
    RequiredFieldItem,
    InstructionStep,
    MissingInfoChecklistItem,
    TestConnectionResult,
)

logger = logging.getLogger(__name__)

class GemmaNotConfiguredError(Exception):
    """Raised when Gemma inference is requested without API configuration."""
    pass

class GemmaConstraintViolationError(Exception):
    """Raised if an unpermitted provider or non-Gemma model is configured."""
    pass

class GemmaAuthenticationError(Exception):
    """Raised when API key is invalid or rejected by provider."""
    pass

class GemmaModelUnavailableError(Exception):
    """Raised when the requested Gemma model is not supported by the provider."""
    pass


GEMMA_SYSTEM_PROMPT = """You are Gemma, an advanced open foundation AI model developed by Google, specializing in document understanding, administrative compliance, and form analysis.

Your goal is to parse and explain bureaucratic, official, government, employment, or academic application forms with 100% factual accuracy.

CRITICAL INSTRUCTIONS:
1. DEADLINES: ONLY extract deadlines, cutoffs, validity windows, and dates that are EXPLICITLY STATED in the source document. Do NOT invent, assume, or hallucinate dates. If no deadline is stated in the document, return an empty list for deadlines.
2. REQUIRED FIELDS: Extract all key form fields that the applicant must fill out, their type, mandatory status, and specific validation rules.
3. REQUIRED DOCUMENTS: Identify every required document, certificate, affidavit, and photo specification explicitly mentioned. Include the exact source quote and clause/page reference where possible.
4. DUAL EXPLANATIONS: For every instruction step and overall summary, provide TWO distinct explanations:
   - English: Plain, clear, jargon-free English that anyone can understand without bureaucratic complexity.
   - Hinglish / Hindi: Natural, conversational, clear Hindi written in Hinglish (Roman script, e.g., "Aapka naam 10th marksheet aur Aadhaar card mein bilkul match karna chahiye...") so that Indian applicants can follow without confusion.
5. MISSING INFORMATION CHECKLIST: Create a specific checklist of items, fields, or documents the applicant must confirm before final submission, with actionable tips and source references.
6. FACTUALITY & SOURCE GROUNDING: Cite exact quotes (`source_quote`) from the text whenever possible.

You must respond ONLY with a valid, clean JSON object matching this exact schema:
{
  "form_title": "Official Title of the Form",
  "issuing_organization": "Issuing Authority / Organization / Department",
  "form_purpose": "Brief purpose of this application",
  "summary_english": "Plain English summary of the form and its requirements",
  "summary_hinglish": "Clear Hinglish summary of the form and its requirements",
  "deadlines": [
    {
      "title": "Name of the deadline",
      "date_or_time": "Exact stated date, time, or period",
      "category": "submission" | "fee_payment" | "correction" | "validity" | "other",
      "urgency": "high" | "medium" | "low",
      "source_quote": "Exact quote from document stating this deadline",
      "source_reference": "Section or Page number"
    }
  ],
  "required_fields": [
    {
      "field_name": "Field Label",
      "field_type": "text" | "date" | "number" | "dropdown" | "signature",
      "description": "What to enter",
      "is_mandatory": true | false,
      "validation_rules": "Format or matching constraints",
      "source_reference": "Section reference"
    }
  ],
  "required_documents": [
    {
      "name": "Document Name",
      "acceptable_types": ["Alternative 1", "Alternative 2"],
      "format_and_specs": "Format, size, self-attestation, or background rules",
      "is_mandatory": true | false,
      "source_quote": "Exact quote from source specifying this requirement",
      "source_reference": "Section or Page reference"
    }
  ],
  "instructions": [
    {
      "step_number": 1,
      "title": "Clear step title",
      "english_explanation": "Simplified plain English explanation",
      "hinglish_explanation": "Conversational Hinglish explanation",
      "critical_warning": "Warning about common mistakes or penalties",
      "source_reference": "Clause or Section"
    }
  ],
  "missing_info_checklist": [
    {
      "id": "chk-1",
      "field_name": "Specific detail or field to verify",
      "category": "personal" | "academic" | "financial" | "declaration" | "document",
      "why_needed": "Why this specific field is needed",
      "english_tip": "Plain English advice",
      "hinglish_tip": "Hinglish advice",
      "source_reference": "Document reference",
      "is_checked": false
    }
  ]
}
"""


def clean_json_response(raw_text: str) -> str:
    """Strips markdown code blocks and repairs minor JSON syntax errors."""
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1].strip()
    text = re.sub(r",\s*([\]}])", r"\1", text)
    return text


class GemmaInferenceService:
    def get_config(self):
        settings.reload()
        return settings

    def validate_service_constraints(self) -> None:
        """Enforces Gemma exclusivity and rejects forbidden providers."""
        cfg = self.get_config()
        cfg.validate_constraints()

    async def test_model_connection(self) -> TestConnectionResult:
        """Tests live connection to the configured Gemma model provider.

        Do NOT claim the model works until a real API request succeeds.
        Checks for:
        - Valid API key (handles 401)
        - Provider reachability
        - Gemma model availability on the provider
        - End-to-end inference round-trip
        """
        cfg = self.get_config()

        # 1. Check if key is configured
        if not cfg.is_gemma_configured():
            return TestConnectionResult(
                success=False,
                provider="None",
                model=cfg.gemma_model,
                endpoint=cfg.gemma_api_endpoint,
                masked_key="not-configured",
                gemma_verified=False,
                latency_ms=0.0,
                message="API key is not configured in backend/.env.",
                error_detail="Please add your GEMMA_API_KEY or BACKBOARD_API_KEY to backend/.env and save the file."
            )

        # 2. Check strict constraints
        try:
            cfg.validate_constraints()
        except ValueError as err:
            return TestConnectionResult(
                success=False,
                provider="Forbidden Provider / Model",
                model=cfg.gemma_model,
                endpoint=cfg.gemma_api_endpoint,
                masked_key=cfg.get_masked_api_key(),
                gemma_verified=False,
                latency_ms=0.0,
                message=str(err),
                error_detail="FixMyForm AI strictly permits Gemma models only and rejects forbidden providers."
            )

        start_time = time.time()
        is_backboard = cfg.is_backboard()

        async with httpx.AsyncClient(timeout=30.0) as client:
            if is_backboard:
                return await self._test_backboard_connection(client, cfg, start_time)
            else:
                return await self._test_openai_compatible_connection(client, cfg, start_time)

    async def _test_backboard_connection(
        self,
        client: httpx.AsyncClient,
        cfg: Any,
        start_time: float
    ) -> TestConnectionResult:
        """Verifies Backboard API connection, model catalog, and performs live ping."""
        base_url = cfg.gemma_api_endpoint.rstrip("/")
        if not base_url.endswith("/api"):
            base_url = f"{base_url}/api" if not base_url.endswith("/api") else base_url

        headers = {
            "X-API-Key": cfg.gemma_api_key,
            "Content-Type": "application/json"
        }

        # Step A: Query models to check authentication and discover Gemma models
        gemma_models_found = []
        try:
            models_res = await client.get(
                f"{base_url}/models?limit=100",
                headers=headers
            )
            if models_res.status_code == 401:
                return TestConnectionResult(
                    success=False,
                    provider="Backboard API",
                    model=cfg.gemma_model,
                    endpoint=base_url,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=round((time.time() - start_time) * 1000, 2),
                    message="Authentication failed (HTTP 401): Invalid or missing Backboard API key.",
                    error_detail=models_res.text
                )
            elif models_res.status_code == 200:
                models_data = models_res.json()
                if isinstance(models_data, list):
                    for m in models_data:
                        name = m.get("model_name", "") or m.get("id", "")
                        if "gemma" in name.lower():
                            gemma_models_found.append(name)
        except httpx.RequestError as e:
            return TestConnectionResult(
                success=False,
                provider="Backboard API",
                model=cfg.gemma_model,
                endpoint=base_url,
                masked_key=cfg.get_masked_api_key(),
                gemma_verified=False,
                latency_ms=round((time.time() - start_time) * 1000, 2),
                message="Network error connecting to Backboard API.",
                error_detail=str(e)
            )

        # Step B: Perform a real message test call with configured Gemma model
        messages_url = f"{base_url}/threads/messages"
        payload = {
            "content": "Respond with the word 'OK' only to verify model connection.",
            "model_name": cfg.gemma_model,
            "llm_provider": cfg.backboard_provider or "google",
            "stream": False
        }

        try:
            msg_res = await client.post(messages_url, headers=headers, json=payload)
            latency = round((time.time() - start_time) * 1000, 2)

            if msg_res.status_code == 401:
                return TestConnectionResult(
                    success=False,
                    provider="Backboard API",
                    model=cfg.gemma_model,
                    endpoint=messages_url,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message="Authentication failed (HTTP 401): Invalid Backboard API key.",
                    error_detail=msg_res.text
                )
            elif msg_res.status_code == 400 or msg_res.status_code == 404:
                err_text = msg_res.text
                return TestConnectionResult(
                    success=False,
                    provider="Backboard API",
                    model=cfg.gemma_model,
                    endpoint=messages_url,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message=f"Gemma model '{cfg.gemma_model}' not available through Backboard provider '{cfg.backboard_provider}'.",
                    error_detail=f"Provider response ({msg_res.status_code}): {err_text}",
                    available_gemma_models=gemma_models_found
                )
            elif msg_res.status_code == 429:
                return TestConnectionResult(
                    success=False,
                    provider="Backboard API",
                    model=cfg.gemma_model,
                    endpoint=messages_url,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message="Provider rate limit reached (HTTP 429). Please wait before retrying.",
                    error_detail=msg_res.text
                )

            msg_res.raise_for_status()
            data = msg_res.json()
            content = data.get("content", "")

            if data.get("status") == "FAILED" or "LLM Error" in content:
                return TestConnectionResult(
                    success=False,
                    provider="Backboard API",
                    model=cfg.gemma_model,
                    endpoint=messages_url,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message=f"Model execution failed on Backboard: {content}",
                    error_detail=content,
                    available_gemma_models=gemma_models_found
                )

            return TestConnectionResult(
                success=True,
                provider="Backboard API",
                model=cfg.gemma_model,
                endpoint=messages_url,
                masked_key=cfg.get_masked_api_key(),
                gemma_verified=True,
                latency_ms=latency,
                message=f"Live connection verified! Successfully executed inference with {cfg.gemma_model}.",
                available_gemma_models=gemma_models_found
            )
        except Exception as e:
            latency = round((time.time() - start_time) * 1000, 2)
            return TestConnectionResult(
                success=False,
                provider="Backboard API",
                model=cfg.gemma_model,
                endpoint=messages_url,
                masked_key=cfg.get_masked_api_key(),
                gemma_verified=False,
                latency_ms=latency,
                message=f"Failed to communicate with Gemma via Backboard: {e}",
                error_detail=str(e),
                available_gemma_models=gemma_models_found
            )

    async def _test_openai_compatible_connection(
        self,
        client: httpx.AsyncClient,
        cfg: Any,
        start_time: float
    ) -> TestConnectionResult:
        """Verifies OpenAI-compatible endpoint (Groq / OpenRouter / Ollama / vLLM)."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg.gemma_api_key}"
        }
        payload = {
            "model": cfg.gemma_model,
            "messages": [
                {"role": "user", "content": "Respond with the word 'OK' only to verify model connection."}
            ],
            "max_tokens": 10
        }

        try:
            res = await client.post(cfg.gemma_api_endpoint, headers=headers, json=payload)
            latency = round((time.time() - start_time) * 1000, 2)

            if res.status_code == 401:
                return TestConnectionResult(
                    success=False,
                    provider="OpenAI-compatible Endpoint",
                    model=cfg.gemma_model,
                    endpoint=cfg.gemma_api_endpoint,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message="Authentication failed (HTTP 401): Invalid API key.",
                    error_detail=res.text
                )
            elif res.status_code == 404 or res.status_code == 400:
                return TestConnectionResult(
                    success=False,
                    provider="OpenAI-compatible Endpoint",
                    model=cfg.gemma_model,
                    endpoint=cfg.gemma_api_endpoint,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message=f"Model '{cfg.gemma_model}' not found or unsupported by configured endpoint.",
                    error_detail=res.text
                )
            elif res.status_code == 429:
                return TestConnectionResult(
                    success=False,
                    provider="OpenAI-compatible Endpoint",
                    model=cfg.gemma_model,
                    endpoint=cfg.gemma_api_endpoint,
                    masked_key=cfg.get_masked_api_key(),
                    gemma_verified=False,
                    latency_ms=latency,
                    message="Provider rate limit reached (HTTP 429).",
                    error_detail=res.text
                )

            res.raise_for_status()
            return TestConnectionResult(
                success=True,
                provider="OpenAI-compatible Endpoint",
                model=cfg.gemma_model,
                endpoint=cfg.gemma_api_endpoint,
                masked_key=cfg.get_masked_api_key(),
                gemma_verified=True,
                latency_ms=latency,
                message=f"Live connection verified! Successfully executed inference with {cfg.gemma_model}."
            )
        except Exception as e:
            latency = round((time.time() - start_time) * 1000, 2)
            return TestConnectionResult(
                success=False,
                provider="OpenAI-compatible Endpoint",
                model=cfg.gemma_model,
                endpoint=cfg.gemma_api_endpoint,
                masked_key=cfg.get_masked_api_key(),
                gemma_verified=False,
                latency_ms=latency,
                message=f"Connection failure: {e}",
                error_detail=str(e)
            )

    async def analyze_document_with_gemma(
        self,
        document_text: str,
        document_name: str,
        page_count: int = 1
    ) -> FormAnalysisResult:
        """Sends extracted document text to Gemma inference endpoint."""
        cfg = self.get_config()

        # Strict Check: Is Gemma API configured?
        if not cfg.is_gemma_configured():
            raise GemmaNotConfiguredError(
                "Gemma API key is not configured in backend environment variables. "
                "FixMyForm AI strictly refuses to fake AI responses. "
                "Please configure GEMMA_API_KEY in backend/.env, or switch to Demo Mode to view verified sample analyses."
            )

        # Strict Check: Forbidden providers & model constraints
        cfg.validate_constraints()

        max_chars = 24000
        truncated_text = document_text[:max_chars]
        if len(document_text) > max_chars:
            truncated_text += "\n\n[... Text truncated for model context limit ...]"

        user_prompt = f"""DOCUMENT NAME: {document_name}
PAGE COUNT: {page_count}

EXTRACTED DOCUMENT CONTENT:
\"\"\"
{truncated_text}
\"\"\"

Analyze this form document using Gemma. Follow all prompt instructions strictly. Output valid JSON only."""

        is_backboard = cfg.is_backboard()
        raw_content = ""

        async with httpx.AsyncClient(timeout=120.0) as client:
            if is_backboard:
                base_url = cfg.gemma_api_endpoint.rstrip("/")
                if not base_url.endswith("/api"):
                    base_url = f"{base_url}/api"
                messages_url = f"{base_url}/threads/messages"

                headers = {
                    "X-API-Key": cfg.gemma_api_key,
                    "Content-Type": "application/json"
                }
                payload = {
                    "content": f"{GEMMA_SYSTEM_PROMPT}\n\n{user_prompt}",
                    "model_name": cfg.gemma_model,
                    "llm_provider": cfg.backboard_provider or "google",
                    "json_output": True,
                    "stream": False
                }

                logger.info(f"Invoking Gemma via Backboard at: {messages_url} (model={cfg.gemma_model}, provider={cfg.backboard_provider})")
                try:
                    res = await client.post(messages_url, headers=headers, json=payload)
                    if res.status_code == 401:
                        raise GemmaAuthenticationError("Invalid or missing Backboard API key (HTTP 401).")
                    elif res.status_code in (400, 404):
                        raise GemmaModelUnavailableError(
                            f"Gemma model '{cfg.gemma_model}' is not available on Backboard provider '{cfg.backboard_provider}'. Error: {res.text}"
                        )
                    res.raise_for_status()
                    data = res.json()
                    if data.get("status") == "FAILED" or "LLM Error" in str(data.get("content", "")):
                        err_msg = data.get("content", "Unknown error from Backboard provider")
                        raise GemmaModelUnavailableError(
                            f"Backboard error: {err_msg}"
                        )
                    raw_content = data.get("content", "")
                except httpx.HTTPStatusError as e:
                    raise RuntimeError(f"Backboard API HTTP {e.response.status_code}: {e.response.text}")
                except Exception as e:
                    if isinstance(e, (GemmaAuthenticationError, GemmaModelUnavailableError)):
                        raise e
                    raise RuntimeError(f"Network error connecting to Backboard API: {e}")
            else:
                # Standard OpenAI-compatible endpoint
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {cfg.gemma_api_key}"
                }
                payload = {
                    "model": cfg.gemma_model,
                    "messages": [
                        {"role": "system", "content": GEMMA_SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 4096
                }

                logger.info(f"Invoking Gemma at: {cfg.gemma_api_endpoint} (model={cfg.gemma_model})")
                try:
                    res = await client.post(cfg.gemma_api_endpoint, headers=headers, json=payload)
                    if res.status_code == 401:
                        raise GemmaAuthenticationError("Invalid API key (HTTP 401).")
                    elif res.status_code in (400, 404):
                        raise GemmaModelUnavailableError(
                            f"Model '{cfg.gemma_model}' not found on endpoint. Error: {res.text}"
                        )
                    res.raise_for_status()
                    data = res.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        raw_content = data["choices"][0]["message"]["content"]
                    else:
                        raw_content = json.dumps(data)
                except httpx.HTTPStatusError as e:
                    raise RuntimeError(f"Gemma inference failed ({e.response.status_code}): {e.response.text}")
                except Exception as e:
                    if isinstance(e, (GemmaAuthenticationError, GemmaModelUnavailableError)):
                        raise e
                    raise RuntimeError(f"Network error connecting to Gemma endpoint: {e}")

        # Parse & Validate structured JSON
        clean_json_str = clean_json_response(raw_content)
        try:
            parsed = json.loads(clean_json_str, strict=False)
        except json.JSONDecodeError as err:
            logger.error(f"Failed to decode Gemma JSON: {err}. Raw content: {clean_json_str[:500]}")
            raise ValueError(f"Gemma returned invalid JSON response: {err}")

        deadlines = [DeadlineItem(**d) for d in parsed.get("deadlines", [])]
        documents = [RequiredDocumentItem(**doc) for doc in parsed.get("required_documents", [])]
        fields = [RequiredFieldItem(**f) for f in parsed.get("required_fields", [])]
        instructions = [InstructionStep(**inst) for inst in parsed.get("instructions", [])]
        
        checklist_items = []
        for idx, chk in enumerate(parsed.get("missing_info_checklist", [])):
            if "id" not in chk:
                chk["id"] = f"chk-{idx + 1}"
            checklist_items.append(MissingInfoChecklistItem(**chk))

        return FormAnalysisResult(
            document_name=document_name,
            form_title=parsed.get("form_title", "Untitled Form Document"),
            issuing_organization=parsed.get("issuing_organization", "Unknown Organization"),
            form_purpose=parsed.get("form_purpose", "Document Analysis"),
            is_demo=False,
            model_used=f"Gemma ({cfg.gemma_model})",
            summary_english=parsed.get("summary_english", "No English summary generated."),
            summary_hinglish=parsed.get("summary_hinglish", "No Hinglish summary generated."),
            deadlines=deadlines,
            required_documents=documents,
            required_fields=fields,
            instructions=instructions,
            missing_info_checklist=checklist_items,
            raw_text_snippet=truncated_text[:800],
            pages_processed=page_count,
            char_count=len(document_text),
            analyzed_at=datetime.now().isoformat()
        )

gemma_service = GemmaInferenceService()
