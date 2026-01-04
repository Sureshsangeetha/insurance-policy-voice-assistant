import json
from app.db.sqlite import get_conn

def analytics_summary():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as n FROM audit_logs")
    total = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) as n FROM audit_logs WHERE status='Resolved'")
    resolved = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) as n FROM audit_logs WHERE status='Escalated'")
    escalated = cur.fetchone()["n"]

    cur.execute("""
        SELECT intent, COUNT(*) as n
        FROM audit_logs
        GROUP BY intent
        ORDER BY n DESC
        LIMIT 10
    """)
    intents = [{"intent": r["intent"], "count": r["n"]} for r in cur.fetchall()]
    conn.close()

    esc_rate = (escalated / total) if total else 0.0

    return {
        "total_turns": total,
        "resolved_turns": resolved,
        "escalated_turns": escalated,
        "escalation_rate": round(esc_rate, 4),
        "top_intents": intents
    }
