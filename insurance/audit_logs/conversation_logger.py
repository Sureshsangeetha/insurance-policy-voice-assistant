import json
import os
from datetime import datetime

# Directory where logs will be stored
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "conversations.json")


def log_conversation(conversation_data: dict) -> None:
    """
    Safely logs conversation data in JSON-lines format.

    - Append-only (audit safe)
    - No PII masking here (assumed done earlier)
    - Never raises exception (logging must not crash the app)
    """

    try:
        # Ensure log directory exists
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        log_entry = {
            "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conversation": conversation_data
        }

        # Append log entry as JSON line
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    except Exception:
        # IMPORTANT:
        # Logging failures should NEVER break the API
        pass
