"""Entity-presence faithfulness pre-filter.

Stage 1 of the anti-fabrication pipeline: extract named entities (multi-word
capitalized phrases) from the spoken response and check whether each appears
in the retrieved L3 context via string matching.

No LLM call — effectively free per turn. Catches Q20-class failures where
the model invents an org/sect name that is absent from any retrieved chunk.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_NE_PATTERN = re.compile(r"\b[A-Z][a-zA-Z'\-]*(?:\s+[A-Z][a-zA-Z'\-]+){1,}\b")

_STOPWORDS = {
    "The", "A", "An", "In", "On", "At", "By", "For", "Of", "To", "And",
    "But", "Or", "If", "As", "With", "From", "That", "This", "These",
    "Those", "His", "Her", "Their", "Our", "Your", "My", "Its", "Do",
    "Did", "Will", "Can", "May", "Must", "Shall", "Should", "Would",
    "Could", "Not", "No", "Yes", "You", "He", "She", "We", "They",
    "It", "I", "Me", "Him", "When", "Where", "What", "Who", "How",
    "There", "Here", "Now", "Then", "One", "Two", "Three",
    "Until", "After", "Before", "Once", "Since", "While", "Though",
    "Even", "Still", "Just", "Only", "Also", "Both", "Each",
    "Rank", "Level", "Stage", "Grade",
}


@dataclass(frozen=True)
class GuardResult:
    flagged: bool
    ungrounded_entities: list[str]


def extract_named_entities(text: str) -> list[str]:
    """Return de-duplicated multi-word capitalized phrases from text.

    Leading stopwords are stripped from a match rather than discarding it,
    so "The Bloodwing Demon Sect" yields "Bloodwing Demon Sect".
    """
    seen: set[str] = set()
    results: list[str] = []
    for m in _NE_PATTERN.finditer(text):
        words = m.group(0).strip().split()
        while words and words[0] in _STOPWORDS:
            words = words[1:]
        if len(words) < 2:
            continue
        phrase = " ".join(words)
        if phrase not in seen:
            seen.add(phrase)
            results.append(phrase)
    return results


def _normalize_for_match(s: str) -> str:
    """Normalize an entity / context substring for matching.

    - lowercase
    - strip English possessive 's / s' so 'Bai Ning Bing's' matches a context
      that names 'Bai Ning Bing'
    - collapse internal whitespace so 'Flower  Wine Monk' matches 'Flower Wine Monk'
    """
    s = s.lower()
    # Strip possessive on the trailing word (handles 'Monk's' -> 'monk' and "Mosses' " -> 'mosses')
    s = re.sub(r"(\w)['’]s\b", r"\1", s)
    s = re.sub(r"(\w)s['’]\b", r"\1s", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def check_entity_presence(entities: list[str], context: str) -> list[str]:
    """Return entities that do NOT appear in context (case-insensitive).

    Possessive forms are normalized — 'Bai Ning Bing's' matches a context
    that names 'Bai Ning Bing'.
    """
    context_norm = _normalize_for_match(context)
    return [e for e in entities if _normalize_for_match(e) not in context_norm]


def guard(spoken: str, l3_context: str) -> GuardResult:
    """Run entity-presence pre-filter against retrieved L3 context.

    Returns GuardResult(flagged=True, ungrounded_entities=[...]) when the
    spoken text names entities absent from the retrieved context — a signal
    the model may be drawing on training-corpus memory rather than grounded
    facts.

    When l3_context is empty AND spoken contains specific entities, every
    extracted entity is flagged as ungrounded — this is the maximum-signal
    fabrication case (D02-class: refusal-template language wrapping training
    data). When spoken contains no extractable entities, the guard returns
    flagged=False regardless of L3.
    """
    entities = extract_named_entities(spoken)
    if not entities:
        return GuardResult(flagged=False, ungrounded_entities=[])

    if not l3_context:
        return GuardResult(flagged=True, ungrounded_entities=entities)

    ungrounded = check_entity_presence(entities, l3_context)
    return GuardResult(flagged=bool(ungrounded), ungrounded_entities=ungrounded)
