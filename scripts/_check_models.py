from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.config import LLM_PROVIDER, PRIMARY_MODEL, JUDGE_MODEL
print("provider:", LLM_PROVIDER)
print("primary:", PRIMARY_MODEL)
print("judge:", JUDGE_MODEL)
