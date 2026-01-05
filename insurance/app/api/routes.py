from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

import uuid
from llm.gemini_client import generate_response

from nlu.intent_classifier import detect_intent
from nlu.confidence_scorer import score_confidence
from retrieval.grounded_search import fetch_policy_content
from escalation.escalation_manager import check_escalation
from audit_logs.conversation_logger import log_conversation

router = APIRouter()

# ✅ Request body schema
class PolicyQueryRequest(BaseModel):
    user_input: str


@router.post("/query")
def policy_query(request: PolicyQueryRequest):
    user_input = request.user_input

    call_id = f"CALL_{uuid.uuid4()}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1️⃣ Intent detection
    intent = detect_intent(user_input)

    # 2️⃣ Confidence scoring
    confidence = score_confidence(intent)

    # 3️⃣ Escalation check
    escalation = check_escalation(intent, confidence)

    conversation = [
        {
            "timestamp": timestamp,
            "speaker": "user",
            "transcribed_text": user_input
        }
    ]

    # 4️⃣ Escalation handling
    if escalation["escalation_flag"]:
        response = {
            "call_id": call_id,
            "language_detected": "English",
            "conversation": conversation,
            "query_category": intent.replace("_", " ").title(),
            "resolution_status": "Escalated",
            **escalation
        }

        log_conversation(response)
        return response

    # 5️⃣ Policy grounding
    policy_data = fetch_policy_content(intent)

    assistant_response = {
        "timestamp": timestamp,
        "speaker": "assistant",
        "intent": intent,
        "confidence_score": confidence,
        "retrieved_content_reference": policy_data["reference"],
        "voice_response_text": policy_data["answer"]
    }

    conversation.append(assistant_response)

    final_response = {
        "call_id": call_id,
        "language_detected": "English",
        "conversation": conversation,
        "query_category": intent.replace("_", " ").title(),
        "resolution_status": "Resolved",
        "escalation_flag": False,
        "callback_requested": False
    }

    log_conversation(final_response)
    return final_response
