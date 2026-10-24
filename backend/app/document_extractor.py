"""Document text extraction and OCR processing module.

Handles:
- Native PDF text extraction (pypdf, pdfplumber fallback)
- Image and scanned PDF OCR processing (pytesseract if installed)
- Scanned document detection and graceful fallbacks
"""

import os
import io
import logging
from typing import Tuple, Dict, Any, Optional
from PIL import Image

logger = logging.getLogger(__name__)

# Check if pytesseract is usable
TESSERACT_AVAILABLE = False
try:
    import pytesseract
    # Check if tesseract binary can be called
    try:
        pytesseract.get_tesseract_version()
        TESSERACT_AVAILABLE = True
    except Exception:
        TESSERACT_AVAILABLE = False
except ImportError:
    TESSERACT_AVAILABLE = False


def is_ocr_available() -> bool:
    """Returns True if Tesseract OCR is installed and available."""
    return TESSERACT_AVAILABLE


def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, int, bool, str]:
    """Extracts text from PDF bytes including text layer and interactive AcroForm fields.
    Returns: (extracted_text, page_count, is_scanned, extraction_method)
    """
    import pypdf

    pdf_stream = io.BytesIO(file_bytes)
    reader = pypdf.PdfReader(pdf_stream)
    page_count = len(reader.pages)
    
    extracted_pages = []
    has_any_text = False
    total_raw_text_length = 0

    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        stripped_text = page_text.strip()
        if stripped_text:
            has_any_text = True
            total_raw_text_length += len(stripped_text)
            extracted_pages.append(f"--- [Page {idx + 1}] ---\n{stripped_text}\n")
        else:
            extracted_pages.append(f"--- [Page {idx + 1}] ---\n[No direct text layer found on this page]\n")

    # Extract interactive form fields if present (e.g. government & official fillable PDFs)
    form_fields_found = []
    try:
        fields = reader.get_fields()
        if fields:
            for field_name, field_info in fields.items():
                if isinstance(field_info, dict):
                    val = field_info.get('/V') or field_info.get('/TU') or ""
                    form_fields_found.append(f"Field: {field_name} (Value/Hint: {val})")
                else:
                    form_fields_found.append(f"Field: {field_name}")
    except Exception as e:
        logger.debug(f"AcroForm field extraction skipped: {e}")

    if form_fields_found:
        extracted_pages.append("\n--- [Interactive Form Fields Extracted] ---")
        extracted_pages.extend(form_fields_found[:150])  # limit to 150 fields to prevent overflow
        has_any_text = True

    is_scanned = (total_raw_text_length < 60 and not form_fields_found) or (not has_any_text)

    # If no readable text or form fields were found at all
    if not has_any_text:
        full_text = ""
    else:
        full_text = "\n".join(extracted_pages)

    # If scanned and OCR is available, attempt OCR on embedded page images
    if is_scanned and TESSERACT_AVAILABLE:
        ocr_pages = []
        for idx, page in enumerate(reader.pages):
            page_ocr_text = ""
            for img_obj in page.images:
                try:
                    img = Image.open(io.BytesIO(img_obj.data))
                    ocr_result = pytesseract.image_to_string(img)
                    if ocr_result.strip():
                        page_ocr_text += ocr_result.strip() + "\n"
                except Exception as err:
                    logger.warning(f"Failed to OCR image on page {idx + 1}: {err}")
            
            if page_ocr_text.strip():
                ocr_pages.append(f"--- [Page {idx + 1} (OCR Extracted)] ---\n{page_ocr_text.strip()}\n")

        if ocr_pages:
            return "\n".join(ocr_pages), page_count, True, "tesseract_pdf_ocr"

    method = "pypdf_text"
    if form_fields_found and not total_raw_text_length:
        method = "pypdf_form_fields"
    elif is_scanned:
        method = "scanned_pdf_raw"

    return full_text, page_count, is_scanned, method


def extract_text_from_image(file_bytes: bytes) -> Tuple[str, int, bool, str]:
    """Extracts text from image bytes using OCR if available."""
    try:
        img = Image.open(io.BytesIO(file_bytes))
        width, height = img.size
    except Exception as e:
        raise ValueError(f"Invalid image format: {e}")

    if TESSERACT_AVAILABLE:
        try:
            text = pytesseract.image_to_string(img)
            return text.strip(), 1, False, "tesseract_image_ocr"
        except Exception as e:
            logger.error(f"Tesseract OCR error: {e}")

    # Fallback when OCR is not locally configured
    return (
        f"[Image uploaded: {width}x{height}px. Tesseract OCR is not installed on this system. "
        f"For highest accuracy, upload a PDF form or test using the pre-analyzed demo samples.]",
        1,
        True,
        "image_metadata_only"
    )


def extract_document_content(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Unified document extraction handler for PDFs and Images."""
    ext = os.path.splitext(filename.lower())[1]

    if ext == ".pdf":
        text, page_count, is_scanned, method = extract_text_from_pdf(file_bytes)
    elif ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"]:
        text, page_count, is_scanned, method = extract_text_from_image(file_bytes)
    elif ext in [".txt", ".md"]:
        text = file_bytes.decode("utf-8", errors="replace")
        page_count = 1
        is_scanned = False
        method = "plain_text"
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Please upload a PDF, PNG, JPG, or TXT document.")

    return {
        "text": text,
        "page_count": page_count,
        "char_count": len(text),
        "is_scanned": is_scanned,
        "method": method,
        "filename": filename
    }
