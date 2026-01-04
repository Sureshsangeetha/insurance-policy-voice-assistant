from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter()

# -----------------------------
# CHAT (ChatGPT-style UI)
# -----------------------------
@router.post("/api/chat")
def chat(payload: dict):
    session_id = payload.get("session_id", str(uuid.uuid4()))
    text = payload.get("transcribed_text", "")

    return {
        "call_id": f"CALL-{session_id}",
        "language_detected": "English",
        "conversation": [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "speaker": "user",
                "transcribed_text": text,
            },
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "speaker": "assistant",
                "intent": "policy_coverage",
                "confidence_score": 0.85,
                "retrieved_content_reference": [
                    "PolicyDoc_HealthSecure_v3_Section_2.1"
                ],
                "voice_response_text": (
                    "Your policy covers hospitalization, pre and post "
                    "hospitalization expenses as per the policy document."
                ),
            },
        ],
        "query_category": "policy_coverage",
        "resolution_status": "Resolved",
        "escalation_flag": False,
        "callback_requested": False,
    }


# -----------------------------
# VOICE INBOUND (Telephony)
# -----------------------------
@router.post("/api/voice/inbound")
def voice_inbound(payload: dict):
    return {
        "message": "Voice call received",
        "payload": payload,
        "next_step": "Intent classification → Knowledge retrieval",
    }


# -----------------------------
# HUMAN AGENT QUEUE
# -----------------------------
@router.get("/agent/queue")
def agent_queue():
    return {
        "queue_size": 1,
        "agents_available": 2,
        "waiting_calls": [
            {
                "call_id": "CALL-ADV-001",
                "reason": "Low confidence intent detection",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ],
    }
