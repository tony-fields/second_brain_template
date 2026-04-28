#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/research_query.sh \"question\""
  exit 1
fi

cd "$REPO_DIR"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH."
  exit 1
fi

question="$*"
prompt="$(QUERY="$question" python3 -c 'import os; print(open("codex/commands/research_query.md", encoding="utf-8").read().replace("{{query}}", os.environ["QUERY"]))')"

codex --ask-for-approval never exec \
  --cd "$REPO_DIR" \
  --sandbox workspace-write \
  "$prompt"
