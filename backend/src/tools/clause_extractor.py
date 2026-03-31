"""MCP Tool: extract_clauses — identifies legal clauses locally using regex."""

import re

CLAUSE_PATTERNS: dict[str, list[str]] = {
    "non_compete": [
        r"non[- ]compete",
        r"covenant not to compete",
        r"shall not.*compete",
        r"competitive activity",
        r"competing business",
    ],
    "arbitration": [
        r"arbitration",
        r"binding arbitration",
        r"arbitrate.*disputes",
        r"\bAAA\b|\bJAMS\b|\bICC\b",
        r"waive.*right.*court",
    ],
    "confidentiality": [
        r"confidential",
        r"non[- ]disclosure",
        r"proprietary information",
        r"trade secret",
        r"nda\b",
    ],
    "ip_assignment": [
        r"intellectual property",
        r"work for hire",
        r"work made for hire",
        r"assigns.*all.*rights",
        r"all inventions",
        r"ownership.*created",
        r"hereby assigns",
    ],
    "termination": [
        r"terminat",
        r"at[- ]will",
        r"notice of termination",
        r"grounds for termination",
        r"immediate termination",
    ],
    "indemnification": [
        r"indemnif",
        r"hold harmless",
        r"defend.*against.*claims",
        r"indemnity",
    ],
    "limitation_of_liability": [
        r"limitation of liability",
        r"in no event.*liable",
        r"maximum liability",
        r"consequential damages",
        r"shall not be liable",
    ],
    "governing_law": [
        r"governed by.*law",
        r"governing law",
        r"laws of the state",
        r"choice of law",
        r"jurisdiction.*courts",
    ],
    "auto_renewal": [
        r"automatic.*renew",
        r"auto[- ]renew",
        r"shall.*renew.*automatically",
        r"evergreen.*clause",
        r"unless.*cancelled.*notice",
    ],
    "force_majeure": [
        r"force majeure",
        r"act of god",
        r"circumstances beyond.*control",
        r"unforeseeable.*event",
    ],
    "non_solicitation": [
        r"non[- ]solicit",
        r"shall not.*solicit",
        r"poaching",
        r"recruit.*employees",
    ],
    "liquidated_damages": [
        r"liquidated damages",
        r"penalty.*breach",
        r"fixed.*amount.*damages",
    ],
}


def extract_clauses(text: str) -> dict[str, list[str]]:
    """
    Runs locally — no external calls.
    Finds legal clauses using regex pattern matching.
    Returns a dict of clause_type -> list of matched excerpts.
    """
    found: dict[str, list[str]] = {}
    text_lower = text.lower()
    sentences = _split_sentences(text)

    for clause_type, patterns in CLAUSE_PATTERNS.items():
        matches = []
        for pattern in patterns:
            for sentence in sentences:
                if re.search(pattern, sentence, re.IGNORECASE) and sentence not in matches:
                    matches.append(sentence[:200])  # cap at 200 chars per match
                    break
        if matches:
            found[clause_type] = matches[:3]  # max 3 examples per clause type

    return found


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+|(?<=\n)\n", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]
