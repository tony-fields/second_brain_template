# Link Concepts

Use this command to build and maintain the Obsidian paper-to-concept graph.

## Workflow

1. Scan all Markdown files in `papers/`.

2. For each paper, identify important concepts using these sources in order:
   - `## Candidate Concepts` inside `AI-GENERATED`
   - `## Digest Summary`
   - `## Key Contributions`
   - `## Core Ideas / Intuition`
   - Zotero `## Summary` and `## Highlights` inside `AUTO-GENERATED`
   - existing `## Connections`

3. Create or update concept files in `concepts/`.

Use this format:

```md
# Concept Name

<!-- CONCEPT-GENERATED START -->

## Definition
- Concise definition grounded in the paper notes.

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

If a concept file already exists, replace only the `CONCEPT-GENERATED` block and preserve everything outside it.

4. Create graph edges with real wiki links.

Obsidian's graph is built from Markdown links, so every relationship must be represented as a `[[Wiki Link]]`.

Create these edges:

- Paper -> concept: append links to each paper's `## Connections` section.
- Concept -> paper: list paper links in each concept's `## Related Papers` section.
- Concept -> concept: list high-confidence concept links in each concept's `## Related Concepts` section.

Paper links should look like:

```md
## Connections
- [[Concept Name]]
```

If `## Connections` is missing, add it near the end of the file.

5. Maintain `concepts/Concept Graph.md` as an index note:

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

If `concepts/Concept Graph.md` already exists, replace only the `GRAPH-GENERATED` block and preserve everything outside it.

## Rules

- Never edit inside `AUTO-GENERATED`.
- Never edit inside `AI-GENERATED`.
- Never delete user-written notes.
- Do not duplicate links.
- Use `[[Concept Name]]` wiki links.
- Make graph links bidirectional where useful.
- Prefer fewer, high-signal concepts over noisy tags.
- Do not create vague concepts like `Paper`, `Method`, `System`, `Result`, or `Research`.
