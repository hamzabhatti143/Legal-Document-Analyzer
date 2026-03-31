"""MCP Tool: score_risks — rule-based risk assessment, runs 100% locally."""

import re

RISK_RULES = {
    "non_compete": {
        "severity": "high",
        "title": "Non-Compete Clause",
        "description": "Restricts your ability to work in the same industry or role after leaving. Could limit future employment options.",
        "suggestion": "Negotiate a limited geographic scope, shorter duration (6-12 months max), and narrow role definition.",
    },
    "ip_assignment": {
        "severity": "high",
        "title": "Broad IP Assignment",
        "description": "Company may claim ownership of work you create, potentially including work done outside company time.",
        "suggestion": "Add an exclusion clause for work created on personal time, using personal equipment, unrelated to company business.",
    },
    "arbitration": {
        "severity": "medium",
        "title": "Mandatory Arbitration",
        "description": "Waives your right to sue in court. Disputes resolved in private arbitration which often favors the stronger party.",
        "suggestion": "Request removal of the class-action waiver and ensure the arbitration venue is local to you.",
    },
    "auto_renewal": {
        "severity": "medium",
        "title": "Automatic Renewal",
        "description": "Contract renews automatically unless cancelled with notice. Easy to miss the cancellation window.",
        "suggestion": "Ensure cancellation notice period is reasonable (30 days) and set a calendar reminder.",
    },
    "limitation_of_liability": {
        "severity": "medium",
        "title": "Liability Cap",
        "description": "Limits what you can recover if the other party causes you harm or fails to deliver.",
        "suggestion": "Verify the liability cap is proportional to the contract value and covers direct damages at minimum.",
    },
    "indemnification": {
        "severity": "high",
        "title": "Broad Indemnification",
        "description": "You may be required to cover the other party's legal costs and damages in a wide range of scenarios.",
        "suggestion": "Limit indemnification to claims arising from your own gross negligence or wilful misconduct only.",
    },
    "non_solicitation": {
        "severity": "medium",
        "title": "Non-Solicitation Clause",
        "description": "Prohibits you from recruiting colleagues or contacting clients after leaving.",
        "suggestion": "Limit scope to direct clients you worked with and a 12-month maximum duration.",
    },
    "liquidated_damages": {
        "severity": "high",
        "title": "Liquidated Damages",
        "description": "Fixed financial penalty for breach, which may be disproportionate to actual harm caused.",
        "suggestion": "Ensure the penalty amount is reasonable and proportionate to the contract value.",
    },
}

OVERALL_SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def score_risks(clauses_found: dict[str, list[str]]) -> list[dict]:
    """
    Runs locally — no external calls.
    Maps found clauses to risk entries with severity, description, and suggestions.
    """
    risks = []
    for clause_type, excerpts in clauses_found.items():
        if clause_type in RISK_RULES:
            rule = RISK_RULES[clause_type]
            risks.append({
                "title": rule["title"],
                "description": rule["description"],
                "severity": rule["severity"],
                "clause": excerpts[0] if excerpts else None,
                "suggestion": rule["suggestion"],
            })

    risks.sort(key=lambda r: OVERALL_SEVERITY_ORDER.index(r["severity"]))
    return risks


def calculate_overall_severity(risks: list[dict]) -> str:
    """Returns the highest severity found across all risks."""
    if not risks:
        return "low"
    for level in OVERALL_SEVERITY_ORDER:
        if any(r["severity"] == level for r in risks):
            return level
    return "low"


def extract_parties(text: str) -> list[str]:
    """
    Runs locally — no external calls.
    Extracts party names using common legal document patterns.
    """
    parties = []
    patterns = [
        r"between\s+([A-Z][A-Za-z\s,\.]+?)\s+(?:and|&)\s+([A-Z][A-Za-z\s,\.]+?)(?:\s*[,\(]|\s+hereinafter)",
        r'"([A-Z][A-Za-z\s]+?)"\s+(?:hereinafter|referred to as)',
        r"(?:Company|Employer|Employee|Client|Contractor|Vendor|Buyer|Seller):\s*([A-Z][A-Za-z\s,\.]+?)(?:\n|,)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text[:3000])
        for match in matches:
            if isinstance(match, tuple):
                parties.extend([m.strip() for m in match if m.strip()])
            elif isinstance(match, str) and match.strip():
                parties.append(match.strip())

    return list(dict.fromkeys(parties))[:5]  # deduplicate, max 5


def extract_dates(text: str) -> list[str]:
    """
    Runs locally — no external calls.
    Finds dates, durations, and deadlines in the document.
    """
    patterns = [
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d+\s+(?:days?|months?|years?)\b",
        r"(?:effective|commencing|starting|beginning)\s+(?:on|from)?\s*[A-Za-z0-9,\s]+\d{4}",
        r"(?:expires?|terminates?|ends?)\s+(?:on)?\s*[A-Za-z0-9,\s]+\d{4}",
    ]
    dates = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend([m.strip() for m in matches])

    return list(dict.fromkeys(dates))[:10]
