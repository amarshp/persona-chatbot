"""Shared configuration for V1 and V2 A/B experiment.

All controlled variables live here. Both systems import from this file
to ensure identical settings for a fair comparison.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── Paths ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = PROJECT_ROOT / "shared"
DATA_DIR = SHARED_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PERSONALITY_DIR = DATA_DIR / "personality"
ARC_SUMMARIES_DIR = DATA_DIR / "arc_summaries"
CHUNKS_DB_DIR = DATA_DIR / "chunks_db"
EVAL_DIR = SHARED_DIR / "eval"
RESULTS_DIR = PROJECT_ROOT / "results"

# ── LLM Provider Switch ──────────────────────────────────────────────
# Set LLM_PROVIDER=openrouter in .env to use OpenRouter instead of Copilot.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "copilot")  # "copilot" | "openrouter"

# ── LLM (GitHub Copilot) ─────────────────────────────────────────────
COPILOT_TOKEN = os.getenv("COPILOT_TOKEN", "")
COPILOT_CHAT_URL = os.getenv(
    "COPILOT_CHAT_URL",
    "https://api.business.githubcopilot.com/chat/completions",
)

# ── LLM (OpenRouter) ─────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

# ── Active models (resolved from provider) ───────────────────────────
if LLM_PROVIDER == "openrouter":
    PRIMARY_MODEL = os.getenv("OPENROUTER_PRIMARY_MODEL", "anthropic/claude-sonnet-4.6")
    JUDGE_MODEL   = os.getenv("OPENROUTER_JUDGE_MODEL",   "openai/gpt-5.4")
else:  # copilot
    PRIMARY_MODEL = os.getenv("COPILOT_PRIMARY_MODEL", "claude-sonnet-4.6")  # 1M input ctx, 64K output
    JUDGE_MODEL   = os.getenv("COPILOT_JUDGE_MODEL",   "gpt-5.4")

TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 1024

# ── Embeddings ─────────────────────────────────────────────────────────
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

# ── Token Budgets (prompt layers) ─────────────────────────────────────
L1_BUDGET = 500    # identity core — never truncated
L2_BUDGET = 300    # speech / behavior rules
L3_BUDGET = 2500   # retrieved context + reasoning scaffold
L4_BUDGET = 400    # session state + recent history

# ── Retrieval ──────────────────────────────────────────────────────────
TOP_K_CHUNKS = 8
TOP_K_EXPERIENCES = 5
TOP_K_ARC_SUMMARIES = 3

# ── Session ────────────────────────────────────────────────────────────
SELF_STATE_UPDATE_INTERVAL = 5   # update every N messages
ROLLING_SUMMARY_INTERVAL = 5
CONVERSATION_WINDOW = 8          # last N message pairs kept in full
