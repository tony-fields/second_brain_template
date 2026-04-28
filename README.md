SECOND BRAIN TEMPLATE
=====================

An Obsidian vault template for building an AI-assisted research system.

This project connects:

  Zotero / Better BibTeX
        -> Python import scripts
        -> Obsidian paper notes
        -> Codex skills and command prompts
        -> AI-generated summaries, concepts, graph links, and research notes

The goal is to make a portable "programmable research vault" that can be
cloned, reused, and extended without hardcoding local machine paths.


PROJECT STRUCTURE
=================

  zotero-export/
    Put your Better BibTeX JSON export here as:

      zotero-export/library.json

  papers/
    Imported paper notes live here. These are created from Zotero citekeys.

  concepts/
    Concept notes and the generated graph index live here.

  notes/
    Literature reviews, synthesis notes, and other higher-level notes live here.

  daily/
    Daily notes, if you use them.

  inbox/
    Scratch capture area.

  scripts/
    Command-line automation for import, digestion, validation, repair, and
    research workflows.

  codex/commands/
    Prompt files used by command-line Codex workflows.

  codex/skills/
    Repo-local skill instructions that tell Codex how to work safely inside
    this vault.

  .system/
    Generated machine-readable manifests and logs. The folder is kept in git,
    but generated JSON/JSONL files are ignored.


REQUIREMENTS
============

You need:

  - Python 3
  - Obsidian
  - Zotero with Better BibTeX export
  - Codex CLI installed and authenticated

The scripts are designed to be run from the repository root:

  bash scripts/full_pipeline.sh

They also resolve the repository path internally, so they are portable across
different clone locations.


FIRST RUN
=========

1. Export your Zotero library using Better BibTeX.

2. Save the export as:

     zotero-export/library.json

3. Import Zotero papers into Obsidian notes:

     python3 scripts/import_zotero.py

4. See which papers need AI digestion:

     python3 scripts/paper_digest_status.py

5. Run AI digestion:

     bash scripts/digest_papers.sh

6. Build concept notes and graph links:

     bash scripts/link_concepts.sh

7. Validate the vault:

     bash scripts/check_vault.sh

Or run the complete pipeline:

     bash scripts/full_pipeline.sh


CORE WORKFLOWS
==============

Import Zotero Data
------------------

  python3 scripts/import_zotero.py

Reads Better BibTeX JSON from zotero-export/library.json and creates or updates
paper notes in papers/.

The import script owns only this block:

  <!-- AUTO-GENERATED START -->
  ...
  <!-- AUTO-GENERATED END -->

It also creates an AI placeholder block for later digestion.


Digest Papers
-------------

  bash scripts/digest_papers.sh

Runs Codex on papers that need summaries.

The paper digestion agent owns only this block:

  <!-- AI-GENERATED START -->
  ...
  <!-- AI-GENERATED END -->

Papers are processed incrementally. A paper only needs digestion when its
AI-SOURCE-HASH does not match the current Zotero HASH.


Link Concepts
-------------

  bash scripts/link_concepts.sh

Runs Codex to:

  - scan paper notes
  - identify important concepts
  - create/update concept notes in concepts/
  - append non-duplicate concept links to paper Connections sections
  - add backlinks from concepts to papers
  - add concept-to-concept links
  - maintain concepts/Concept Graph.md

Concept linking owns:

  <!-- CONCEPT-GENERATED START -->
  ...
  <!-- CONCEPT-GENERATED END -->

The graph index owns:

  <!-- GRAPH-GENERATED START -->
  ...
  <!-- GRAPH-GENERATED END -->


Validate Vault
--------------

  bash scripts/check_vault.sh

Checks for:

  - missing generated markers
  - stale AI hashes
  - invalid AI statuses
  - duplicate links
  - broken wiki links
  - missing concept graph markers

This also rebuilds local .system manifests.


Repair Vault
------------

  bash scripts/repair_vault.sh

Performs safe mechanical repairs:

  - add missing AI placeholders
  - add missing Connections sections
  - deduplicate Connections links
  - create missing concept stubs
  - rebuild concepts/Concept Graph.md
  - rebuild .system manifests

It should not rewrite your hand-written notes.


Research Query
--------------

  bash scripts/research_query.sh "What does the vault say about blind signatures?"

Asks Codex to answer using only the vault. It should cite paper citekeys and
link concepts.


Literature Review
-----------------

  bash scripts/literature_review.sh "blind signatures"

Asks Codex to create or update:

  notes/lit-review-blind-signatures.md

The literature review agent owns only:

  <!-- LIT-REVIEW-GENERATED START -->
  ...
  <!-- LIT-REVIEW-GENERATED END -->


CODEX SKILLS
============

paper-digestion
---------------

