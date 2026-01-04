from app.config import CONFIDENCE_THRESHOLD

# Business rules for escalation (insurance-safe)
# - Low confidence
# - Out of scope: payments, claim initiation, recommendations/advice
# - No grounded content found

def should_escalate(intent: str, confidence: float, grounded: dict) -> tuple[bool, str | None]:
    if confidence < CONFIDENCE_THRESHOLD:
        return True, "Low confidence intent detection"

    if intent in {"payments", "claim_initiation", "personal_advice", "out_of_scope"}:
        return True, "Out of scope request"

    if grounded.get("answer_quality") == "NO_MATCH":
        return True, "Policy content unavailable/unclear"

    return False, None
