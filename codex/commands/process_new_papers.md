# Process New Papers

Use this command to digest papers for the first time and to refresh papers whose Zotero source data changed.

## Workflow

1. Run:

```bash
python3 scripts/paper_digest_status.py
```

2. For each listed paper, read only the paper note and use the content inside `AUTO-GENERATED` as source material.

3. Replace or create only this section:

```md
<!-- AI-GENERATED START -->

<!-- AI-SOURCE-HASH: <current AUTO hash> -->
<!-- AI-STATUS: complete -->

## Digest Summary
- 2-4 sentence technical summary.

## Key Contributions
- ...

## Core Ideas / Intuition
- ...

## Important Details
- ...

## Candidate Concepts
- [[Concept Name]]

<!-- AI-GENERATED END -->
```

4. After editing, run:

```bash
python3 scripts/paper_digest_status.py
```

The command should report no papers needing AI digestion unless some papers lack usable source metadata.

## Rules

- Never edit inside `AUTO-GENERATED`.
- Never overwrite user-written `Notes`, `Open Questions`, or existing manual sections.
- The AI block may be replaced when the source hash changes.
- Use only information present in the paper note.
- Be concise and technical.
- If the note has no abstract and no highlights, mark `AI-STATUS: needs-source` and explain what is missing inside the AI block.
- If digestion fails, mark `AI-STATUS: failed` and include a short reason inside the AI block.
- If the digest is uncertain and needs human review, mark `AI-STATUS: review-needed`.
