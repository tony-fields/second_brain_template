---
name: paper-digestion
description: Digest Zotero-imported Obsidian paper notes by writing summaries, contributions, core ideas, details, and candidate concept links only for papers whose AUTO-GENERATED source hash is new or changed.
---

# Paper Digestion

Use this skill when the user asks an agent to digest imported papers, summarize all papers for the first time, or process newly added papers in this Obsidian research vault.

## Core Contract

- Zotero sync owns `AUTO-GENERATED`.
- This skill owns `AI-GENERATED`.
- User notes outside those markers must be preserved.
- A paper is already digested when `AI-SOURCE-HASH` equals the current `HASH` in `AUTO-GENERATED`.

## Workflow

1. Run:

```bash
python3 scripts/paper_digest_status.py
```

2. For each listed paper, read the note and extract:
- title
- citekey
- `<!-- HASH: ... -->`
- `Summary`
- `Highlights`
- metadata useful for context

3. Replace only the `AI-GENERATED` block with:

```md
<!-- AI-GENERATED START -->

<!-- AI-SOURCE-HASH: <current AUTO hash> -->
<!-- AI-STATUS: complete -->

## Digest Summary
- ...

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

4. If the paper does not contain enough source material to summarize, use `AI-STATUS: needs-source` and write a short note inside the AI block explaining what is missing.

5. Run `python3 scripts/paper_digest_status.py` again. The expected result is no stale papers except those intentionally marked `needs-source`.

## Writing Guidelines

- Use only facts present in the note.
- Keep summaries concise, technical, and useful for later concept-linking.
- Prefer 3-6 bullets for contributions and core ideas.
- Candidate concepts should use Obsidian wiki links, for example `[[Blind Signatures]]`.
- Do not add duplicate links.
