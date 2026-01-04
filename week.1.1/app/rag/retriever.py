from __future__ import annotations
import json
from pathlib import Path
from rank_bm25 import BM25Okapi

INDEX_PATH = Path("data/kb/index.json")

def _load_index():
    if not INDEX_PATH.exists():
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _tokenize(text: str):
    return [t for t in ''.join([c.lower() if c.isalnum() else ' ' for c in text]).split() if t]

def retrieve_grounded_answer(user_text: str, intent: str, entities: dict) -> dict:
    idx = _load_index()
    if not idx or not idx.get("chunks"):
        # fallback: minimal answer when KB not built
        return {
            "answer": (
                "I can help with policy enquiries, but the knowledge base is not configured yet. "
                "Please upload approved policy documents and run `python tools/build_kb.py`."
            ),
            "references": [],
            "answer_quality": "NO_MATCH",
            "query_category": intent
        }

    chunks = idx["chunks"]
    corpus_tokens = [_tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(corpus_tokens)

    q = user_text
    scores = bm25.get_scores(_tokenize(q))
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]

    top = [chunks[i] for i in top_idx if scores[i] > 0]
    if not top:
        return {
            "answer": (
                "I couldn’t find an exact match in the approved policy content. "
                "I can escalate this to a human agent for confirmation."
            ),
            "references": [],
            "answer_quality": "NO_MATCH",
            "query_category": intent
        }

    # Compose grounded answer from top chunk (keep short for voice)
    primary = top[0]
    refs = [t["ref"] for t in top]
    answer = primary["text"].strip()
    if len(answer) > 360:
        answer = answer[:360].rsplit(" ", 1)[0] + "…"

    return {
        "answer": answer,
        "references": refs,
        "answer_quality": "MATCHED",
        "query_category": intent
    }
