"""
V1 Level 1 baseline — terminal chat loop.

Usage
-----
    py v1/main.py

Commands (type at the prompt)
------------------------------
    quit / exit  — end session and print token summary
    reset        — clear conversation history, keep composer loaded
    reload       — re-read personality JSONs from disk (no restart needed)
    debug        — print the full current system prompt to stdout
    stats        — print token usage so far
"""

from __future__ import annotations

import sys
from pathlib import Path

# ── path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import PRIMARY_MODEL, CONVERSATION_WINDOW, MAX_OUTPUT_TOKENS
from v1.persona.prompt_composer import PromptComposer

# ── constants ─────────────────────────────────────────────────────────────────
HISTORY_PAIRS   = CONVERSATION_WINDOW   # 8 pairs = 16 messages kept in context
RESPONSE_TOKENS = MAX_OUTPUT_TOKENS     # 1024
MODEL           = PRIMARY_MODEL         # claude-sonnet-4.6


# ── helpers ───────────────────────────────────────────────────────────────────

def _trim_history(history: list[dict], max_pairs: int) -> list[dict]:
    """Keep only the last max_pairs user/assistant pairs."""
    max_msgs = max_pairs * 2
    return history[-max_msgs:] if len(history) > max_msgs else history


def _print_stats(client: LLMClient) -> None:
    m = client.get_metrics()
    print(f"\n── Token usage ──────────────────────────────")
    print(f"  Calls       : {len(m['llm_calls'])}")
    print(f"  Tokens in   : {m['total_tokens_in']:,}")
    print(f"  Tokens out  : {m['total_tokens_out']:,}")
    total_ms = sum(c["latency_ms"] for c in m["llm_calls"])
    print(f"  Total time  : {total_ms/1000:.1f}s")
    print(f"────────────────────────────────────────────\n")


def _print_debug(composer: PromptComposer, state: dict) -> None:
    print("\n" + "═" * 72)
    print(composer.debug_layers(state))
    print("═" * 72 + "\n")


# ── main loop ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("Loading personality files...", end=" ", flush=True)
    composer = PromptComposer()
    client   = LLMClient()
    state    = composer.initial_state()
    print("done.")

    sys_chars = len(composer.l1) + len(composer.l2)
    print(f"System prompt: ~{sys_chars // 4:,} tokens  |  Model: {MODEL}")
    print('Commands: quit, reset, reload, debug, stats')
    print("─" * 60)

    history: list[dict] = []

    while True:
        # ── input ──────────────────────────────────────────────────────
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            _print_stats(client)
            break

        if not user_input:
            continue

        # ── commands ───────────────────────────────────────────────────
        cmd = user_input.lower()

        if cmd in ("quit", "exit"):
            _print_stats(client)
            break

        if cmd == "reset":
            history = []
            print("[History cleared]")
            continue

        if cmd == "reload":
            print("Reloading personality files...", end=" ", flush=True)
            composer = PromptComposer()
            state    = composer.initial_state()
            print("done.")
            continue

        if cmd == "debug":
            _print_debug(composer, state)
            continue

        if cmd == "stats":
            _print_stats(client)
            continue

        # ── build messages ─────────────────────────────────────────────
        trimmed = _trim_history(history, HISTORY_PAIRS)
        messages = composer.build(trimmed, state)
        messages.append({"role": "user", "content": user_input})

        # ── call LLM ───────────────────────────────────────────────────
        try:
            response = client.generate(
                messages,
                model=MODEL,
                temperature=0.7,
                max_tokens=RESPONSE_TOKENS,
                purpose="chat_turn",
            )
        except Exception as exc:
            print(f"\n[Error: {exc}]")
            continue

        # ── print and record ───────────────────────────────────────────
        print(f"\nFang Yuan: {response}")

        history.append({"role": "user",      "content": user_input})
        history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
