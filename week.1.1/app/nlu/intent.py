from __future__ import annotations
import re
from typing import Dict, Tuple, Any

# Hybrid NLU: deterministic patterns (reliable) + confidence heuristics
# (Gemini adapter can be added later without changing orchestration.)

INTENTS = {
    "policy_coverage": [r"\bcover\b", r"coverage", r"included", r"what.*cover"],
    "premium_details": [r"premium", r"price", r"cost", r"amount.*premium"],
    "benefits": [r"benefit", r"cashless", r"network hospital", r"sum insured"],
    "exclusions": [r"exclusion", r"not covered", r"waiting period", r"limit"],
    "claim_process_info": [r"claim", r"reimbursement", r"cashless claim", r"documents.*claim"],
    "renewal": [r"renew", r"renewal", r"expiry", r"valid till", r"policy validity"],
    # Explicit out-of-scope categories
    "payments": [r"pay", r"payment", r"debit", r"credit card", r"upi", r"bank transfer"],
    "claim_initiation": [r"file a claim", r"start claim", r"initiate claim", r"raise claim"],
    "personal_advice": [r"should i", r"recommend", r"best plan", r"which policy"],
}

ENTITY_PATTERNS = {
    "policy_number": r"\b[A-Z]{0,3}\d{6,12}\b",
    "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
}

def extract_entities(text: str) -> Dict[str, Any]:
    entities = {}
    for k, pat in ENTITY_PATTERNS.items():
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            entities[k] = m.group(0)
    return entities

def detect_intent(text: str, session: dict | None = None) -> Tuple[str, float, Dict[str, Any]]:
    t = text.lower()
    entities = extract_entities(text)

    best_intent = "out_of_scope"
    best_score = 0.0

    for intent, patterns in INTENTS.items():
        score = 0.0
        for p in patterns:
            if re.search(p, t):
                score += 1.0
        if score > best_score:
            best_score = score
            best_intent = intent

    # Confidence heuristic
    # More matches => higher confidence; capped to keep compliance conservative.
    if best_score >= 3:
        conf = 0.88
    elif best_score == 2:
        conf = 0.80
    elif best_score == 1:
        conf = 0.70
    else:
        conf = 0.45

    # Multi-turn hint: if user asks "what about exclusions?" after coverage,
    # session can bias to insurance intents (not payments).
    if session and session.get("last_intent") in {"policy_coverage", "benefits"} and best_intent == "out_of_scope":
        # Keep conservative but avoid unnecessary escalation for follow-ups
        conf = max(conf, 0.55)

    return best_intent, conf, entities
