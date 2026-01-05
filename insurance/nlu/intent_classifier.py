def detect_intent(text: str) -> str:
    """
    Detects the intent of the user query.
    Returns a predefined intent string.
    """

    text = text.lower().strip()

    if "cover" in text or "coverage" in text:
        return "policy_coverage"

    if "benefit" in text or "advantage" in text:
        return "policy_benefits"

    if "exclude" in text or "not covered" in text:
        return "policy_exclusions"

    if "claim" in text:
        return "claim_process_info"

    if "renew" in text or "renewal" in text:
        return "renewal_date"

    if "valid" in text or "expiry" in text or "expire" in text:
        return "policy_validity"

    if "agent" in text or "human" in text or "representative" in text:
        return "human_agent_request"

    return "unknown"
