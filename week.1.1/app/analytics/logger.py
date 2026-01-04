from datetime import datetime
import json
from app.db.sqlite import get_conn

def _ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_turn(call_id: str, session_id: str, user_text: str, intent: str, confidence: float, status: str, refs: list[str]):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audit_logs(call_id, session_id, user_text, intent, confidence, status, refs, timestamp) VALUES(?,?,?,?,?,?,?,?)",
        (call_id, session_id, user_text, intent, float(confidence), status, json.dumps(refs), _ts())
    )
    conn.commit()
    conn.close()
