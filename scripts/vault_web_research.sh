#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/vault_web_research.sh \"question\""
  exit 1
fi

cd "$REPO_DIR"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH."
  exit 1
fi

query="$*"
prompt="$(QUERY="$query" python3 -c 'import os; print(open("codex/commands/vault_web_research.md", encoding="utf-8").read().replace("{{query}}", os.environ["QUERY"]))')"

python3 scripts/build_context_pack.py

codex --search --ask-for-approval never exec \
  --cd "$REPO_DIR" \
  --sandbox workspace-write \
  "$prompt"
