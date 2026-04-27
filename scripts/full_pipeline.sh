#!/bin/bash
set -e

echo "Step 1: Syncing Zotero to Obsidian"
python3 scripts/import_zotero.py

echo "Step 2: Checking papers that need AI digestion"
python3 scripts/paper_digest_status.py

echo "Step 3: Running Codex paper digestion"

codex run codex/commands/process_new_papers.md

echo "Pipeline complete"
