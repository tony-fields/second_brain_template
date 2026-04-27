#!/bin/bash

echo "🔄 Step 1: Syncing Zotero → Obsidian"
python3 scripts/import_zotero_sync.py

echo "🤖 Step 2: Running Codex full update"

# Option A: if using Codex CLI
codex run codex/commands/full_update.md

# Option B (fallback): open instructions
# echo "Run Codex with: codex/commands/full_update.md"

echo "✅ Pipeline complete"