Path:

  codex/skills/paper-digestion/SKILL.md

Purpose:

  Digest Zotero-imported paper notes by writing summaries, contributions,
  core ideas, important details, and candidate concept links.

Owned block:

  AI-GENERATED

Useful command:

  bash scripts/digest_papers.sh


concept-linking
---------------

Path:

  codex/skills/concept-linking/SKILL.md

Purpose:

  Build and maintain the Obsidian concept graph by linking papers, concepts,
  and related concepts.

Owned blocks:

  CONCEPT-GENERATED
  GRAPH-GENERATED

Useful command:

  bash scripts/link_concepts.sh


research-query
--------------

Path:

  codex/skills/research-query/SKILL.md

Purpose:

  Answer research questions using only the vault, citing citekeys and linking
  concepts.

Useful command:

  bash scripts/research_query.sh "your question"


literature-review
-----------------

Path:

  codex/skills/literature-review/SKILL.md

Purpose:

  Create literature review notes from the vault for a topic, concept, or
  research question.

Owned block:

  LIT-REVIEW-GENERATED

Useful command:

  bash scripts/literature_review.sh "your topic"


CODEX COMMAND FILES
===================

  codex/commands/full_update.md
    Full update workflow prompt.

  codex/commands/process_new_papers.md
    Paper digestion prompt.

  codex/commands/link_concepts.md
    Concept graph prompt.

  codex/commands/research_query.md
    Research question prompt.

  codex/commands/literature_review.md
    Literature review prompt.

  codex/commands/query_brain.md
    Older query prompt kept for compatibility.

  codex/commands/summarize_papers.md
    Read-only paper summary prompt.

  codex/commands/build_concepts.md
    Older concept-building prompt kept for compatibility.


SAFETY MODEL
============

The vault is designed around ownership boundaries.

  AUTO-GENERATED
    Owned by the Zotero import script.

  AI-GENERATED
    Owned by the paper digestion skill.

  CONCEPT-GENERATED
    Owned by the concept-linking skill inside concept notes.

  GRAPH-GENERATED
    Owned by the concept-linking skill inside concepts/Concept Graph.md.

  LIT-REVIEW-GENERATED
    Owned by the literature-review skill.

Everything outside those generated blocks is treated as user-written and should
be preserved.


AI STATUSES
===========

Paper digestion uses these statuses:

  pending
    The paper has not been digested yet.

  complete
    The paper digest matches the current Zotero source hash.

  needs-source
    The paper lacks enough abstract/highlight content to digest safely.

  failed
    The agent or tool failed while processing the paper.

  review-needed
    The digest was created, but the source was ambiguous and needs human review.


MANIFESTS AND LOGS
==================

Generated local state lives in .system/:

  .system/papers.json
  .system/concepts.json
  .system/pipeline_log.jsonl

These files are ignored by git. They can be rebuilt with:

  bash scripts/check_vault.sh

or:

  bash scripts/repair_vault.sh


OBSIDIAN COMMANDS
=================

If you use an Obsidian shell-command plugin, add commands like:

  bash scripts/full_pipeline.sh

  bash scripts/digest_papers.sh

  bash scripts/link_concepts.sh

  bash scripts/check_vault.sh

  bash scripts/repair_vault.sh

  bash scripts/research_query.sh "your question"

  bash scripts/literature_review.sh "your topic"

If your plugin does not run commands from the vault root, configure its working
directory to the vault root or prefix the command with a relative cd.


TEMPLATE NOTES
==============

This repository is intended to be safe to clone and reuse.

Recommended template workflow:

  1. Clone the repo.
  2. Add zotero-export/library.json.
  3. Run bash scripts/full_pipeline.sh.
  4. Open the vault in Obsidian.
  5. Run bash scripts/check_vault.sh before committing major changes.

Generated manifests and logs are local state. Paper notes, concept notes, and
human-authored notes are the important long-term artifacts.


TROUBLESHOOTING
===============

No papers were imported
-----------------------

Check that your Better BibTeX export exists:

  zotero-export/library.json

Then run:

  python3 scripts/import_zotero.py


Codex command fails
-------------------

Make sure the Codex CLI is installed and authenticated:

  codex --help

Then try a workflow script again:

  bash scripts/digest_papers.sh


Vault looks inconsistent
------------------------

Run:

  bash scripts/check_vault.sh

Then:

  bash scripts/repair_vault.sh


Publishing To GitHub
====================

Before publishing:

  - remove private Zotero exports from zotero-export/
  - remove private paper notes if needed
  - keep .system/*.json and .system/*.jsonl ignored
  - run bash scripts/check_vault.sh
  - verify .gitignore excludes local generated files

This project is a template. Your real research data can live in a private fork
or separate vault.
