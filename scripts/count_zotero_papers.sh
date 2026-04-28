#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"
python3 scripts/count_zotero_papers.py "$@"
