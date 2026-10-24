"""Pydantic data models for FixMyForm AI.

Structured models for form instructions, deadlines, document requirements,
required fields, dual English & Hinglish explanations, and missing-information checklists.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class DeadlineItem(BaseModel):
    title: str = Field(description="Name or description of the deadline")
    date_or_time: str = Field(description="Explicitly stated date, time, or duration")
    category: str = Field(
        default="submission",
        description="Category: 'submission', 'fee_payment', 'correction', 'validity', or 'other'"
    )
    urgency: str = Field(
        default="medium",
        description="Urgency level: 'high', 'medium', or 'low'"
    )
    source_quote: str = Field(
        description="Exact quote from the source document where this deadline is explicitly mentioned"
    )
    source_reference: Optional[str] = Field(
        default=None,
        description="Page number, section header, or clause number in source"
    )

class RequiredDocumentItem(BaseModel):
    name: str = Field(description="Name of the required document")
    acceptable_types: List[str] = Field(
        default_factory=list,
        description="List of acceptable document alternatives (e.g., Passport, Aadhaar, Voter ID)"
    )
    format_and_specs: str = Field(
        description="Format, file size, notarization, self-attestation, or background specifications"
    )
    is_mandatory: bool = Field(
        default=True,
        description="Whether this document is strictly mandatory or optional"
    )
    source_quote: str = Field(
        description="Exact quote from source specifying this requirement"
    )
    source_reference: Optional[str] = Field(
        default=None,
        description="Source section or page reference"
    )

class RequiredFieldItem(BaseModel):
    field_name: str = Field(description="Name or label of the required form field")
    field_type: str = Field(default="text", description="Type of field (text, date, number, dropdown, signature)")
    description: str = Field(description="Description of what should be entered in this field")
    is_mandatory: bool = Field(default=True, description="Whether this field is mandatory")
    validation_rules: Optional[str] = Field(default=None, description="Validation constraints (e.g. 10 digits, alphanumeric, exact match)")
    source_reference: Optional[str] = Field(default=None, description="Source section or page reference")

class InstructionStep(BaseModel):
    step_number: int = Field(description="Sequential step index")
    title: str = Field(description="Clear title of the instruction step")
    english_explanation: str = Field(
        description="Simplified, plain-English explanation without bureaucratic jargon"
    )
    hinglish_explanation: str = Field(
        description="Easy-to-understand explanation in conversational Hindi/Hinglish"
    )
    critical_warning: Optional[str] = Field(
        default=None,
        description="Common mistake, penalty, or critical caveat to avoid"
    )
    source_reference: Optional[str] = Field(
        default=None,
        description="Source clause, section, or page number"
    )

class MissingInfoChecklistItem(BaseModel):
    id: str = Field(description="Unique checklist identifier")
    field_name: str = Field(description="Specific field, detail, or document item the applicant must verify")
    category: str = Field(
        default="personal",
        description="Category: 'personal', 'academic', 'financial', 'declaration', or 'document'"
    )
    why_needed: str = Field(description="Reason this item is necessary for form acceptance")
    english_tip: str = Field(description="Actionable tip in plain English")
    hinglish_tip: str = Field(description="Actionable tip in Hinglish")
    source_reference: Optional[str] = Field(
        default=None,
        description="Source reference in the document"
    )
    is_checked: bool = Field(default=False, description="Applicant completion check state")

class FormAnalysisResult(BaseModel):
    document_name: str = Field(description="Name of the uploaded file or sample form")
    form_title: str = Field(description="Official title of the form")
    issuing_organization: str = Field(description="Government department, university, or issuing entity")
    form_purpose: str = Field(description="Brief explanation of what this form is used for")
    is_demo: bool = Field(default=False, description="Whether this is verified demo data or live AI analysis")
    model_used: str = Field(default="Gemma 4", description="AI model used for analysis")
    summary_english: str = Field(description="Overall executive summary in plain English")
    summary_hinglish: str = Field(description="Overall executive summary in conversational Hindi/Hinglish")
    deadlines: List[DeadlineItem] = Field(default_factory=list)
    required_documents: List[RequiredDocumentItem] = Field(default_factory=list)
    required_fields: List[RequiredFieldItem] = Field(default_factory=list)
    instructions: List[InstructionStep] = Field(default_factory=list)
    missing_info_checklist: List[MissingInfoChecklistItem] = Field(default_factory=list)
    raw_text_snippet: Optional[str] = Field(default=None, description="Preview of extracted source text")
    pages_processed: int = Field(default=1)
    char_count: int = Field(default=0)
    analyzed_at: str = Field(description="ISO timestamp of analysis")

class HealthStatus(BaseModel):
    status: str
    gemma_configured: bool
    gemma_model: str
    endpoint_host: str
    demo_mode_active: bool
    ocr_available: bool

class TestConnectionResult(BaseModel):
    success: bool
    provider: str
    model: str
    endpoint: str
    masked_key: str
    gemma_verified: bool
    latency_ms: float
    message: str
    error_detail: Optional[str] = None
    available_gemma_models: List[str] = Field(default_factory=list)
