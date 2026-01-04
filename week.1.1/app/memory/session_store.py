from __future__ import annotations

# In-memory session memory (demo). Swap with Redis for production.
_SESSIONS: dict[str, dict] = {}

def get_session(session_id: str) -> dict:
    return _SESSIONS.get(session_id, {"turns": [], "last_intent": None})

def update_session(session_id: str, user_text: str, assistant_text: str):
    s = _SESSIONS.setdefault(session_id, {"turns": [], "last_intent": None})
    s["turns"].append({"user": user_text, "assistant": assistant_text})
    # keep last 10 turns
    s["turns"] = s["turns"][-10:]
