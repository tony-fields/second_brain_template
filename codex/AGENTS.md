# Codex Rules for Second Brain

## Safety Rules
- NEVER overwrite content outside the generated block owned by the current task
- NEVER delete user-written notes
- ALWAYS preserve:
  - Notes
  - Connections
  - Open Questions
- Treat AUTO-GENERATED as Zotero-owned
- Treat AI-GENERATED as agent-owned
- Treat CONCEPT-GENERATED as concept-linking-owned
- Treat GRAPH-GENERATED as concept-graph-index-owned
- Treat LIT-REVIEW-GENERATED as literature-review-owned

## File Rules
- Papers are stored in: papers/
- Concepts are stored in: concepts/
- Literature reviews are stored in: notes/
- Machine-readable manifests are stored in: .system/
- Use citekeys as identifiers

## Editing Rules
- Paper digestion should only modify the AI-GENERATED block
- Concept linking may modify CONCEPT-GENERATED blocks in concepts/
- Concept linking may modify GRAPH-GENERATED in concepts/Concept Graph.md
- Concept linking may modify Connections in papers/ (append only)
- Literature review generation may modify LIT-REVIEW-GENERATED blocks in notes/
- Prefer adding, not replacing

## Linking Rules
- Use [[Concept]] style links
- Do not duplicate content across files
- Prefer bidirectional graph links: papers to concepts, concepts back to papers, and concepts to related concepts

## Behavior
- Be concise
- Do not hallucinate missing content
- Only use information present in the vault
- Run validation with `bash scripts/check_vault.sh` after pipeline-level changes
