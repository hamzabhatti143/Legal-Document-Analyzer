"""MCP Tool: parse_document — extracts text locally, nothing sent externally."""

import io
from typing import Optional


def parse_document(file_bytes: bytes, mime_type: str) -> dict:
    """
    Parses PDF or DOCX files locally.
    Returns extracted text, page count, and word count.
    No data leaves the server.
    """
    if mime_type == "application/pdf":
        return _parse_pdf(file_bytes)
    elif mime_type in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ):
        return _parse_docx(file_bytes)
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOC/DOCX.")


def _parse_pdf(file_bytes: bytes) -> dict:
    import pdfplumber

    text_parts = []
    pages = 0

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages = len(pdf.pages)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    text = "\n".join(text_parts)
    return {
        "text": text,
        "pages": pages,
        "word_count": len(text.split()),
    }


def _parse_docx(file_bytes: bytes) -> dict:
    from docx import Document

    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(paragraphs)
    return {
        "text": text,
        "pages": None,
        "word_count": len(text.split()),
    }
