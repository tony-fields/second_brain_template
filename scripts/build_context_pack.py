import os

from vault_utils import (
    BASE_DIR,
    CONCEPTS_PATH,
    NOTES_PATH,
    PAPERS_PATH,
    SYSTEM_PATH,
    append_log,
    inspect_concept,
    inspect_paper,
    iter_concepts,
    iter_papers,
    read_text,
    relpath,
    section_body,
    write_text,
)


MAX_SECTION_CHARS = 1200


def trim(text, limit=MAX_SECTION_CHARS):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def iter_notes():
    if not os.path.isdir(NOTES_PATH):
        return
    for name in sorted(os.listdir(NOTES_PATH)):
        if name.startswith(".") or not name.endswith(".md"):
            continue
        yield os.path.join(NOTES_PATH, name)


def note_title(text, fallback):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_paper_entry(path):
    text = read_text(path)
    info = inspect_paper(path)
    parts = [
        f"### {info['citekey']}",
        f"- Path: {info['path']}",
        f"- Title: {info['title']}",
        f"- Digest status: {info['digest_status']}",
        f"- AI status: {info['ai_status'] or 'missing'}",
    ]
    summary = section_body(text, "Digest Summary") or section_body(text, "Summary")
    concepts = section_body(text, "Candidate Concepts")
    connections = section_body(text, "Connections")
    if summary:
        parts.append(f"- Summary: {trim(summary)}")
    if concepts:
        parts.append(f"- Candidate concepts: {trim(concepts, 600)}")
    if connections:
        parts.append(f"- Connections: {trim(connections, 600)}")
    return "\n".join(parts)


def build_concept_entry(path):
    text = read_text(path)
    info = inspect_concept(path)
    parts = [
        f"### {info['name']}",
        f"- Path: {info['path']}",
        f"- Title: {info['title']}",
    ]
    definition = section_body(text, "Definition")
    related_papers = section_body(text, "Related Papers")
    related_concepts = section_body(text, "Related Concepts")
    if definition:
        parts.append(f"- Definition: {trim(definition)}")
    if related_papers:
        parts.append(f"- Related papers: {trim(related_papers, 600)}")
    if related_concepts:
        parts.append(f"- Related concepts: {trim(related_concepts, 600)}")
    return "\n".join(parts)


def build_note_entry(path):
    text = read_text(path)
    title = note_title(text, os.path.splitext(os.path.basename(path))[0])
    return "\n".join(
        [
            f"### {title}",
            f"- Path: {relpath(path)}",
            f"- Preview: {trim(text, 1000)}",
        ]
    )


def main():
    os.makedirs(SYSTEM_PATH, exist_ok=True)
    paper_paths = list(iter_papers())
    concept_paths = list(iter_concepts())
    note_paths = list(iter_notes())

    lines = [
        "# Vault Context Pack",
        "",
        "This file is generated. It is a compact map of the vault for Codex runs.",
        "",
        "## Counts",
        f"- Papers: {len(paper_paths)}",
        f"- Concepts: {len(concept_paths)}",
        f"- Notes: {len(note_paths)}",
        "",
        "## Papers",
    ]

    if paper_paths:
        lines.extend(build_paper_entry(path) for path in paper_paths)
    else:
        lines.append("- No paper notes found.")

    lines.extend(["", "## Concepts"])
    if concept_paths:
        lines.extend(build_concept_entry(path) for path in concept_paths)
    else:
        lines.append("- No concept notes found.")

    lines.extend(["", "## Notes"])
    if note_paths:
        lines.extend(build_note_entry(path) for path in note_paths)
    else:
        lines.append("- No notes found.")

    output_path = os.path.join(SYSTEM_PATH, "context_pack.md")
    write_text(output_path, "\n\n".join(lines) + "\n")
    append_log(
        "context_pack_built",
        papers=len(paper_paths),
        concepts=len(concept_paths),
        notes=len(note_paths),
    )
    print(f"Wrote {os.path.relpath(output_path, BASE_DIR)}")


if __name__ == "__main__":
    main()
