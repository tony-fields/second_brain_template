---
name: literature-review
description: Create literature review notes from the vault for a topic, concept, or research question, using paper citekeys, concept links, themes, disagreements, timelines, gaps, and open problems.
---

# Literature Review

Use this skill when the user asks for a literature review, research overview, state of the field, topic synthesis, or review note based on the vault.

## Workflow

1. Identify relevant papers in `papers/` and concepts in `concepts/`.
2. Use `AI-GENERATED` digests first, then manual notes, then Zotero summaries/highlights.
3. Create or update a review note in `notes/` when requested by a command script.
4. Preserve existing user-written sections outside generated markers.

## Review Note Format

```md
# Literature Review: Topic

<!-- LIT-REVIEW-GENERATED START -->

## Overview

## Main Approaches

## Key Papers
- [[citekey]]

## Timeline Of Ideas

## Agreements

## Disagreements

## Open Problems

## Related Concepts
- [[Concept Name]]

## Suggested Next Reading
- [[citekey]]

<!-- LIT-REVIEW-GENERATED END -->

---

## Notes
- 
```

## Rules

- Use only information present in the vault.
- Cite specific papers by citekey.
- Link relevant concepts.
- If updating an existing review note, replace only `LIT-REVIEW-GENERATED`.
- If evidence is thin, say so explicitly.
