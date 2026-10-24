# FixMyForm AI 📄✨

**Intelligent Document & Form Compliance Engine powered exclusively by Google Gemma 4.**

FixMyForm AI solves one of the most frustrating real-world problems: government, university admission, scholarship, employment, and visa forms are filled with impenetrable bureaucracy, obscure document rules, and hidden deadlines.

By leveraging **Gemma 4** as the sole AI model, FixMyForm AI extracts explicit instructions, identifies deadlines stated in the source without hallucinations, provides bilingual explanations in plain English and Hindi/Hinglish, and produces an interactive verification checklist with exact source citations.

---

## 🌟 Key Features

- **Gemma 4 Exclusive Document Intelligence**: Powered exclusively by Google's open foundation model Gemma 4 for high-precision, factual administrative document analysis.
- **Strict Anti-Hallucination Deadlines**: Extracts *only* deadlines explicitly stated in the source text, accompanied by exact source quotes and section/clause citations.
- **Required Documents & Specifications**: Identifies mandatory vs. supporting documents, acceptable alternative proofs, photo specifications, and self-attestation rules.
- **Bilingual Dual-Language Explanations**: Jargon-free explanations in **Simple English** and natural conversational **Hindi/Hinglish** (e.g., *"Aadhaar card par aur 10th marksheet par naam bilkul same hona chahiye..."*).
- **Interactive Pre-Submission Checklist**: Real-time actionable checklist with completion tracking, categorizing personal, financial, academic, and document fields before form submission.
- **Clearly Labelled Demo Mode (Zero Fake AI)**: When the Gemma API key is not configured, FixMyForm AI operates in an explicitly badged Demo Mode offering authentic pre-analyzed sample forms rather than faking AI responses.
- **Multi-Format Ingestion & OCR**: Supports text-searchable PDFs, plain text, and scanned documents/images with automatic OCR fallback.

---

## 🏛️ Architectural Constraints & Security

FixMyForm AI is built in accordance with strict architectural guardrails:

1. **Gemma 4 Exclusivity**: Gemma 4 is the **only** AI model integrated. All non-Gemma models and proprietary model APIs (e.g., OpenAI, Anthropic) are rejected.
2. **Forbidden Providers**: DigitalOcean is explicitly **disallowed** and rejected at runtime by backend constraint validators.
3. **Documented Open Endpoints**: Compatible with standard, documented inference endpoints for Gemma:
   - **Groq Cloud** (`api.groq.com/openai/v1`)
   - **OpenRouter** (`openrouter.ai/api/v1`)
   - **Hugging Face Inference API / Endpoints** (`api-inference.huggingface.co`)
   - **Self-hosted Ollama** (`http://localhost:11434/v1`)
   - **Self-hosted vLLM** (`http://localhost:8000/v1`)
4. **Environment Variable Security**: All API keys and endpoints reside strictly in the backend `.env` configuration and are never exposed to the frontend client.
5. **No Fake AI Responses**: If a user uploads custom files when the Gemma API is not configured, the system strictly returns an informative notice and prompts the user to either explore verified Demo Mode samples or configure `GEMMA_API_KEY`.

---

## 📋 Pre-Analyzed Demo Forms

When running in Demo Mode, users can explore verified analyses of complex real-world forms:

| Sample Form | Issuing Authority | Key Highlights |
| :--- | :--- | :--- |
| **Form No. 1: Indian Passport Application** | Passport Seva, Ministry of External Affairs (MEA) | Tatkaal timelines, Annexure E standard affidavit, strict 1-year address continuity, white-background photo specs. |
| **National Merit Scholarship (Form NSP-2026)** | Ministry of Education, Govt of India | Strict 30-Nov deadline, Tehsildar income certificate (< Rs 8 Lakh), NPCI Aadhaar bank mapping mandate. |
| **Form 12BB: Employee Tax & HRA Declaration** | Income Tax Department & Corporate Payroll | 15-Jan cutoff, compulsory Landlord PAN (> Rs 1 Lakh rent), Section 80C & 80D deduction proofs. |

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+** (Python 3.13 supported)
- **Node.js 20+** and **npm**
- *(Optional)* Tesseract OCR binary if analyzing scanned image documents

