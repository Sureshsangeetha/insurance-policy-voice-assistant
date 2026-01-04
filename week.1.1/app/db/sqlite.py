import sqlite3
from pathlib import Path

DB_PATH = Path("data/db.sqlite3")

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        call_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        user_text TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        closed_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id TEXT,
        session_id TEXT,
        user_text TEXT,
        intent TEXT,
        confidence REAL,
        status TEXT,
        refs TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()
