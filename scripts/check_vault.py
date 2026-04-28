import os
import sys

from vault_utils import (
    AI_END,
    AI_START,
    AUTO_END,
    AUTO_START,
    CONCEPTS_PATH,
    CONCEPT_END,
    CONCEPT_START,
    GRAPH_END,
    GRAPH_START,
    PAPERS_PATH,
    VALID_AI_STATUSES,
    WIKI_LINK_RE,
    block_between,
    extract,
    iter_concepts,
    iter_papers,
    paper_citekey,
    read_text,
    rebuild_manifests,
    section_links,
    wiki_links,
    AUTO_HASH_RE,
    AI_HASH_RE,
    AI_STATUS_RE,
)


def issue(issues, severity, path, message):
    issues.append((severity, path, message))


def target_exists(link, paper_names, concept_names):
    return link in paper_names or link in concept_names


def main():
    issues = []
    paper_paths = list(iter_papers())
    concept_paths = list(iter_concepts())
    paper_names = {paper_citekey(path) for path in paper_paths}
    concept_names = {os.path.splitext(os.path.basename(path))[0] for path in concept_paths}

    for path in paper_paths:
        rel = os.path.relpath(path)
        text = read_text(path)

        if AUTO_START not in text or AUTO_END not in text:
            issue(issues, "error", rel, "missing AUTO-GENERATED markers")
        if AI_START not in text or AI_END not in text:
            issue(issues, "error", rel, "missing AI-GENERATED markers")

        auto_hash = extract(AUTO_HASH_RE, text)
        ai_hash = extract(AI_HASH_RE, text)
        ai_status = extract(AI_STATUS_RE, text)

        if not auto_hash:
            issue(issues, "error", rel, "missing source HASH")
        if not ai_hash:
            issue(issues, "warning", rel, "missing AI-SOURCE-HASH")
        elif ai_hash.startswith("pending:"):
            issue(issues, "warning", rel, "AI digest is pending")
        elif auto_hash and ai_hash != auto_hash and ai_status not in {"needs-source", "failed", "review-needed"}:
            issue(issues, "warning", rel, "AI-SOURCE-HASH does not match source HASH")

        if ai_status and ai_status not in VALID_AI_STATUSES:
            issue(issues, "warning", rel, f"unknown AI-STATUS: {ai_status}")

        links = section_links(text, "Connections")
        duplicate_links = sorted({link for link in links if links.count(link) > 1})
        for link in duplicate_links:
            issue(issues, "warning", rel, f"duplicate Connections link: [[{link}]]")

        for link in wiki_links(text):
            if link.strip() and not target_exists(link, paper_names, concept_names):
                issue(issues, "warning", rel, f"broken wiki link: [[{link}]]")

    for path in concept_paths:
        rel = os.path.relpath(path)
        text = read_text(path)
        name = os.path.splitext(os.path.basename(path))[0]

        if name == "Concept Graph":
            if GRAPH_START not in text or GRAPH_END not in text:
                issue(issues, "warning", rel, "missing GRAPH-GENERATED markers")
        elif CONCEPT_START not in text or CONCEPT_END not in text:
            issue(issues, "warning", rel, "missing CONCEPT-GENERATED markers")

        related_papers = section_links(text, "Related Papers")
        for paper in related_papers:
            if paper not in paper_names:
                issue(issues, "warning", rel, f"related paper does not exist: [[{paper}]]")

        for link in wiki_links(text):
            if link.strip() and not target_exists(link, paper_names, concept_names):
                issue(issues, "warning", rel, f"broken wiki link: [[{link}]]")

    if not os.path.isdir(PAPERS_PATH):
        issue(issues, "error", "papers/", "missing papers directory")
    if not os.path.isdir(CONCEPTS_PATH):
        issue(issues, "error", "concepts/", "missing concepts directory")

    papers, _ = rebuild_manifests()

    print(f"Papers checked: {len(papers)}")
    if papers:
        print("Papers:")
        for paper in papers:
            print(
                f"- {paper['citekey']} | {paper['digest_status']} | "
                f"{paper['title']} | {paper['path']}"
            )
    else:
        print("Papers: none")
    print("")

    if not issues:
        print("Vault check passed.")
        return 0

    for severity, path, message in issues:
        print(f"{severity.upper()}: {path}: {message}")

    return 1 if any(severity == "error" for severity, _, _ in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
