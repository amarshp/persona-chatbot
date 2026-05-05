"""Vector retrieval over raw chapter chunks (Phase 2).

Wraps the chromadb collection ``fang_yuan_chapters`` (chapters 1-120,
embedded with ``BAAI/bge-large-en-v1.5``) and exposes a
function-shaped equivalent of ``v1.retrieval.wiki_retriever.retrieve_sections``
so the same multi-query + CRAG downstream stack can consume both wiki sections
and chapter chunks uniformly.

Adapter strategy: each retrieved chapter chunk is wrapped as a ``WikiSection``
with ``page_rel="raw/chapter_NNNN.txt"`` and ``section_title="chunk<idx>"``.
Downstream code (CRAG, formatter) sees them as just more candidates.

The lexical_score returned is a rank-based int (top_k - rank, so #1 = top_k,
#20 = 1). This is used only for deterministic sorting before CRAG; the
cross-encoder is the actual relevance arbiter.
"""

from __future__ import annotations

import os
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from shared.config import DATA_DIR
from v1.retrieval.wiki_chunker import WikiSection

# Set SKIP_CHAPTER_RETRIEVAL=1 to disable vector chapter retrieval (e.g. to
# isolate wiki-only retrieval for smoke tests, or as an emergency kill-switch
# if a future environment surfaces a dual-model loading issue with
# bge-large-en-v1.5 + bge-reranker-base). Verified 2026-05-06: both models
# coexist cleanly in the live pipeline; chapter retrieval is enabled by default.
_SKIP = os.getenv("SKIP_CHAPTER_RETRIEVAL", "").lower() in {"1", "true", "yes"}

CHUNKS_DB_DIR = DATA_DIR / "chunks_db"
COLLECTION_NAME = "fang_yuan_chapters"
RAW_DIR = DATA_DIR / "raw"

_EF = None  # lazy-loaded on first query to avoid allocating 1.3GB at import time

_client: chromadb.api.client.Client | None = None
_collection = None


def _get_collection():
    global _client, _collection, _EF
    if _collection is not None:
        return _collection
    if _EF is None:
        _EF = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-en-v1.5")
    _client = chromadb.PersistentClient(path=str(CHUNKS_DB_DIR))
    _collection = _client.get_collection(COLLECTION_NAME, embedding_function=_EF)
    return _collection


def _wrap_chunk_as_section(
    chunk_id: str,
    document: str,
    metadata: dict,
) -> WikiSection:
    """Adapter: chromadb chunk -> WikiSection."""
    chapter_number = metadata.get("chapter_number")
    chunk_index = metadata.get("chunk_index", 0)
    chapter_title = metadata.get("chapter_title", "")
    source_file = metadata.get("source_file", f"chapter_{chapter_number:04d}.txt") if chapter_number else "unknown"

    page_rel = f"raw/{source_file}"
    page_path = RAW_DIR / source_file
    section_title = f"chunk{chunk_index}"

    return WikiSection(
        page_path=page_path,
        page_rel=page_rel,
        page_summary=chapter_title,
        page_tags=("chapter", f"ch{chapter_number}") if chapter_number else ("chapter",),
        section_title=section_title,
        content=document,
        char_len=len(document),
    )


def retrieve_chapter_sections(
    query: str,
    *,
    top_k: int = 20,
) -> list[tuple[int, WikiSection]]:
    """
    Vector retrieval over chapter chunks. Returns up to top_k results,
    each as ``(rank_score, WikiSection)`` so the shape matches
    ``v1.retrieval.wiki_retriever.retrieve_sections``.

    rank_score is ``top_k - rank`` (higher = better) so existing sort logic
    that prefers larger lexical_score keeps top results first. The CRAG
    cross-encoder downstream is the actual relevance arbiter.
    """
    if _SKIP or not query or not query.strip():
        return []

    collection = _get_collection()
    try:
        result = collection.query(
            query_texts=[query],
            n_results=top_k,
        )
    except Exception:
        return []

    ids = result.get("ids", [[]])
    documents = result.get("documents", [[]])
    metadatas = result.get("metadatas", [[]])
    if not ids or not ids[0]:
        return []

    out: list[tuple[int, WikiSection]] = []
    for rank, (cid, doc, meta) in enumerate(zip(ids[0], documents[0], metadatas[0])):
        section = _wrap_chunk_as_section(cid, doc, meta)
        rank_score = top_k - rank
        out.append((rank_score, section))
    return out
