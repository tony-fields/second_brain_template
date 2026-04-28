# Vault Web Research

Answer the user's question using both this vault and web search.

Question:

{{query}}

## Instructions

1. Run:

```bash
python3 scripts/build_context_pack.py
```

2. Read `.system/context_pack.md`.

3. Open relevant files from `papers/`, `concepts/`, and `notes/` as needed.

4. Use web search for current or external information.

5. Keep source boundaries clear:

```md
## From The Vault

## From The Web

## Synthesis

## Sources
```

## Rules

- Use only vault files for vault claims.
- Use web citations for web claims.
- Cite local paper notes with `[[citekey]]`.
- Link local concepts with `[[Concept Name]]`.
- Do not modify files unless the user explicitly asks.
