# Full Update

Run the complete research-vault update workflow.

## Steps

1. Sync Zotero export into paper notes:

```bash
python3 scripts/import_zotero.py
```

2. Digest new or stale papers by following `codex/commands/process_new_papers.md`.

3. Build or refresh concept files by following `codex/commands/build_concepts.md`.

4. Link papers to concepts by following `codex/commands/link_concepts.md`.

## Safety

- Zotero sync owns only `AUTO-GENERATED`.
- AI digestion owns only `AI-GENERATED`.
- Concept linking may append non-duplicate links to `Connections`.
- Do not delete user-written content.
