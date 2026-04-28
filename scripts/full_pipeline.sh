#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"

echo "Step 1: Syncing Zotero to Obsidian"
python3 scripts/import_zotero.py

echo "Step 2: Running paper digestion"
bash scripts/digest_papers.sh

echo "Step 3: Running concept linking"
bash scripts/link_concepts.sh

echo "Step 4: Checking vault integrity"
bash scripts/check_vault.sh

echo "Pipeline complete"
