# Insurance Policy Enquiry Voice Assistant (Full Project, Premium UI)

This project is a **compliance-first** Insurance Policy Enquiry assistant with:
- ChatGPT-style **premium web UI**
- **Voice input** (browser Web Speech API) + **Voice output** (SpeechSynthesis)
- Hybrid **Intent + Confidence** detection
- **Knowledge retrieval** (RAG-style) from approved docs (PDF/TXT) with section/source references
- **Multi-turn** conversation (session memory)
- **Human agent queue** (escalations) + callback flag
- **Analytics** (calls, intents, escalation rate) + audit logs
- Strict structured JSON responses aligned to your case study

> Note: For telephony (Twilio/Exotel), see `docs/TELEPHONY.md` for the webhook blueprint.
> This repo focuses on an **end-to-end runnable demo** that can be extended to real calls.

---

## 1) Quick start (Windows)

```bash
cd insurance_voice_assistant_fullstack
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- UI: http://127.0.0.1:8000/chat
- Health: http://127.0.0.1:8000/
- Agent Queue: http://127.0.0.1:8000/agent/queue
- Analytics Summary: http://127.0.0.1:8000/analytics/summary

---

## 2) Add policy documents (grounded answers)

Put approved documents here:
- `data/policy_docs/` (PDF or TXT)

Then build the searchable index:

```bash
python tools/build_kb.py
```

The index is saved in `data/kb/index.json`.

---

## 3) Test via API (Thunder Client / Postman)

### Chat (same endpoint used by UI)
`POST /api/chat`

Body:
```json
{
  "session_id": "demo-001",
  "transcribed_text": "What does my policy cover?",
  "language_hint": "English"
}
```

---

## 4) Environment variables (optional)

Create `.env` (optional):

```env
CONFIDENCE_THRESHOLD=0.65
# Optional Gemini (pluggable)
GEMINI_API_KEY=
GEMINI_MODEL=
```

If Gemini is not configured, the system runs in **hybrid deterministic mode** (rule-based + retrieval).

---

## 5) What to show in placement demo

1. Open `/chat` and ask: "What does my policy cover?"
2. Show sources displayed under each assistant message
3. Ask an out-of-scope question: "Can you pay my premium?"
4. Show escalation ticket created in `/agent/queue`
5. Show analytics in `/analytics/summary`

---

## License
Educational / placement demo.
