#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI was not found on PATH."
  exit 1
fi

if [[ $# -gt 0 ]]; then
  codex --ask-for-approval never exec resume --last "$*"
else
  codex exec resume --last
fi
