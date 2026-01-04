import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import router as api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Insurance Policy Voice Assistant")

# -----------------------------
# Serve Premium Chat UI
# -----------------------------
app.mount(
    "/app",
    StaticFiles(directory=os.path.join(BASE_DIR, "..", "ui"), html=True),
    name="ui",
)

# -----------------------------
# API Routes
# -----------------------------
app.include_router(api_router)

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "Insurance Assistant running",
        "ui": "/app",
        "chat_api": "/api/chat",
        "voice_api": "/api/voice/inbound",
        "agent_queue": "/agent/queue",
    }
