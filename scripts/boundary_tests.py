"""Run boundary retrieval diagnostics without calling the LLM.

Run from project root:
    python scripts/boundary_tests.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import DATA_DIR
from v1.retrieval.query_router import route
from v1.retrieval.wiki_retriever import _CHARS_PER_TOKEN, retrieve

WIKI_DIR = DATA_DIR / "wiki"
RAW_DIR = DATA_DIR / "raw"

BLOCK_SEPARATOR = "\n\n---\n\n"
HEADER_SEPARATOR = " — "
VOCAB_TRIGGER_THRESHOLD = 0.30
PHASE3_SECTIONS_THRESHOLD = 3.0
PHASE3_TOKENS_THRESHOLD = 1800.0
SOFT_LEAK_THRESHOLD = 2.0

VOCABULARY_TESTS: list[tuple[str, str, str]] = [
    (
        "How do you handle people who pretend to be your friend?",
        "philosophy/self_interest_and_human_nature.md",
        "Fang Yuan's Reasoning",
    ),
    (
        "What does it take for a weakling to climb?",
        "philosophy/strength_as_foundation.md",
        "Fang Yuan's Reasoning",
    ),
    (
        "How do you weigh dignity against staying alive?",
        "philosophy/demonic_path_survival.md",
        "Fang Yuan's Reasoning",
    ),
    (
        "When you sense someone wants to harm you, what's your move?",
        "philosophy/killing_logic.md",
        "The Principle",
    ),
    (
        "When is it worth wagering everything on a long shot?",
        "decisions/rebirth_and_spring_autumn_cicada.md",
        "Fang Yuan's Reasoning",
    ),
    (
        "How did you make money off other students?",
        "decisions/extortion_campaign.md",
        "Key Events",
    ),
    (
        "What did you do when the merchant came for you?",
        "decisions/jia_jin_sheng_killing.md",
        "Key Events",
    ),
    (
        "How did your guardians treat you growing up?",
        "relationships/uncle_and_aunt.md",
        "Summary",
    ),
    (
        "Tell me about the time you played dead during a fight.",
        "events/beast_horde_survival.md",
        "Key Events",
    ),
    (
        "Walk me through the politics of your group selection.",
        "decisions/jiao_san_team_selection.md",
        "Fang Yuan's Reasoning",
    ),
]

COVERAGE_TESTS: list[str] = [
    "Tell me about Mo Bei specifically and what role he plays in the academy power structure.",
    "Walk me through your year-end exam — what happened and what did you decide?",
    "What do you make of Gu Yue Bo, the clan leader?",
    "Tell me about Wang Da and how you ended up dealing with him.",
    "What was the Chi family patriarch like?",
    "Tell me about Chi Shan — the top Chi faction combatant.",
]

OUT_OF_SCOPE_TESTS: list[tuple[str, list[str]]] = [
    ("Walk me through the northern gate wolf tide aftermath in detail.", []),
    ("Tell me about your fight with Bai Ning Bing — strategy and outcome.", []),
    ("How did you become a Venerable?", []),
    ("What happened during the immortal war years?", []),
]

# ── Phase 1 verification: query routing ────────────────────────────
# Phase 1 shipped v1/retrieval/query_router.py with two routes:
#   "wiki" → run wiki retrieval
#   "none" → skip retrieval entirely (trivial messages)
# These tests verify routing is stable. Should currently be all-PASS.
# Will become a regression guard when Phase 3 adds a third "vector"
# route — those tests must keep passing as routing changes.

ROUTING_TESTS: list[tuple[str, str]] = [
    ("ok", "none"),
    ("yes", "none"),
    ("go on", "none"),
    ("sure", "none"),
    ("hmm", "none"),
    ("Tell me about the Spring Autumn Cicada.", "wiki"),
    ("How did you become a Venerable?", "wiki"),
    ("Walk me through the politics of your group selection.", "wiki"),
    ("What does it take for a weakling to climb?", "wiki"),
    ("Mo Bei.", "wiki"),
]

# ── Phase 5 trigger: wiki health (static structural checks) ────────
# Files in shared/data/wiki/ that are NOT content pages and should
# be excluded from orphan/coverage analysis. Anything else is a
# content page and is expected to: (a) be linked from index.md,
# (b) have YAML frontmatter with `tags` and `chapters_covered`,
# (c) reference only chapters that exist as raw chapter files.

WIKI_META_FILES: frozenset[str] = frozenset(
    {
        "SCHEMA.md",
        "CONVENTIONS.md",
        "TEST_PROMPTS.md",
        "TEST_RESULTS.md",
        "index.md",
    }
)

PHASE5_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#]+\.md)(?:#[^)]*)?\)")
PHASE5_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
PHASE5_TAGS_RE = re.compile(r"^tags:\s*\[(.*?)\]\s*$", re.MULTILINE)
PHASE5_CHAPTERS_RE = re.compile(
    r"^chapters_covered:\s*\[(.*?)\]\s*$", re.MULTILINE
)


@dataclass(frozen=True)
class RetrievedBlock:
    header: str
    page_rel: str
    section_title: str
    content: str


@dataclass(frozen=True)
class RoutingResult:
    test_id: str
    query: str
    expected_route: str
    actual_route: str

    @property
    def passed(self) -> bool:
        return self.expected_route == self.actual_route


@dataclass(frozen=True)
class VocabularyResult:
    test_id: str
    expected_page_rel: str
    expected_section_title: str
    passed: bool

    @property
    def expected_header(self) -> str:
        return format_header(self.expected_page_rel, self.expected_section_title)


@dataclass(frozen=True)
class RetrievalSummary:
    sections_returned: int
    pages_touched: int
    total_tokens: int


@dataclass(frozen=True)
class CoverageResult:
    test_id: str
    query: str
    sections_returned: int
    pages_touched: int
    total_tokens: int


@dataclass(frozen=True)
class OutOfScopeResult:
    test_id: str
    query: str
    sections_returned: int
    total_tokens: int
    forbidden_hits: tuple[str, ...]


@dataclass(frozen=True)
class WikiHealthIssue:
    category: str
    page_rel: str
    detail: str


@dataclass(frozen=True)
class WikiHealthReport:
    content_pages: tuple[str, ...]
    issues: tuple[WikiHealthIssue, ...]


def format_header(page_rel: str, section_title: str) -> str:
    return f"## {section_title}{HEADER_SEPARATOR}{page_rel}"


def truncate(text: str, width: int) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= width:
        return normalized
    if width <= 3:
        return normalized[:width]
    return f"{normalized[:width - 3]}..."


def split_blocks(result: str) -> list[str]:
    if not result:
        return []
    return [block for block in result.split(BLOCK_SEPARATOR) if block.strip()]


def parse_block(block: str) -> RetrievedBlock | None:
    lines = block.splitlines()
    if not lines:
        return None
    header = lines[0].strip()
    if not header.startswith("## ") or HEADER_SEPARATOR not in header:
        return None
    title_part, page_rel = header[3:].split(HEADER_SEPARATOR, 1)
    return RetrievedBlock(
        header=header,
        section_title=title_part.strip(),
        page_rel=page_rel.strip(),
        content=block,
    )


def parse_blocks(result: str) -> list[RetrievedBlock]:
    parsed: list[RetrievedBlock] = []
    for block in split_blocks(result):
        parsed_block = parse_block(block)
        if parsed_block is not None:
            parsed.append(parsed_block)
    return parsed


def summarize_result(result: str) -> RetrievalSummary:
    blocks = parse_blocks(result)
    pages = {block.page_rel for block in blocks}
    return RetrievalSummary(
        sections_returned=len(blocks),
        pages_touched=len(pages),
        total_tokens=len(result) // _CHARS_PER_TOKEN,
    )


def run_routing_tests() -> list[RoutingResult]:
    rows: list[RoutingResult] = []
    for index, (query, expected) in enumerate(ROUTING_TESTS, start=1):
        rows.append(
            RoutingResult(
                test_id=f"R{index:02d}",
                query=query,
                expected_route=expected,
                actual_route=route(query),
            )
        )
    return rows


def run_vocabulary_tests() -> list[VocabularyResult]:
    rows: list[VocabularyResult] = []
    for index, (query, page_rel, section_title) in enumerate(VOCABULARY_TESTS, start=1):
        result = retrieve(query)
        expected_header = format_header(page_rel, section_title)
        rows.append(
            VocabularyResult(
                test_id=f"V{index:02d}",
                expected_page_rel=page_rel,
                expected_section_title=section_title,
                passed=expected_header in result,
            )
        )
    return rows


def run_coverage_tests() -> list[CoverageResult]:
    rows: list[CoverageResult] = []
    for index, query in enumerate(COVERAGE_TESTS, start=1):
        result = retrieve(query)
        summary = summarize_result(result)
        rows.append(
            CoverageResult(
                test_id=f"C{index:02d}",
                query=query,
                sections_returned=summary.sections_returned,
                pages_touched=summary.pages_touched,
                total_tokens=summary.total_tokens,
            )
        )
    return rows


def run_out_of_scope_tests() -> list[OutOfScopeResult]:
    rows: list[OutOfScopeResult] = []
    for index, (query, forbidden_page_rels) in enumerate(OUT_OF_SCOPE_TESTS, start=1):
        result = retrieve(query)
        summary = summarize_result(result)
        hits = tuple(page_rel for page_rel in forbidden_page_rels if page_rel in result)
        rows.append(
            OutOfScopeResult(
                test_id=f"O{index:02d}",
                query=query,
                sections_returned=summary.sections_returned,
                total_tokens=summary.total_tokens,
                forbidden_hits=hits,
            )
        )
    return rows


def _phase5_iter_content_pages() -> list[Path]:
    """All .md files under WIKI_DIR that are not meta files."""
    if not WIKI_DIR.exists():
        return []
    return sorted(
        path for path in WIKI_DIR.rglob("*.md") if path.name not in WIKI_META_FILES
    )


def _phase5_rel(path: Path) -> str:
    return path.relative_to(WIKI_DIR).as_posix()


def _phase5_check_orphans(
    index_text: str,
    content_pages: list[Path],
) -> list[WikiHealthIssue]:
    issues: list[WikiHealthIssue] = []
    linked_targets = {
        match.group(1).strip()
        for match in PHASE5_LINK_RE.finditer(index_text)
    }
    for page in content_pages:
        rel = _phase5_rel(page)
        if rel not in linked_targets:
            issues.append(
                WikiHealthIssue(
                    category="orphan",
                    page_rel=rel,
                    detail="not linked from index.md",
                )
            )
    return issues


def _phase5_check_broken_refs(
    content_pages: list[Path],
    index_path: Path,
) -> list[WikiHealthIssue]:
    issues: list[WikiHealthIssue] = []
    files_to_scan: list[Path] = list(content_pages)
    if index_path.exists():
        files_to_scan.append(index_path)
    wiki_root = WIKI_DIR.resolve()
    for page in files_to_scan:
        try:
            text = page.read_text(encoding="utf-8")
        except OSError:
            continue
        page_dir = page.parent
        rel_owner = _phase5_rel(page) if page != index_path else "index.md"
        for match in PHASE5_LINK_RE.finditer(text):
            target_rel = match.group(1).strip()
            if target_rel.startswith(("http://", "https://")):
                continue
            target = (page_dir / target_rel).resolve()
            try:
                target.relative_to(wiki_root)
            except ValueError:
                continue
            if not target.exists():
                issues.append(
                    WikiHealthIssue(
                        category="broken_ref",
                        page_rel=rel_owner,
                        detail=f"link target missing: {target_rel}",
                    )
                )
    return issues


def _phase5_check_frontmatter(content_pages: list[Path]) -> list[WikiHealthIssue]:
    issues: list[WikiHealthIssue] = []
    for page in content_pages:
        rel = _phase5_rel(page)
        try:
            text = page.read_text(encoding="utf-8")
        except OSError:
            issues.append(
                WikiHealthIssue(
                    category="frontmatter",
                    page_rel=rel,
                    detail="unreadable",
                )
            )
            continue
        fm_match = PHASE5_FRONTMATTER_RE.match(text)
        if fm_match is None:
            issues.append(
                WikiHealthIssue(
                    category="frontmatter",
                    page_rel=rel,
                    detail="missing YAML frontmatter block",
                )
            )
            continue
        fm = fm_match.group(1)
        if PHASE5_TAGS_RE.search(fm) is None:
            issues.append(
                WikiHealthIssue(
                    category="frontmatter",
                    page_rel=rel,
                    detail="frontmatter missing `tags`",
                )
            )
        if PHASE5_CHAPTERS_RE.search(fm) is None:
            issues.append(
                WikiHealthIssue(
                    category="frontmatter",
                    page_rel=rel,
                    detail="frontmatter missing `chapters_covered`",
                )
            )
    return issues


def _phase5_check_missing_chapters(
    content_pages: list[Path],
) -> list[WikiHealthIssue]:
    issues: list[WikiHealthIssue] = []
    for page in content_pages:
        rel = _phase5_rel(page)
        try:
            text = page.read_text(encoding="utf-8")
        except OSError:
            continue
        fm_match = PHASE5_FRONTMATTER_RE.match(text)
        if fm_match is None:
            continue
        chap_match = PHASE5_CHAPTERS_RE.search(fm_match.group(1))
        if chap_match is None:
            continue
        raw = chap_match.group(1)
        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue
            try:
                chapter_num = int(token)
            except ValueError:
                continue
            chapter_file = RAW_DIR / f"chapter_{chapter_num:04d}.txt"
            if not chapter_file.exists():
                issues.append(
                    WikiHealthIssue(
                        category="missing_chapter",
                        page_rel=rel,
                        detail=(
                            "chapters_covered references chapter "
                            f"{chapter_num:04d} but raw file missing"
                        ),
                    )
                )
    return issues


def run_wiki_health() -> WikiHealthReport:
    content_pages = _phase5_iter_content_pages()
    issues: list[WikiHealthIssue] = []
    index_path = WIKI_DIR / "index.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    issues.extend(_phase5_check_orphans(index_text, content_pages))
    issues.extend(_phase5_check_broken_refs(content_pages, index_path))
    issues.extend(_phase5_check_frontmatter(content_pages))
    issues.extend(_phase5_check_missing_chapters(content_pages))
    return WikiHealthReport(
        content_pages=tuple(_phase5_rel(page) for page in content_pages),
        issues=tuple(issues),
    )


def average(values: Iterable[int]) -> float:
    items = list(values)
    if not items:
        return 0.0
    return sum(items) / len(items)


def routing_verdict(rows: list[RoutingResult]) -> tuple[str, int, int]:
    total = len(rows)
    fails = sum(1 for row in rows if not row.passed)
    verdict = "PASS" if fails == 0 else "FAIL"
    return verdict, fails, total


def vocabulary_verdict(rows: list[VocabularyResult]) -> tuple[str, int, int]:
    total = len(rows)
    fails = sum(1 for row in rows if not row.passed)
    failure_rate = (fails / total) if total else 0.0
    verdict = "ACTIVE" if failure_rate >= VOCAB_TRIGGER_THRESHOLD else "INACTIVE"
    return verdict, fails, total


def coverage_verdict(rows: list[CoverageResult]) -> tuple[str, float, float]:
    avg_sections = average(row.sections_returned for row in rows)
    avg_tokens = average(row.total_tokens for row in rows)
    is_active = (
        avg_sections >= PHASE3_SECTIONS_THRESHOLD
        and avg_tokens >= PHASE3_TOKENS_THRESHOLD
    )
    return ("ACTIVE" if is_active else "INACTIVE"), avg_sections, avg_tokens


def out_of_scope_verdict(rows: list[OutOfScopeResult]) -> tuple[str, float]:
    avg_sections = average(row.sections_returned for row in rows)
    if avg_sections <= 1.0:
        return "PASS", avg_sections
    if avg_sections <= SOFT_LEAK_THRESHOLD:
        return "soft-leak", avg_sections
    return "clear-leak", avg_sections


def wiki_health_verdict(report: WikiHealthReport) -> tuple[str, int]:
    count = len(report.issues)
    verdict = "CLEAN" if count == 0 else f"{count} ISSUES"
    return verdict, count


def print_routing_section(rows: list[RoutingResult]) -> None:
    verdict, fails, total = routing_verdict(rows)
    print("── Phase 1 verification: query routing ───────────────────────────")
    print("id   query (truncated)                          expected  actual    result")
    print("--   ---------------------------------------    --------  --------  ------")
    for row in rows:
        print(
            f"{row.test_id:<3}  "
            f"{truncate(row.query, 39):<39}    "
            f"{row.expected_route:<8}  "
            f"{row.actual_route:<8}  "
            f"{'PASS' if row.passed else 'FAIL'}"
        )
    passes = total - fails
    print(
        f"\nRouting tests: {passes}/{total} pass.   "
        f"Phase 1 routing: {verdict} ({fails} unexpected classifications)"
    )


def print_vocabulary_section(rows: list[VocabularyResult]) -> None:
    verdict, fails, total = vocabulary_verdict(rows)
    print("── Phase 2/4 boundary: vocabulary gap ────────────────────────────")
    print("id   expected                                                 result")
    print("--   ------------------------------------------------------   ------")
    for row in rows:
        print(
            f"{row.test_id:<3}  "
            f"{truncate(row.expected_header[3:], 54):<54}   "
            f"{'PASS' if row.passed else 'FAIL'}"
        )
    passes = total - fails
    print(
        f"\nVocabulary tests: {passes}/{total} pass.   "
        f"Phase 2/4 trigger: {fails} fails (≥30% threshold = {verdict})"
    )


def print_coverage_section(rows: list[CoverageResult]) -> None:
    print("\n── Phase 3 boundary: coverage gap ────────────────────────────────")
    print("id   query (truncated)                          sections_returned  pages_touched")
    print("--   ---------------------------------------    -----------------  -------------")
    for row in rows:
        print(
            f"{row.test_id:<3}  "
            f"{truncate(row.query, 39):<39}    "
            f"{row.sections_returned:>17}  "
            f"{row.pages_touched:>13}"
        )
    print(
        "\nCoverage tests: each row shows what retrieval surfaced for an "
        "officially uncovered topic."
    )
    print(
        "A row returning ≥3 sections is a candidate false-positive "
        "(Phase 3 or wiki expansion)."
    )


def print_out_of_scope_section(rows: list[OutOfScopeResult]) -> None:
    print("\n── Anti-fabrication regression: out-of-scope queries ─────────────")
    print("id   query (truncated)                          sections_returned  total_tokens")
    print("--   ---------------------------------------    -----------------  ------------")
    for row in rows:
        print(
            f"{row.test_id:<3}  "
            f"{truncate(row.query, 39):<39}    "
            f"{row.sections_returned:>17}  "
            f"{row.total_tokens:>12}"
        )
        if row.forbidden_hits:
            print(f"     forbidden page hits: {', '.join(row.forbidden_hits)}")


def print_wiki_health_section(report: WikiHealthReport) -> None:
    verdict, count = wiki_health_verdict(report)
    print("\n── Phase 5 trigger: wiki health (static checks) ──────────────────")
    print(
        f"Content pages scanned: {len(report.content_pages)}   "
        f"Issues found: {count}"
    )
    if not report.issues:
        print("All checks pass: orphan / broken-ref / frontmatter / chapter coverage.")
        return
    categories = ("orphan", "broken_ref", "frontmatter", "missing_chapter")
    for category in categories:
        bucket = [issue for issue in report.issues if issue.category == category]
        if not bucket:
            continue
        print(f"\n  [{category}] ({len(bucket)})")
        for issue in bucket:
            print(f"    - {issue.page_rel}: {issue.detail}")


def print_summary(
    routing_rows: list[RoutingResult],
    vocabulary_rows: list[VocabularyResult],
    coverage_rows: list[CoverageResult],
    out_of_scope_rows: list[OutOfScopeResult],
    wiki_health_report: WikiHealthReport,
) -> None:
    vocab_verdict, vocab_fails, vocab_total = vocabulary_verdict(vocabulary_rows)
    phase3_verdict, avg_coverage_sections, avg_coverage_tokens = coverage_verdict(
        coverage_rows
    )
    scope_verdict, avg_scope_sections = out_of_scope_verdict(out_of_scope_rows)
    routing_verdict_str, routing_fails, routing_total = routing_verdict(routing_rows)
    health_verdict_str, health_count = wiki_health_verdict(wiki_health_report)
    print("\nSUMMARY")
    print(
        "Phase 2/4 trigger: "
        f"{vocab_verdict} ({vocab_fails}/{vocab_total} vocab fails, threshold 30%)"
    )
    print(
        "Phase 3 trigger:   "
        f"{phase3_verdict} (avg sections={avg_coverage_sections:.2f}, "
        f"avg total_tokens={avg_coverage_tokens:.0f})"
    )
    print(
        "Out-of-scope regression: "
        f"{scope_verdict} (avg sections={avg_scope_sections:.2f})"
    )
    print(
        "Phase 1 routing:   "
        f"{routing_verdict_str} ({routing_fails}/{routing_total} unexpected classifications)"
    )
    print(
        "Phase 5 wiki health: "
        f"{health_verdict_str} ({health_count} structural issues)"
    )


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    routing_rows = run_routing_tests()
    vocabulary_rows = run_vocabulary_tests()
    coverage_rows = run_coverage_tests()
    out_of_scope_rows = run_out_of_scope_tests()
    wiki_health_report = run_wiki_health()

    print_routing_section(routing_rows)
    print()
    print_vocabulary_section(vocabulary_rows)
    print_coverage_section(coverage_rows)
    print_out_of_scope_section(out_of_scope_rows)
    print_wiki_health_section(wiki_health_report)
    print_summary(
        routing_rows,
        vocabulary_rows,
        coverage_rows,
        out_of_scope_rows,
        wiki_health_report,
    )


if __name__ == "__main__":
    main()
