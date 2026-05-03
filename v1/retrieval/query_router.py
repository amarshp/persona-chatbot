"""Simple query router for V1 wiki retrieval."""

from __future__ import annotations

import re
from typing import Literal

_QUESTION_WORDS = frozenset({
    "who", "what", "why", "how", "when", "where", "which", "whose", "whom",
    "should", "would", "could", "can", "do", "does", "did", "is", "are", "was",
    "were", "will", "tell", "explain", "describe", "walk",
})

_NOVEL_KEYWORDS = frozenset({
    "fang", "yuan", "zheng", "mo", "yan", "bei", "chen", "shen", "cui", "jiao",
    "san", "gu", "yue", "bo", "qing", "shu", "wang", "da", "bai", "ning", "bing",
    "chi", "lian", "shan", "kong", "jing", "jia", "jin", "sheng", "hua", "xin",
    "dong", "tu", "jiang", "ya",
    "cicada", "sac", "liquor", "worm", "primeval", "aperture", "cultivation",
    "clan", "tribe", "demonic", "demon", "axiom", "awakening", "talent", "refine",
    "refining", "rank", "venerable", "beast", "horde", "wolf", "tide", "gate",
    "moonblade", "photo", "audio", "essence", "stones", "moonlight", "cave",
    "academy", "chairman", "faction", "heir",
})


def route(query: str) -> Literal["wiki", "none"]:
    words = [word for word in re.split(r"\W+", query.lower()) if word]
    if len(words) >= 8:
        return "wiki"
    if any(word in _QUESTION_WORDS for word in words):
        return "wiki"
    if any(word in _NOVEL_KEYWORDS for word in words):
        return "wiki"
    return "none"