---

### 1. Backend Setup (FastAPI)

1. Open a terminal in the project root and navigate to `backend/`:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Configure your `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to supply your Gemma 4 credentials:
   ```ini
   # Leave blank to operate in verified Demo Mode:
   GEMMA_API_KEY=your_gemma_api_key_here

   # Compatible Gemma inference endpoint:
   GEMMA_API_ENDPOINT=https://api.groq.com/openai/v1/chat/completions

   # Gemma model identifier:
   GEMMA_MODEL=google/gemma-4
   ```

4. Run the backend server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The backend API will be live at `http://127.0.0.1:8000`. You can view the OpenAPI interactive documentation at `http://127.0.0.1:8000/docs`.

---

### 2. Frontend Setup (React + Tailwind CSS)

1. In a separate terminal, navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```

3. Launch the development server:
   ```bash
   npm run dev -- --host 127.0.0.1 --port 5173
   ```
   Open your browser at `http://127.0.0.1:5173`.

---

## 🧪 Testing

### Backend Unit & Integration Tests (pytest)
To execute the automated backend test suite verifying API status, Gemma constraints, DigitalOcean rejection, text extraction, and Demo Mode:
```powershell
$env:PYTHONPATH = ".\backend"
.\backend\venv\Scripts\python.exe -m pytest .\backend\tests -v
```

### Frontend Production Build
To verify frontend compilation and asset bundling:
```bash
cd frontend
npm run build
```

---

## 📁 Repository Structure

```
FixmyForm-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py              # Settings, DigitalOcean rejection & Gemma-only enforcement
│   │   ├── models.py              # Pydantic schemas (deadlines, checklist, bilingual instructions)
│   │   ├── document_extractor.py  # PDF text extraction & OCR fallback
│   │   ├── gemma_service.py       # Gemma 4 inference service & precision prompt engineering
│   │   ├── sample_forms.py        # Verified authentic sample forms for Demo Mode
│   │   └── main.py                # FastAPI routes (/status, /samples, /analyze, /extract-preview)
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py            # 9 automated tests for constraints, demo mode, and endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Backend environment template
│   └── .env                       # Backend active environment
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx             # Header with Gemma 4 credit, status badge, language toggle
│   │   │   ├── DemoModeBanner.jsx     # Explicit demo banner with sample form selectors
│   │   │   ├── HeroBanner.jsx         # Punchy value proposition & feature highlights
│   │   │   ├── DocumentUpload.jsx     # Drag-and-drop file upload & real-time text preview drawer
│   │   │   ├── AnalysisDashboard.jsx  # Main results container with print/save support
│   │   │   ├── DeadlinesSection.jsx   # Source-grounded deadlines with urgency flags
│   │   │   ├── DocumentsSection.jsx   # Required proofs, specifications & acceptable types
│   │   │   ├── InstructionsSection.jsx# Step-by-step guidance in English & Hinglish
│   │   │   ├── ChecklistSection.jsx   # Interactive verification checklist with progress bar
│   │   │   ├── RawSourceModal.jsx     # Extracted text inspector for grounding verification
│   │   │   └── ConfigModal.jsx        # Gemma 4 setup guide & architectural constraints
│   │   ├── App.jsx                    # Root application state & orchestrator
│   │   ├── index.css                  # Tailwind CSS v4, dark theme & glassmorphism
│   │   └── main.jsx
│   ├── vite.config.js                 # Vite + Tailwind plugin & backend API proxy
│   └── package.json
│
└── README.md
```

---

## 🎖️ Model Credits

**Google Gemma 4**: Developed by Google DeepMind and the open-source Gemma community. FixMyForm AI is built exclusively to showcase the document reasoning, legal/administrative compliance, and multilingual capabilities of Gemma 4.
