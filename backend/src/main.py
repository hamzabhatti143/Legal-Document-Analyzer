"""
Document Analyzer — Python MCP Backend
All document processing runs locally. Only structured metadata is sent to the AI.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from tools.document_parser import parse_document
from tools.clause_extractor import extract_clauses
from tools.risk_scorer import score_risks, calculate_overall_severity, extract_parties, extract_dates
from tools.gemini_client import analyze_with_gemini
from models import AnalysisResult, Metadata, Analysis

load_dotenv()

app = FastAPI(title="Document Analyzer Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Document Analyzer Backend"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(
    file: UploadFile = File(...),
    domain: str = Form(default="general"),
):
    # --- Validate ---
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF and DOC/DOCX files are allowed")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size must be under 10MB")

    try:
        # --- MCP Tool 1: Parse document locally ---
        parsed = parse_document(file_bytes, file.content_type)
        text: str = parsed["text"]
        pages: int | None = parsed["pages"]
        word_count: int = parsed["word_count"]

        # --- MCP Tool 2: Extract clauses locally ---
        clauses_found = extract_clauses(text)

        # --- MCP Tool 3: Score risks locally ---
        risks = score_risks(clauses_found)
        overall_severity = calculate_overall_severity(risks)

        # --- MCP Tool 4: Extract parties & dates locally ---
        parties = extract_parties(text)
        dates = extract_dates(text)

        # --- Send ONLY structured data to Gemini (not raw text) ---
        analysis_dict = analyze_with_gemini(
            domain=domain,
            word_count=word_count,
            parties=parties,
            dates=dates,
            clauses_found=clauses_found,
            risks=risks,
            text_excerpt=text[:800],
        )

        return AnalysisResult(
            success=True,
            metadata=Metadata(
                pages=pages,
                wordCount=word_count,
                domain=domain,
                filename=file.filename or "document",
            ),
            analysis=Analysis(**analysis_dict),
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
