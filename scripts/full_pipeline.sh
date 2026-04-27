#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"

echo "Step 1: Syncing Zotero to Obsidian"
python3 scripts/import_zotero.py

echo "Step 2: Running paper digestion"
bash scripts/digest_papers.sh

echo "Pipeline complete"
