# Link Concepts

Use this command to build and maintain the paper-to-concept graph.

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

<!-- CONCEPT-GENERATED END -->

---

## Notes
- 
```

If a concept file already exists, replace only the `CONCEPT-GENERATED` block and preserve everything outside it.

4. Append non-duplicate links to each paper's `## Connections` section:

```md
## Connections
- [[Concept Name]]
```

If `## Connections` is missing, add it near the end of the file.

## Rules

- Never edit inside `AUTO-GENERATED`.
- Never edit inside `AI-GENERATED`.
- Never delete user-written notes.
- Do not duplicate links.
- Use `[[Concept Name]]` wiki links.
- Prefer fewer, high-signal concepts over noisy tags.
- Do not create vague concepts like `Paper`, `Method`, `System`, `Result`, or `Research`.
