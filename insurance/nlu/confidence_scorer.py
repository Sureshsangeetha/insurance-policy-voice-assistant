def score_confidence(intent: str) -> float:
    """
    Assigns a confidence score based on intent certainty.
    """

    if intent == "unknown":
        return 0.40

    if intent in ["human_agent_request", "claim_process_info"]:
        return 0.70

    return 0.90
