# Full Update

Run the complete research-vault update workflow.

## Steps

1. Sync Zotero export into paper notes:

```bash
python3 scripts/import_zotero.py
```

2. Digest new or stale papers by following `codex/commands/process_new_papers.md`.

3. Build or refresh concept files and paper links by following `codex/commands/link_concepts.md`.

4. Validate the vault:

```bash
bash scripts/check_vault.sh
```

## Safety

- Zotero sync owns only `AUTO-GENERATED`.
- AI digestion owns only `AI-GENERATED`.
- Concept linking may update `CONCEPT-GENERATED` blocks in `concepts/` and append non-duplicate links to paper `Connections`.
- Validation is read-only except for rebuilding `.system/` manifests.
- Do not delete user-written content.
