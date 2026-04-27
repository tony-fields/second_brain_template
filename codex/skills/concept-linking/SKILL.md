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
- Maintain `concepts/Concept Graph.md` as an Obsidian graph index.
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

## Related Concepts
- [[Related Concept]]

<!-- CONCEPT-GENERATED END -->

---

## Notes
- 
```

If a concept file already exists, replace only the `CONCEPT-GENERATED` block. Preserve all content outside it.

## Graph Links

Obsidian graph edges come from wiki links. The skill must create real links in Markdown, not just prose.

Create three kinds of graph links:

1. Paper -> concept links in each paper's `## Connections` section.
2. Concept -> paper links in each concept's `## Related Papers` section.
3. Concept -> concept links in each concept's `## Related Concepts` section when concepts are clearly related.

Also maintain a graph index at `concepts/Concept Graph.md`:

```md
# Concept Graph

<!-- GRAPH-GENERATED START -->

## Concepts
- [[Concept Name]]

## Paper Links
- [[citekey]] -> [[Concept Name]]

## Concept Links
- [[Concept A]] -> [[Concept B]]

<!-- GRAPH-GENERATED END -->
```

If the graph index already exists, replace only the `GRAPH-GENERATED` block.

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
- Make links bidirectional where useful: papers link to concepts, concepts link back to papers.
- Do not create vague concepts like `Paper`, `Method`, `System`, `Result`, or `Research`.
- Prefer fewer, high-signal concepts over noisy tags.
- Base every link on evidence in the paper note.
- Do not duplicate existing links.
