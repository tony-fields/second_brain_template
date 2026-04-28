#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/literature_review.sh \"topic\""
  exit 1
fi

cd "$REPO_DIR"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH."
  exit 1
fi

topic="$*"
slug="$(printf "%s" "$topic" | tr "[:upper:]" "[:lower:]" | sed -E "s/[^a-z0-9]+/-/g; s/^-+//; s/-+$//")"
prompt="$(TOPIC="$topic" SLUG="$slug" python3 -c 'import os; text=open("codex/commands/literature_review.md", encoding="utf-8").read(); print(text.replace("{{topic}}", os.environ["TOPIC"]).replace("{{slug}}", os.environ["SLUG"]))')"

codex --ask-for-approval never exec \
  --cd "$REPO_DIR" \
  --sandbox workspace-write \
  "$prompt"
