from pydantic import BaseModel
from typing import Optional, Literal

Severity = Literal["low", "medium", "high", "critical"]
Priority = Literal["low", "medium", "high"]
Domain = Literal["contract", "employment", "real_estate", "ip", "corporate", "privacy", "general"]


class Risk(BaseModel):
    title: str
    description: str
    severity: Severity
    clause: Optional[str] = None


class Obligation(BaseModel):
    party: str
    action: str
    deadline: Optional[str] = None


class Improvement(BaseModel):
    issue: str
    suggestion: str
    priority: Priority


class Analysis(BaseModel):
    domain: Domain
    severity: Severity
    summary: str
    risks: list[Risk]
    obligations: list[Obligation]
    improvements: list[Improvement]
    keyTerms: list[str]
    verdict: str


class Metadata(BaseModel):
    pages: Optional[int]
    wordCount: int
    domain: str
    filename: str


class AnalysisResult(BaseModel):
    success: bool
    metadata: Metadata
    analysis: Analysis


class ExtractedData(BaseModel):
    text_excerpt: str
    word_count: int
    clauses_found: dict[str, list[str]]
    parties: list[str]
    dates: list[str]
    red_flags: list[dict]
    domain: str
