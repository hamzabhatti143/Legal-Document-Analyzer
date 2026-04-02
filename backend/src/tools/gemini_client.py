"""Gemini client — receives only structured data, never raw document text."""

import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)

LANGUAGE_INSTRUCTION = {
    "en": "Respond in English.",
    "ur": "تمام جوابات اردو زبان میں دیں۔ summary، verdict، risks، obligations، improvements اور keyTerms سب اردو میں لکھیں۔",
}

PROMPT_TEMPLATE = """You are an expert document analyst.

{language_instruction}

Based on the following pre-extracted structured data from a document, provide a comprehensive analysis.
The raw document text has been processed locally — only structured metadata is provided to you.

=== DOCUMENT METADATA ===
Domain: {domain}
Word Count: {word_count}
Parties Identified: {parties}
Key Dates Found: {dates}

=== CLAUSES DETECTED (locally extracted) ===
{clauses_summary}

=== RISK FLAGS (locally scored) ===
{risks_summary}

=== SHORT DOCUMENT EXCERPT (first 800 chars only) ===
{excerpt}

=== INSTRUCTIONS ===
Respond ONLY with a valid JSON object — no markdown, no backticks, no explanation.
Use this exact structure:
{{
  "domain": "{domain}",
  "severity": "low|medium|high|critical",
  "summary": "Plain English summary in 3-5 sentences a non-lawyer can understand",
  "risks": [
    {{ "title": "Risk title", "description": "Plain explanation", "severity": "low|medium|high|critical", "clause": "Relevant excerpt if available" }}
  ],
  "obligations": [
    {{ "party": "Who is obligated", "action": "What they must do", "deadline": "When if specified or null" }}
  ],
  "improvements": [
    {{ "issue": "Problem found", "suggestion": "Recommended fix", "priority": "low|medium|high" }}
  ],
  "keyTerms": ["important term 1", "important term 2"],
  "verdict": "One sentence overall assessment"
}}"""


def analyze_with_gemini(
    domain: str,
    word_count: int,
    parties: list[str],
    dates: list[str],
    clauses_found: dict[str, list[str]],
    risks: list[dict],
    text_excerpt: str,
    language: str = "en",
) -> dict:
    """
    Sends ONLY structured metadata to Gemini — never the full document text.
    The excerpt is limited to 800 characters for context.
    """
    clauses_summary = "\n".join(
        f"- {clause_type.replace('_', ' ').title()}: {len(excerpts)} occurrence(s)"
        for clause_type, excerpts in clauses_found.items()
    ) or "No specific clauses detected"

    risks_summary = "\n".join(
        f"- [{r['severity'].upper()}] {r['title']}: {r['description'][:100]}"
        for r in risks
    ) or "No major risk flags detected"

    prompt = PROMPT_TEMPLATE.format(
        language_instruction=LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["en"]),
        domain=domain,
        word_count=word_count,
        parties=", ".join(parties) if parties else "Not identified",
        dates=", ".join(dates[:5]) if dates else "None found",
        clauses_summary=clauses_summary,
        risks_summary=risks_summary,
        excerpt=text_excerpt[:800],
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    raw = response.text

    json_match = re.search(r"\{[\s\S]*\}", raw)
    if not json_match:
        raise ValueError("Gemini returned an unexpected response format")

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError:
        raise ValueError("Gemini response could not be parsed as valid JSON")
