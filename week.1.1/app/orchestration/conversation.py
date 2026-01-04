from __future__ import annotations

from datetime import datetime
import uuid

from app.nlu.intent import detect_intent
from app.rag.retriever import retrieve_grounded_answer
from app.compliance.guardrails import apply_guardrails
from app.orchestration.escalation import should_escalate
from app.agent_queue.service import create_ticket
from app.analytics.logger import log_turn
from app.memory.session_store import get_session, update_session

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_turn(session_id: str, user_text: str, language_hint: str = "English") -> dict:
    call_id = session_id  # for voice calls, session_id can be CallSid
    session = get_session(session_id)

    # 1) NLU
    intent, confidence, entities = detect_intent(user_text, session=session)

    # 2) Retrieval (grounded)
    grounded = retrieve_grounded_answer(user_text=user_text, intent=intent, entities=entities)

    # 3) Compliance guardrails (mask PII and block advice)
    safe_user_text = apply_guardrails.mask_pii(user_text)
    safe_answer = apply_guardrails.enforce_no_advice(grounded["answer"])

    # 4) Escalation decision
    escalate, reason = should_escalate(intent=intent, confidence=confidence, grounded=grounded)

    # 5) Build response JSON (your required format)
    t = now_ts()
    if escalate:
        ticket = create_ticket(
            call_id=call_id,
            session_id=session_id,
            user_text=safe_user_text,
            reason=reason or "Escalation triggered"
        )
        resp = {
            "call_id": call_id,
            "language_detected": language_hint,
            "conversation": [
                {"timestamp": t, "speaker": "user", "transcribed_text": safe_user_text},
                {
                    "timestamp": t,
                    "speaker": "assistant",
                    "intent": intent,
                    "confidence_score": confidence,
                    "retrieved_content_reference": grounded.get("references", []),
                    "voice_response_text": (
                        "I’m not fully confident I can answer that correctly. "
                        "I’m escalating this to a human agent and arranging a callback."
                    )
                }
            ],
            "query_category": grounded.get("query_category", intent),
            "resolution_status": "Escalated",
            "escalation_flag": True,
            "escalation_reason": reason,
            "callback_requested": True,
            "ticket_id": ticket["ticket_id"]
        }
        log_turn(call_id, session_id, safe_user_text, intent, confidence, "Escalated", grounded.get("references", []))
        update_session(session_id, user_text=safe_user_text, assistant_text=resp["conversation"][-1]["voice_response_text"])
        return resp

    resp = {
        "call_id": call_id,
        "language_detected": language_hint,
        "conversation": [
            {"timestamp": t, "speaker": "user", "transcribed_text": safe_user_text},
            {
                "timestamp": t,
                "speaker": "assistant",
                "intent": intent,
                "confidence_score": confidence,
                "retrieved_content_reference": grounded.get("references", []),
                "voice_response_text": safe_answer
            }
        ],
        "query_category": grounded.get("query_category", intent),
        "resolution_status": "Resolved",
        "escalation_flag": False,
        "callback_requested": False
    }

    log_turn(call_id, session_id, safe_user_text, intent, confidence, "Resolved", grounded.get("references", []))
    update_session(session_id, user_text=safe_user_text, assistant_text=safe_answer)
    return resp
