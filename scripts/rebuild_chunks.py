"""Rebuild the fang_yuan_chapters ChromaDB collection.

Drops the existing collection and rebuilds it from all 120 raw chapter files
with overlapping chunks so facts at chunk boundaries are not lost.

Parameters
----------
CHUNK_SIZE : 1800 characters per chunk
OVERLAP    : 100 characters of overlap between consecutive chunks
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHUNK_SIZE = 1800
OVERLAP = 100
COLLECTION_NAME = "fang_yuan_chapters"
BATCH_SIZE = 100

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "shared" / "data"
RAW_DIR = DATA_DIR / "raw"
CHUNKS_DB_DIR = DATA_DIR / "chunks_db"

EF = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-en-v1.5")


def chunk_text(text: str) -> list[str]:
    stride = CHUNK_SIZE - OVERLAP
    chunks: list[str] = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + CHUNK_SIZE])
        start += stride
    return chunks


def main() -> None:
    manifest_path = RAW_DIR / "manifest.json"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(1)

    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    chapter_files = sorted(RAW_DIR.glob("chapter_*.txt"))
    print(f"Found {len(chapter_files)} chapter files.")

    all_ids: list[str] = []
    all_docs: list[str] = []
    all_meta: list[dict] = []

    for chapter_path in chapter_files:
        key = chapter_path.stem  # e.g. "chapter_0001"
        info = manifest.get(key, {})
        chapter_number: int = info.get("number", int(key.split("_")[1]))
        chapter_title: str = info.get("title", key)
        source_file: str = info.get("file", chapter_path.name)

        text = chapter_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        total = len(chunks)

        for idx, chunk in enumerate(chunks):
            all_ids.append(f"{key}_chunk{idx:03d}")
            all_docs.append(chunk)
            all_meta.append(
                {
                    "chapter_number": chapter_number,
                    "chapter_title": chapter_title,
                    "chunk_index": idx,
                    "char_count": len(chunk),
                    "source_file": source_file,
                    "total_chunks": total,
                }
            )

    print(f"Total chunks to index: {len(all_ids)}")

    client = chromadb.PersistentClient(path=str(CHUNKS_DB_DIR))
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Dropped existing collection.")
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME, embedding_function=EF)
    print("Created new collection. Embedding and indexing (this takes a few minutes)...")

    total_chunks = len(all_ids)
    for batch_start in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_chunks)
        collection.add(
            ids=all_ids[batch_start:batch_end],
            documents=all_docs[batch_start:batch_end],
            metadatas=all_meta[batch_start:batch_end],
        )
        pct = batch_end / total_chunks * 100
        print(f"  [{pct:5.1f}%] Indexed chunks {batch_start}–{batch_end - 1}")

    max_ch = max(m["chapter_number"] for m in all_meta)
    print(f"\nDone. Total chunks: {total_chunks}. Chapters covered: 1–{max_ch}.")


if __name__ == "__main__":
    main()
