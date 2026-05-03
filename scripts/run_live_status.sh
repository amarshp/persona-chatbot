#!/usr/bin/env bash
# PersonaRAG Stop-hook launcher — spawns headless Claude (haiku) to
# curate persona-chatbot/results/LIVE_STATUS.md based on the latest
# user→assistant turn. Async-safe; never prints to stdout/stderr to
# avoid being interpreted as a hook directive.

set -u

# --- Recursion guards -------------------------------------------------------
# 1. Env sentinel — survives across nested `claude -p` invocations because
#    bash exports propagate to children. Inner Stop hook re-enters here →
#    sees the sentinel → exits silently.
if [ "${PERSONARAG_LIVE_STATUS_RUNNING:-0}" = "1" ]; then
  exit 0
fi

# 2. Same-session re-entry flag from Claude Code itself.
STDIN_JSON="$(cat || true)"
if printf '%s' "$STDIN_JSON" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

export PERSONARAG_LIVE_STATUS_RUNNING=1

# --- Paths ------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"            # persona-chatbot/
LIVE_STATUS="${LIVE_STATUS_OVERRIDE:-$PROJECT_DIR/results/LIVE_STATUS.md}"
CURATOR_PROMPT="$SCRIPT_DIR/live_status_curator.md"
LOG_FILE="${LIVE_STATUS_LOG_OVERRIDE:-$SCRIPT_DIR/.live_status.log}"
STATE_FILE="${LIVE_STATUS_STATE_OVERRIDE:-$SCRIPT_DIR/.live_status_state.json}"

[ -f "$LIVE_STATUS" ]    || exit 0
[ -f "$CURATOR_PROMPT" ] || exit 0

# --- Pull transcript path from stdin JSON ----------------------------------
TRANSCRIPT="$(printf '%s' "$STDIN_JSON" | python -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get("transcript_path") or "")
except Exception:
    print("")
' 2>/dev/null || true)"

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  # Fallback: newest *.jsonl under sanitized project dir.
  PROJECTS_DIR="$HOME/.claude/projects"
  if [ -d "$PROJECTS_DIR" ]; then
    TRANSCRIPT="$(ls -t "$PROJECTS_DIR"/*PersonaRAG*/*.jsonl 2>/dev/null | head -1 || true)"
  fi
fi

[ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ] || exit 0

# --- Dedup: same final assistant uuid as last run? -------------------------
LAST_UUID=""
if [ -f "$STATE_FILE" ]; then
  LAST_UUID="$(python -c '
import json, sys
try:
    print(json.load(open(r"'"$STATE_FILE"'", "r", encoding="utf-8")).get("last_uuid") or "")
except Exception:
    print("")
' 2>/dev/null || true)"
fi

CUR_UUID="$(python -c '
import json, sys
path = r"'"$TRANSCRIPT"'"
last_asst_uuid = ""
try:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("type") == "assistant":
                content = ev.get("message", {}).get("content")
                has_text = False
                if isinstance(content, list):
                    has_text = any(isinstance(b, dict) and b.get("type") == "text" and b.get("text") for b in content)
                elif isinstance(content, str) and content.strip():
                    has_text = True
                if has_text:
                    last_asst_uuid = ev.get("uuid") or last_asst_uuid
    print(last_asst_uuid)
except Exception:
    print("")
' 2>/dev/null || true)"

if [ -n "$CUR_UUID" ] && [ "$CUR_UUID" = "$LAST_UUID" ]; then
  exit 0
fi

# --- Extract the latest turn (user_msg + asst_text) ------------------------
# Pre-extracting in the launcher means the inner claude does NOT have to
# read the full transcript JSONL — drops cost from ~$0.50/turn to ~$0.05.
TURN_FILE="$SCRIPT_DIR/.live_status_turn.txt"

TRANSCRIPT_FOR_PY="$TRANSCRIPT" python <<'PYEOF' > "$TURN_FILE" 2>/dev/null || true
import json, os, re, sys

path = os.environ.get("TRANSCRIPT_FOR_PY", "")
if not path or not os.path.isfile(path):
    sys.exit(0)

events = []
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except Exception:
            continue

