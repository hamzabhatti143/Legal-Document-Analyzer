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
    "en": "Respond in English. All text values in the JSON must be in English.",
    "ur": (
        "IMPORTANT: You MUST write ALL text values in Urdu (اردو) script. "
        "This includes: summary, verdict, every risk title and description and clause, "
        "every obligation party/action/deadline, every improvement issue and suggestion, "
        "and every keyTerm. Do NOT use English for any of these values. "
        "Only the JSON keys and severity/priority enum values (low/medium/high/critical) stay in English."
    ),
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
{language_instruction}
Use this exact structure:
{{
  "domain": "{domain}",
  "severity": "low|medium|high|critical",
  "summary": "3-5 sentence summary a non-lawyer can understand (in the required language)",
  "risks": [
    {{ "title": "Risk title (in the required language)", "description": "Plain explanation (in the required language)", "severity": "low|medium|high|critical", "clause": "Relevant excerpt if available (in the required language)" }}
  ],
  "obligations": [
    {{ "party": "Who is obligated (in the required language)", "action": "What they must do (in the required language)", "deadline": "When if specified or null" }}
  ],
  "improvements": [
    {{ "issue": "Problem found (in the required language)", "suggestion": "Recommended fix (in the required language)", "priority": "low|medium|high" }}
  ],
  "keyTerms": ["important term 1 (in the required language)", "important term 2 (in the required language)"],
  "verdict": "One sentence overall assessment (in the required language)"
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
