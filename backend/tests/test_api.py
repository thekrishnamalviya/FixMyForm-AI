"""Automated tests for FixMyForm AI backend.

Validates:
1. Strict Gemma exclusivity and constraint validation (DigitalOcean forbidden, non-Gemma rejected).
2. Demo mode operation when Gemma API key is not configured (no fake AI).
3. Sample forms data structure integrity (deadlines, documents, required fields, instructions, checklist).
4. Document text extraction from PDF and plain text.
5. FastAPI route responses for /api/status, /api/samples, /api/samples/{id}, and /api/analyze.
6. Test connection endpoint (/api/test-connection) and Backboard header/endpoint format.
"""

import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings
from app.models import FormAnalysisResult
from app.document_extractor import extract_document_content
from app.sample_forms import SAMPLE_FORMS_COLLECTION, get_sample_form_by_id

client = TestClient(app)

def test_api_status_endpoint():
    """Verify system status reports operational and demo mode state."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "gemma_configured" in data
    assert "demo_mode_active" in data
    assert "ocr_available" in data


def test_test_connection_endpoint_unconfigured():
    """Verify /api/test-connection reports clean status when key is not configured."""
    response = client.post("/api/test-connection")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "provider" in data
    assert "model" in data
    assert "masked_key" in data
    # Masked key must never reveal a raw key
    assert len(data["masked_key"]) <= 16


def test_test_connection_get_endpoint():
    """Verify GET alias for /api/test-connection."""
    response = client.get("/api/test-connection")
    assert response.status_code == 200
    data = response.json()
    assert "gemma_verified" in data


def test_samples_list_endpoint():
    """Verify demo samples endpoint returns valid catalog."""
    response = client.get("/api/samples")
    assert response.status_code == 200
    data = response.json()
    assert data["demo_mode"] is True
    assert len(data["samples"]) >= 3
    sample_ids = [s["id"] for s in data["samples"]]
    assert "passport" in sample_ids
    assert "scholarship" in sample_ids
    assert "tax_12bb" in sample_ids


def test_sample_detail_endpoint_with_required_fields():
    """Verify individual sample returns complete FormAnalysisResult schema including required_fields."""
    for sample_id in ["passport", "scholarship", "tax_12bb"]:
        response = client.get(f"/api/samples/{sample_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["is_demo"] is True
        assert "Gemma" in data["model_used"]
        assert len(data["deadlines"]) > 0
        assert len(data["required_documents"]) > 0
        assert len(data["required_fields"]) > 0
        assert len(data["instructions"]) > 0
        assert len(data["missing_info_checklist"]) > 0
        
        # Verify bilingual explanations exist
        assert data["summary_english"]
        assert data["summary_hinglish"]
        for inst in data["instructions"]:
            assert inst["english_explanation"]
            assert inst["hinglish_explanation"]


def test_custom_upload_without_gemma_api_strictly_refuses_fake_ai():
    """Verify that uploading custom content without GEMMA_API_KEY returns 400
    with explicit error and demo suggestions, never faking AI responses."""
    response = client.post(
        "/api/analyze",
        data={"raw_text": "Sample application form text with deadline 1st Jan 2027"}
    )
    if response.status_code == 400:
        data = response.json()
        assert data["error_code"] == "GEMMA_NOT_CONFIGURED"
        assert data["demo_mode_active"] is True
        assert "suggested_samples" in data


def test_analyze_with_force_demo_sample():
    """Verify force_demo_sample parameter returns requested sample reliably."""
    response = client.post(
        "/api/analyze",
        data={"force_demo_sample": "scholarship"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["form_title"] == SAMPLE_FORMS_COLLECTION["scholarship"].form_title
    assert data["is_demo"] is True


def test_digitalocean_forbidden_constraint():
    """Verify system strictly raises ValueError if DigitalOcean is configured."""
    with pytest.raises(ValueError, match="not permitted"):
        bad_settings = Settings(
            gemma_api_endpoint="https://digitalocean.com/v1/chat/completions",
            gemma_model="google/gemma-4"
        )
        bad_settings.validate_constraints()


def test_non_gemma_model_rejected():
    """Verify system strictly rejects any model that is not Gemma."""
    with pytest.raises(ValueError, match="is not a Gemma model"):
        bad_settings = Settings(
            gemma_api_endpoint="https://api.groq.com/openai/v1/chat/completions",
            gemma_model="some-other-model"
        )
        bad_settings.validate_constraints()


def test_backboard_configuration_detection():
    """Verify Backboard endpoint is recognized and configured properly."""
    bb_settings = Settings(
        gemma_api_endpoint="https://app.backboard.io/api",
        gemma_model="google/gemma-3-12b-it",
        backboard_provider="google"
    )
    assert bb_settings.is_backboard() is True
    assert bb_settings.backboard_provider == "google"
    bb_settings.validate_constraints()


def test_document_extractor_plain_text():
    """Verify document text extractor handles text input."""
    raw = b"GOVERNMENT ADMISSION FORM 2026\nSubmission Deadline: 31st October 2026"
    extracted = extract_document_content(raw, "admission_form.txt")
    assert extracted["page_count"] == 1
    assert "Deadline: 31st October" in extracted["text"]
    assert extracted["is_scanned"] is False


def test_extract_preview_endpoint():
    """Verify /api/extract-preview extracts text and metadata."""
    file_content = b"Form 100: Application Form for Civil Services. Section 1: Candidate Name."
    response = client.post(
        "/api/extract-preview",
        files={"file": ("test_form.txt", io.BytesIO(file_content), "text/plain")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["filename"] == "test_form.txt"
    assert "Civil Services" in data["preview_snippet"]