def extract_text_from_content(content):
    """Return concatenated text from a content field (string or block list)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str):
                out.append(b["text"])
        return "".join(out)
    return ""

def is_real_user(ev):
    if ev.get("type") != "user":
        return False
    msg = ev.get("message") or {}
    if msg.get("role") != "user":
        return False
    c = msg.get("content")
    if isinstance(c, str) and c.strip():
        return True
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get("type") == "text" and (b.get("text") or "").strip():
                return True
    return False

# Find the last contiguous run of assistant text events (no real user msg between).
last_run_start = None
last_run_end = None
i = len(events) - 1
# Walk backwards: skip non-assistant tail until we find one with text
while i >= 0 and events[i].get("type") != "assistant":
    i -= 1
if i < 0:
    sys.exit(0)
last_run_end = i
# Walk back through contiguous assistant events
while i >= 0 and events[i].get("type") == "assistant":
    last_run_start = i
    i -= 1
# Now find the last real-user event before last_run_start
user_idx = -1
for j in range(last_run_start - 1, -1, -1):
    if is_real_user(events[j]):
        user_idx = j
        break

user_text = ""
if user_idx >= 0:
    user_text = extract_text_from_content(events[user_idx].get("message", {}).get("content"))

asst_text_parts = []
last_uuid = ""
for ev in events[last_run_start:last_run_end + 1]:
    msg = ev.get("message") or {}
    txt = extract_text_from_content(msg.get("content"))
    if txt:
        asst_text_parts.append(txt)
        last_uuid = ev.get("uuid") or last_uuid

asst_text = "".join(asst_text_parts)

# Strip noise wrappers from BOTH (curator will also strip, this is belt+braces).
NOISE_TAGS = [
    "system-reminder",
    "command-name", "command-message", "command-args",
    "local-command-stdout", "local-command-caveat",
    "user-prompt-submit-hook",
]
for tag in NOISE_TAGS:
    user_text = re.sub(rf"<{tag}>.*?</{tag}>", "", user_text, flags=re.IGNORECASE | re.DOTALL)
    asst_text = re.sub(rf"<{tag}>.*?</{tag}>", "", asst_text, flags=re.IGNORECASE | re.DOTALL)

print("===LIVE_STATUS_TURN===")
print(f"asst_uuid: {last_uuid}")
print("---USER_BEGIN---")
print(user_text.rstrip())
print("---USER_END---")
print("---ASSISTANT_BEGIN---")
print(asst_text.rstrip())
print("---ASSISTANT_END---")
PYEOF

# If extraction failed or file is tiny, bail.
if [ ! -s "$TURN_FILE" ]; then
  exit 0
fi

# --- Build prompt for the inner claude -------------------------------------
read -r -d '' PROMPT_TEXT <<EOF || true
You are the LIVE_STATUS.md auto-curator for the PersonaRAG project. A
Stop hook just fired in the user's main Claude Code session.

Your full instructions are in this file — read it FIRST in entirety:
  $CURATOR_PROMPT

The latest user→assistant turn has ALREADY been extracted for you (so
you don't need to read the raw transcript). It is at:
  $TURN_FILE

That file has this layout:
  ===LIVE_STATUS_TURN===
  asst_uuid: <uuid>
  ---USER_BEGIN---
  <cleaned user message>
  ---USER_END---
  ---ASSISTANT_BEGIN---
  <full assistant text>
  ---ASSISTANT_END---

Steps:
  1. Read $CURATOR_PROMPT (your full ruleset).
  2. Read $TURN_FILE (the user message + assistant text — already
     stripped of system-reminder / command-* wrappers).
  3. Read the tail of $LIVE_STATUS (~120 lines for tone).
  4. Apply the skip/keep rules from the curator file.
  5. Either output SKIP, or use Edit to append a faithful entry to
     $LIVE_STATUS.

DO NOT read the raw session transcript. The turn is already extracted.

Output ONE short line — either "SKIP", "SKIP-error: <reason>", or
"appended <topic>". Nothing else. The output goes to a log file.
EOF

# --- Invoke headless claude ------------------------------------------------
# Use haiku for cost. acceptEdits permission so Edit runs without prompt.
# --add-dir on the projects dir so Read can access the transcript path
# (which sits outside the cwd).
{
  printf '\n[%s] start uuid=%s\n' "$(date -Iseconds 2>/dev/null || date)" "$CUR_UUID"
  claude \
    -p "$PROMPT_TEXT" \
    --model sonnet \
    --allowedTools "Read Edit" \
    --add-dir "$HOME/.claude/projects" \
    --add-dir "$PROJECT_DIR" \
    --max-budget-usd 0.50 \
    --permission-mode acceptEdits \
    --output-format text \
    --no-session-persistence
  rc=$?
  printf '\n[%s] done rc=%s\n' "$(date -Iseconds 2>/dev/null || date)" "$rc"
} >> "$LOG_FILE" 2>&1

# --- Persist dedup state ---------------------------------------------------
if [ -n "$CUR_UUID" ]; then
  TS="$(date -Iseconds 2>/dev/null || date)"
  printf '{"last_uuid":"%s","last_ts":"%s"}\n' "$CUR_UUID" "$TS" > "$STATE_FILE" 2>/dev/null || true
fi

exit 0
