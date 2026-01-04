from __future__ import annotations
from datetime import datetime
import uuid
from app.db.sqlite import get_conn

def _ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_ticket(call_id: str, session_id: str, user_text: str, reason: str) -> dict:
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tickets(ticket_id, call_id, session_id, user_text, reason, status, created_at) VALUES(?,?,?,?,?,?,?)",
        (ticket_id, call_id, session_id, user_text, reason, "OPEN", _ts())
    )
    conn.commit()
    conn.close()
    return {"ticket_id": ticket_id, "status": "OPEN"}

def list_tickets(status: str = "OPEN") -> list[dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets WHERE status=? ORDER BY created_at DESC", (status,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def close_ticket(ticket_id: str) -> dict:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE tickets SET status=?, closed_at=? WHERE ticket_id=?",
                ("CLOSED", _ts(), ticket_id))
    conn.commit()
    conn.close()
    return {"ticket_id": ticket_id, "status": "CLOSED"}
