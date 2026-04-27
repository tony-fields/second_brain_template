#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"

echo "Checking papers that need AI digestion"
status_output="$(python3 scripts/paper_digest_status.py)"
echo "$status_output"

if [[ "$status_output" == "No papers need AI digestion." ]]; then
  echo "Nothing for Codex to digest."
  exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH."
  echo "Run this from a terminal where 'codex' works, or configure Obsidian to use that shell environment."
  exit 1
fi

echo "Running Codex paper digestion"
codex exec \
  --cd "$REPO_DIR" \
  --sandbox workspace-write \
  --ask-for-approval never \
  - < codex/commands/process_new_papers.md

echo "Rechecking digestion status"
python3 scripts/paper_digest_status.py
