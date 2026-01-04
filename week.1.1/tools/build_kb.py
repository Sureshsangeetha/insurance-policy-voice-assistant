from __future__ import annotations
import os
import json
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path("data/policy_docs")
OUT_DIR = Path("data/kb")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def read_txt(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def read_pdf(p: Path) -> str:
    reader = PdfReader(str(p))
    texts = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        texts.append(f"\n[PAGE {i+1}]\n{t}")
    return "\n".join(texts)

def chunk(text: str, chunk_size: int = 800, overlap: int = 120):
    # Simple chunking by characters (good enough for demo)
    chunks = []
    i = 0
    while i < len(text):
        j = min(len(text), i + chunk_size)
        chunks.append(text[i:j])
        i = max(i + chunk_size - overlap, i + 1)
    return chunks

def main():
    if not DATA_DIR.exists():
        print("No data/policy_docs directory found.")
        return

    all_chunks = []
    for p in DATA_DIR.rglob("*"):
        if p.is_dir():
            continue
        if p.suffix.lower() == ".txt":
            text = read_txt(p)
        elif p.suffix.lower() == ".pdf":
            text = read_pdf(p)
        else:
            continue

        parts = chunk(text)
        for k, part in enumerate(parts):
            ref = f"{p.stem}_Chunk_{k+1}"
            all_chunks.append({
                "ref": ref,
                "source_file": str(p.as_posix()),
                "text": part
            })

    index = {"chunks": all_chunks}
    out = OUT_DIR / "index.json"
    out.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built KB index with {len(all_chunks)} chunks -> {out}")

if __name__ == "__main__":
    main()
