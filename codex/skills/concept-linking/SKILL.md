---
name: concept-linking
description: Build and maintain an Obsidian concept graph by scanning imported paper notes, creating or updating concept notes, and appending non-duplicate wiki links between papers and concepts without overwriting user notes.
---

# Concept Linking

Use this skill when the user asks an agent to look through the vault, identify concepts, create concept pages, or link papers to concepts.

## Core Contract

- Read paper notes in `papers/`.
- Create and update concept notes in `concepts/`.
- Append paper-to-concept links only in each paper's `## Connections` section.
- Never delete user-written notes.
- Never edit inside `AUTO-GENERATED`.
- Never edit inside `AI-GENERATED` during concept linking.

## Sources To Use

Prefer these paper sections in order:

1. `## Candidate Concepts` inside `AI-GENERATED`
2. `## Digest Summary`
3. `## Key Contributions`
4. `## Core Ideas / Intuition`
5. Zotero `## Summary` and `## Highlights` inside `AUTO-GENERATED`
6. Existing manual `## Connections`

## Concept Notes

Each concept note should use this shape:

```md
# Concept Name

<!-- CONCEPT-GENERATED START -->

## Definition
- ...

## Key Ideas
- ...

## Related Papers
- [[citekey]]

<!-- CONCEPT-GENERATED END -->

---

## Notes
- 
```

If a concept file already exists, replace only the `CONCEPT-GENERATED` block. Preserve all content outside it.

## Paper Links

In each relevant paper note, append non-duplicate links under:

```md
## Connections
- [[Concept Name]]
```

If `## Connections` is missing, add it near the end of the file.

## Rules

- Use title case for concept note names.
- Use wiki links: `[[Concept Name]]`.
- Do not create vague concepts like `Paper`, `Method`, `System`, `Result`, or `Research`.
- Prefer fewer, high-signal concepts over noisy tags.
- Base every link on evidence in the paper note.
- Do not duplicate existing links.
