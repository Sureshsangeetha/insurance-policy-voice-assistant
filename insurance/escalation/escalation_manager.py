CONFIDENCE_THRESHOLD = 0.75

OUT_OF_SCOPE_INTENTS = [
    "human_agent_request"
]

def check_escalation(intent: str, confidence: float) -> dict:
    """
    Determines whether the query should be escalated to a human agent.
    """

    # Low confidence → escalate
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "escalation_flag": True,
            "callback_requested": True,
            "escalation_reason": "Low confidence in intent detection"
        }

    # Explicit human agent request
    if intent in OUT_OF_SCOPE_INTENTS:
        return {
            "escalation_flag": True,
            "callback_requested": True,
            "escalation_reason": "User requested human assistance"
        }

    return {
        "escalation_flag": False,
        "callback_requested": False
    }
