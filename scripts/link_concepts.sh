#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"

if ! find papers -maxdepth 1 -type f -name "*.md" | grep -q .; then
  echo "No paper notes found in papers/."
  echo "Run: python3 scripts/import_zotero.py"
  exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH."
  echo "Run this from a terminal where 'codex' works, or configure Obsidian to use that shell environment."
  exit 1
fi

echo "Running Codex concept linking"
codex --ask-for-approval never exec \
  --cd "$REPO_DIR" \
  --sandbox workspace-write \
  - < codex/commands/link_concepts.md

echo "Concept linking complete"
