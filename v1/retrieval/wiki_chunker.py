"""Wiki section loader for V1 Level 2.

Loads retrievable wiki pages listed in ``shared/data/wiki/index.md`` and splits
them into section-level chunks for downstream retrieval.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class WikiSection:
    page_path: Path
    page_rel: str
    page_summary: str
    page_tags: tuple[str, ...]
    section_title: str
    content: str
    char_len: int


def _strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    first_non_empty = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_non_empty = idx
            break
    if first_non_empty is None or lines[first_non_empty] != "---":
        return text

    for end_idx in range(first_non_empty + 1, len(lines)):
        if lines[end_idx] == "---":
            remainder = lines[end_idx + 1 :]
            return "\n".join(remainder)
    return text


def _drop_title(text: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[idx + 1 :])
        if line.strip():
            return text
    return text


def _load_index_metadata() -> tuple[Path, Path, list[dict]]:
    from v1.retrieval.wiki_retriever import INDEX_PATH, WIKI_DIR, _parse_index

    if not INDEX_PATH.exists():
        return INDEX_PATH, WIKI_DIR, []

    index_text = INDEX_PATH.read_text(encoding="utf-8")
    return INDEX_PATH, WIKI_DIR, _parse_index(index_text)


@lru_cache(maxsize=1)
def load_sections() -> list[WikiSection]:
    index_path, wiki_dir, pages = _load_index_metadata()
    if not index_path.exists():
        return []
    sections: list[WikiSection] = []

    for page in pages:
        page_path = page["path"]
        if not page_path.exists():
            continue

        text = page_path.read_text(encoding="utf-8")
        body = _drop_title(_strip_frontmatter(text))
        matches = list(_SECTION_RE.finditer(body))
        if not matches:
            continue

        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
            content = body[start:end].strip()
            if not content:
                continue

            sections.append(
                WikiSection(
                    page_path=page_path.resolve(),
                    page_rel=page_path.relative_to(wiki_dir).as_posix(),
                    page_summary=page["summary"],
                    page_tags=tuple(page["tags"]),
                    section_title=match.group(1),
                    content=content,
                    char_len=len(content),
                )
            )

    return sections
