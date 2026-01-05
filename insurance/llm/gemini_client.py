import os
import threading
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_response(policy_text: str, timeout_seconds: int = 4) -> str:
    """
    Gemini STRICT RAG with timeout.
    If Gemini is slow, return policy text immediately.
    """

    if not GEMINI_API_KEY:
        return policy_text

    result = {"text": policy_text}

    def call_gemini():
        try:
            import google.generativeai as genai

            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            Rewrite the following insurance policy information clearly.
            Do NOT add new information.
            Do NOT give advice.

            Policy text:
            {policy_text}
            """

            response = model.generate_content(prompt)
            result["text"] = response.text.strip()

        except Exception:
            result["text"] = policy_text

    thread = threading.Thread(target=call_gemini)
    thread.start()
    thread.join(timeout_seconds)

    return result["text"]
