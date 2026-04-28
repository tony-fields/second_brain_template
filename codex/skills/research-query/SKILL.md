---
name: research-query
description: Answer research questions using only the Obsidian vault, citing paper citekeys and concept notes while synthesizing evidence, disagreements, gaps, and next reading steps.
---

# Research Query

Use this skill when the user asks a question about the research vault, wants synthesis across papers, or wants to know what the notes say about a topic.

## Workflow

1. Read relevant files from `papers/`, `concepts/`, and `notes/`.
2. Prefer digested material in `AI-GENERATED`, then user notes, then Zotero summaries/highlights.
3. Answer using only information present in the vault.
4. Cite paper notes using citekeys, for example `[[smith2024example]]`.
5. Link relevant concepts with `[[Concept Name]]`.

## Answer Shape

Use this structure when useful:

```md
## Answer

## Evidence
- [[citekey]]: ...

## Connections
- [[Concept Name]] relates because ...

## Disagreements Or Gaps
- ...

## Suggested Next Reading
- [[citekey]]
```

## Rules

- Do not hallucinate missing details.
- Say when the vault does not contain enough evidence.
- Prefer synthesis over listing.
- Do not modify files unless the user explicitly asks.
