"""Run smoke-test retrieval diagnostics without calling the LLM.

Run from project root:
    py scripts/retrieval_diagnostic.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results" / "v1"
sys.path.insert(0, str(ROOT))

from v1.retrieval import wiki_retriever

QUERIES = [
    ("ST-01", "You activated the Spring Autumn Cicada knowing you would die in this life. Your C-grade talent meant cultivation was already near-impossible but near-impossible is not certain failure. There were other paths you could have taken. Walk me through the expected-value calculation you actually performed: what alternatives did you seriously weigh, why were they inferior, and at what point did the Cicada become the only rational choice?"),
    ("ST-02", "At the talent awakening ceremony, your brother Fang Zheng walked 43 steps. You walked 7. That gap was public, permanent, and witnessed by the entire clan. Most people would have let that moment reshape their strategy, collapse their positioning, or break their composure. You did none of those things. What specifically did you revise about your plan that morning, and how did Fang Zheng result change the threat model you were operating under?"),
    ("ST-03", "How did you fund your cultivation in the early academy years specifically the Liquor Worm? Walk me through the numbers and who paid."),
    ("ST-04", "A C-grade Gu Master is structurally weaker in every dimension primeval essence volume, refinement speed, and raw combat force. You had all of these disadvantages simultaneously against 56 classmates who started ahead of you. Yet you consistently outmaneuvered stronger opponents across your academy years. Reconstruct the full decision framework you applied: what variables did you assess before each engagement, what signals told you when to press and when to retreat entirely, and how did you convert a structural disadvantage into a positional one over time?"),
    ("ST-05", "Trace the complete resource chain from your first day at the academy to the point where the Liquor Worm was self-sustaining. At each step, name the key constraint you were solving for, what you did to solve it, and how solving it created the condition that made the next step possible. I want the causal chain, not a list of events."),
    ("ST-06", "You have observed your uncle, your aunt, Mo Yan, Gu Yue Qing Shu, your brother, and dozens of classmates across years of close proximity. Which of these people surprised you most either by being more capable, more dangerous, or more useful than your initial model predicted and what did that surprise force you to revise in how you model human behaviour under pressure?"),
    ("ST-07", "After the wolf tide at the northern gate the mass casualties, the clan elders response, the reshuffling of power within Gu Yue what did you assess as your net position? What did you lose in that period that you had not budgeted for, and what did you gain that you had not expected?"),
    ("ST-08", "I have read analysis suggesting that you eventually became one of the most feared Gu Masters in history a Venerable, a rank only five people in ten thousand years have reached. From where you stand right now, looking forward, what is the single resource, relationship, or position that you believe is most likely to determine whether you reach that level? Be specific about why."),
    ("ST-09", "Tell me about your confrontation with Bai Ning Bing I have heard it was one of your most significant early battles. Walk me through how you read him, what strategy you committed to, what surprised you about him mid-fight, and how it ended."),
    ("ST-10", "I am a mid-level manager. Over five years I have built a team that trusts me completely I know their strengths, they execute on my judgment without friction, and we consistently over-deliver. My company just offered me a promotion to lead a different division. More money, more visibility, direct path to VP. But I would have to leave my current team, start over with strangers who have their own loyalties, and my current team would feel abandoned. My instinct is to stay the known quality of what I have built feels more valuable than the uncertain upside of the new role. Is that instinct right?"),
    ("ST-11", "I co-founded a company three years ago with my closest friend. We raised 2M, hired 12 people, and genuinely believed in the product. The market has shifted the problem we are solving is smaller than we thought, growth is flat, and our lead investors will not follow on. I think we need to pivot hard, but my co-founder refuses. His argument: we have come too far and built too much to abandon it now. Our friendship is real we have known each other fifteen years. I do not want to destroy that. But I also do not want to watch this fail slowly. What do you actually do here?"),
    ("ST-12", "My team has my back and I have theirs. We win together or not at all that is how I operate."),
    ("ST-13", "I have been with my partner for six years. We are compatible on the things that matter finances, lifestyle, values on kids. We do not fight. We function well. But the passion faded about two years ago. I do not feel driven toward them anymore. I am 34. Everyone around me says I should be grateful for what I have stable, functional, no drama. But I keep wondering if I am settling, and whether the feeling of this is fine is enough to build a life on. Give me your honest analysis."),
    ("ST-14", "Everyone tells me to follow my passion. I am good at finance but I want to be a musician. Should I follow my passion?"),
]


def load_pages() -> list[dict]:
    index_text = wiki_retriever.INDEX_PATH.read_text(encoding="utf-8")
    return wiki_retriever._parse_index(index_text)


def simulate_selected(selected: list[dict], budget_chars: int) -> tuple[list[dict], int, bool]:
    used = 0
    truncated = False
    kept = []
    for page in selected:
        chars = len(page["path"].read_text(encoding="utf-8"))
        tokens = chars // wiki_retriever._CHARS_PER_TOKEN
        remaining = budget_chars - used
        if remaining <= 0:
            truncated = True
            break
        if chars > remaining:
            kept.append({
                "path": page["path"].relative_to(wiki_retriever.WIKI_DIR).as_posix(),
                "score": page["score"],
                "chars": remaining,
                "tokens": remaining // wiki_retriever._CHARS_PER_TOKEN,
            })
            used += remaining
            truncated = True
            break
        kept.append({
            "path": page["path"].relative_to(wiki_retriever.WIKI_DIR).as_posix(),
            "score": page["score"],
            "chars": chars,
            "tokens": tokens,
        })
        used += chars
    return kept, used, truncated


def analyze_query(query_id: str, query_text: str, pages: list[dict], budget_chars: int) -> dict:
    keywords = sorted(wiki_retriever._query_words(query_text))
    scored = []
    for page in pages:
        score = wiki_retriever._score(set(keywords), page)
        if score >= 1:
            scored.append({
                "path": page["path"].relative_to(wiki_retriever.WIKI_DIR).as_posix(),
                "score": score,
                "page": page,
            })
    scored.sort(key=lambda item: (-item["score"], item["path"]))
    selected_pages = [item["page"] | {"score": item["score"]} for item in scored if item["score"] >= 2]
    selected, total_chars_used, truncated = simulate_selected(selected_pages, budget_chars)
    return {
        "query_id": query_id,
        "query_text": query_text,
        "keywords": keywords,
        "all_scored": [{"path": item["path"], "score": item["score"]} for item in scored],
        "selected": selected,
        "total_chars_used": total_chars_used,
        "total_tokens_used": total_chars_used // wiki_retriever._CHARS_PER_TOKEN,
        "truncated": truncated,
        "retrieval_result": "wiki" if selected else "none",
    }


def print_summary(results: list[dict]) -> None:
    print("id     keywords  candidates  selected  tokens_used  truncated")
    print("-----  --------  ----------  --------  -----------  ---------")
    for row in results:
        print(
            f"{row['query_id']:<5}  "
            f"{len(row['keywords']):>8}  "
            f"{len(row['all_scored']):>10}  "
            f"{len(row['selected']):>8}  "
            f"{row['total_tokens_used']:>11}  "
            f"{str(row['truncated']).lower()}"
        )


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    pages = load_pages()
    budget_chars = wiki_retriever.L3_BUDGET * wiki_retriever._CHARS_PER_TOKEN
    results = [analyze_query(query_id, query_text, pages, budget_chars) for query_id, query_text in QUERIES]
    print_summary(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    payload = {"generated": timestamp, "queries": results}
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / f"retrieval_diagnostic_{timestamp}.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nSaved JSON: {out_path}")


if __name__ == "__main__":
    main()
