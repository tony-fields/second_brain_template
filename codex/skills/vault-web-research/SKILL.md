---
name: vault-web-research
description: Load the Obsidian research vault into working context, then use web search when needed to compare vault knowledge with current external sources while preserving clear source boundaries.
---

# Vault Web Research

Use this skill when the user asks a question that should combine the local vault with current internet information.

## Core Contract

- Treat the vault as the user's private research context.
- Treat web results as external evidence.
- Clearly separate "From the vault" from "From the web".
- Prefer official or primary sources when searching.
- Do not write external claims into vault notes unless the user asks.
- Do not modify files unless the user explicitly asks.

## Workflow

1. Build or refresh the context pack:

```bash
python3 scripts/build_context_pack.py
```

2. Read `.system/context_pack.md` first.

3. Open relevant files from `papers/`, `concepts/`, and `notes/` when the context pack points to them.

4. Use web search for current information, missing context, source verification, or external comparison.

5. Answer with source boundaries:

```md
## From The Vault

## From The Web

## Synthesis

## Sources
```

## Rules

- Never imply a web claim came from the vault.
- Never imply a vault claim is current external consensus unless verified.
- Cite paper citekeys and concept links for vault evidence.
- Provide web source links for external evidence.
- If the vault and web disagree, say so directly.
