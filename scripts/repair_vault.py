import os

from vault_utils import (
    AI_END,
    AI_START,
    AUTO_HASH_RE,
    CONCEPTS_PATH,
    GRAPH_END,
    GRAPH_START,
    concept_stub,
    dedupe_connection_links,
    ensure_ai_block,
    ensure_connections_section,
    iter_concepts,
    iter_papers,
    paper_citekey,
    read_text,
    rebuild_manifests,
    relpath,
    section_links,
    slug_filename,
    wiki_links,
    write_text,
    extract,
)


def repair_paper(path):
    text = read_text(path)
    original = text
    auto_hash = extract(AUTO_HASH_RE, text)
    if auto_hash:
        text = ensure_ai_block(text, auto_hash)
    text = ensure_connections_section(text)
    text = dedupe_connection_links(text)
    if text != original:
        write_text(path, text)
        return True
    return False


def ensure_concept_for_link(link):
    if not link or link in {" ", "_"}:
        return False
    name = slug_filename(link)
    path = os.path.join(CONCEPTS_PATH, f"{name}.md")
    if os.path.exists(path):
        return False
    write_text(path, concept_stub(name))
    return True


def ensure_graph_index(concept_names, paper_edges, concept_edges):
    path = os.path.join(CONCEPTS_PATH, "Concept Graph.md")
    generated = ["# Concept Graph", "", GRAPH_START, "", "## Concepts"]
    if concept_names:
        generated.extend(f"- [[{name}]]" for name in sorted(concept_names) if name != "Concept Graph")
    else:
        generated.append("- ")
    generated.extend(["", "## Paper Links"])
    if paper_edges:
        generated.extend(f"- [[{paper}]] -> [[{concept}]]" for paper, concept in sorted(paper_edges))
    else:
        generated.append("- ")
    generated.extend(["", "## Concept Links"])
    if concept_edges:
        generated.extend(f"- [[{source}]] -> [[{target}]]" for source, target in sorted(concept_edges))
    else:
        generated.append("- ")
    generated.extend(["", GRAPH_END, ""])
    new_block = "\n".join(generated)

    if os.path.exists(path):
        text = read_text(path)
        if GRAPH_START in text and GRAPH_END in text:
            before = text.split(GRAPH_START, 1)[0].rstrip()
            after = text.split(GRAPH_END, 1)[1].lstrip()
            new_text = before + "\n\n" + "\n".join(generated[2:]) + "\n" + after
        else:
            new_text = text.rstrip() + "\n\n" + "\n".join(generated[2:])
    else:
        new_text = new_block

    if not os.path.exists(path) or read_text(path) != new_text:
        write_text(path, new_text)
        return True
    return False


def main():
    os.makedirs(CONCEPTS_PATH, exist_ok=True)
    changed = []
    created_concepts = []

    for path in iter_papers():
        if repair_paper(path):
            changed.append(relpath(path))

    for path in iter_papers():
        text = read_text(path)
        for link in section_links(text, "Connections"):
            if ensure_concept_for_link(link):
                created_concepts.append(link)

    concept_names = {os.path.splitext(os.path.basename(path))[0] for path in iter_concepts()}
    paper_edges = set()
    concept_edges = set()

    for path in iter_papers():
        paper = paper_citekey(path)
        for link in section_links(read_text(path), "Connections"):
            paper_edges.add((paper, link))

    for path in iter_concepts():
        source = os.path.splitext(os.path.basename(path))[0]
        if source == "Concept Graph":
            continue
        text = read_text(path)
        for link in section_links(text, "Related Concepts"):
            concept_edges.add((source, link))

    if ensure_graph_index(concept_names, paper_edges, concept_edges):
        changed.append("concepts/Concept Graph.md")

    rebuild_manifests()

    if created_concepts:
        print("Created concept stubs:")
        for name in sorted(created_concepts):
            print(f"- [[{name}]]")
    if changed:
        print("Repaired files:")
        for path in sorted(set(changed)):
            print(f"- {path}")
    if not changed and not created_concepts:
        print("No mechanical repairs needed.")


if __name__ == "__main__":
    main()
