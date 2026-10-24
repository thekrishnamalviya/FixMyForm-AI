"""FastAPI application entrypoint for FixMyForm AI.

Integrates:
- Gemma exclusively for document understanding and analysis
- Live model connection test endpoint (/api/test-connection)
- Strict prohibition of DigitalOcean and non-Gemma proprietary models
- Clearly labeled Demo Mode without faking AI responses
- Multi-format document extraction (PDF, images, text)
- Bilingual instructions (English & Hinglish)
- Explicit deadlines and required document extractors
"""

import os
import logging
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.models import FormAnalysisResult, HealthStatus, TestConnectionResult
from app.document_extractor import extract_document_content, is_ocr_available
from app.sample_forms import (
    get_sample_form_by_id,
    list_sample_forms_metadata,
    SAMPLE_FORMS_COLLECTION
)
from app.gemma_service import (
    gemma_service,
    GemmaNotConfiguredError,
    GemmaConstraintViolationError,
    GemmaAuthenticationError,
    GemmaModelUnavailableError
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fixmyform-ai")

app = FastAPI(
    title="FixMyForm AI — Document Understanding with Gemma",
    description="Smart form parsing, deadline extraction, bilingual English/Hinglish explanations, and missing-info checklists powered exclusively by Gemma.",
    version="1.1.0"
)

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/status", response_model=HealthStatus)
def get_system_status():
    """Returns application status, Gemma configuration state, and OCR availability."""
    settings.reload()
    endpoint_host = "not-configured"
    if settings.gemma_api_endpoint:
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(settings.gemma_api_endpoint)
            endpoint_host = parsed_url.netloc or "configured-endpoint"
        except Exception:
            endpoint_host = "custom-endpoint"

    is_configured = settings.is_gemma_configured()

    return HealthStatus(
        status="operational",
        gemma_configured=is_configured,
        gemma_model=settings.gemma_model,
        endpoint_host=endpoint_host,
        demo_mode_active=not is_configured,
        ocr_available=is_ocr_available()
    )


@app.post("/api/test-connection", response_model=TestConnectionResult)
async def test_connection():
    """Tests live connection to the configured model provider.

    Strictly verifies whether Gemma is available through the configured provider.
    Never claims the model works until a real API request succeeds.
    """
    return await gemma_service.test_model_connection()


@app.get("/api/test-connection", response_model=TestConnectionResult)
async def test_connection_get():
    """GET alias for browser/curl testing of model connection."""
    return await gemma_service.test_model_connection()


@app.get("/api/samples")
def get_demo_samples():
    """Lists verified authentic sample forms available in Demo Mode."""
    return {
        "demo_mode": True,
        "message": "Pre-analyzed forms for demonstration when Gemma API is not configured.",
        "samples": list_sample_forms_metadata()
    }


@app.get("/api/samples/{sample_id}", response_model=FormAnalysisResult)
def get_demo_sample_analysis(sample_id: str):
    """Returns verified authentic pre-analyzed analysis for the selected demo form."""
    if sample_id not in SAMPLE_FORMS_COLLECTION:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample '{sample_id}' not found. Available samples: {list(SAMPLE_FORMS_COLLECTION.keys())}"
        )
    return get_sample_form_by_id(sample_id)


@app.post("/api/extract-preview")
async def extract_preview(file: UploadFile = File(...)):
    """Extracts raw text, page count, and scanned detection for document preview."""
    try:
        content = await file.read()
        if len(content) > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {settings.max_upload_size_mb} MB"
            )
        extracted = extract_document_content(content, file.filename or "uploaded_document")
        return {
            "success": True,
            "filename": extracted["filename"],
            "page_count": extracted["page_count"],
            "char_count": extracted["char_count"],
            "is_scanned": extracted["is_scanned"],
            "extraction_method": extracted["method"],
            "preview_snippet": extracted["text"][:1500]
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error during document extraction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {e}"
        )


@app.post("/api/analyze", response_model=FormAnalysisResult)
async def analyze_form_document(
    file: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None),
    force_demo_sample: Optional[str] = Form(None)
):
    """Analyzes a form document using Gemma.

    If a sample is explicitly requested via force_demo_sample, returns verified demo data.
    If custom document is uploaded:
      - If Gemma API is configured: calls Gemma for live document intelligence.
      - If Gemma API is NOT configured: strictly returns 400 with Demo Mode prompt (NO FAKE AI).
    """
    settings.reload()

    # 1. Handle explicit demo sample request
    if force_demo_sample:
        return get_sample_form_by_id(force_demo_sample)

    # 2. Check if Gemma API is configured
    if not settings.is_gemma_configured():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_code": "GEMMA_NOT_CONFIGURED",
                "message": (
                    "Gemma API key is not configured in backend environment variables. "
                    "FixMyForm AI strictly refuses to fake AI responses. "
                    "To analyze custom documents, add GEMMA_API_KEY or BACKBOARD_API_KEY to your backend .env file. "
                    "Alternatively, explore verified pre-analyzed forms in Demo Mode."
                ),
                "demo_mode_active": True,
                "suggested_samples": [
                    {"id": "passport", "title": "Indian Passport Application Form No. 1"},
                    {"id": "scholarship", "title": "National Merit Scholarship Application"},
                    {"id": "tax_12bb", "title": "Form 12BB Tax Declaration & Proofs"}
                ]
            }
        )

    # 3. Extract document content
    document_text = ""
    document_name = "Pasted Form Text"
    page_count = 1

    if file and file.filename:
        content = await file.read()
        if len(content) > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {settings.max_upload_size_mb} MB"
            )
        extracted = extract_document_content(content, file.filename)
        document_text = extracted["text"]
        document_name = file.filename
        page_count = extracted["page_count"]
    elif raw_text and raw_text.strip():
        document_text = raw_text.strip()
        document_name = "Text Input"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a document file (PDF/Image) or text content to analyze."
        )

    if not document_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract readable text from document. If this is a scanned document, ensure OCR is configured."
        )

    # 4. Invoke Gemma
    try:
        analysis = await gemma_service.analyze_document_with_gemma(
            document_text=document_text,
            document_name=document_name,
            page_count=page_count
        )
        return analysis
    except GemmaAuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except GemmaModelUnavailableError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except GemmaConstraintViolationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except GemmaNotConfiguredError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Gemma inference failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemma document analysis failed: {e}"
        )
