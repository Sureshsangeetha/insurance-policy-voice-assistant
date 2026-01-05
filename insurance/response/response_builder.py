from datetime import datetime

def build_response(
    call_id: str,
    intent: str,
    confidence: float,
    policy_data: dict
) -> dict:
    """
    Builds a structured, compliant assistant response.
    This layer does NOT add new information.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": timestamp,
        "speaker": "assistant",
        "intent": intent,
        "confidence_score": confidence,
        "retrieved_content_reference": policy_data.get("reference", []),
        "voice_response_text": policy_data.get(
            "answer",
            "This information is not available at the moment."
        )
    }
