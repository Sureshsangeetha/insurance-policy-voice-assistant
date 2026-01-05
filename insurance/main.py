from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api.routes import router

load_dotenv()

app = FastAPI(title="Insurance Policy Enquiry AI Agent")

# ✅ CORS CONFIGURATION (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend from any origin (demo-safe)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "status": "running",
        "gemini_api_key_loaded": bool(os.getenv("GEMINI_API_KEY"))
    }
