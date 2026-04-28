import json
import os
import re
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS_PATH = os.path.join(BASE_DIR, "papers")
CONCEPTS_PATH = os.path.join(BASE_DIR, "concepts")
SYSTEM_PATH = os.path.join(BASE_DIR, ".system")

AUTO_START = "<!-- AUTO-GENERATED START -->"
AUTO_END = "<!-- AUTO-GENERATED END -->"
AI_START = "<!-- AI-GENERATED START -->"
AI_END = "<!-- AI-GENERATED END -->"
CONCEPT_START = "<!-- CONCEPT-GENERATED START -->"
CONCEPT_END = "<!-- CONCEPT-GENERATED END -->"
GRAPH_START = "<!-- GRAPH-GENERATED START -->"
GRAPH_END = "<!-- GRAPH-GENERATED END -->"

AUTO_HASH_RE = re.compile(r"<!-- HASH: (.*?) -->")
AI_HASH_RE = re.compile(r"<!-- AI-SOURCE-HASH: (.*?) -->")
AI_STATUS_RE = re.compile(r"<!-- AI-STATUS: (.*?) -->")
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

VALID_AI_STATUSES = {"pending", "complete", "needs-source", "failed", "review-needed"}


def relpath(path):
    return os.path.relpath(path, BASE_DIR)


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def iter_markdown_files(folder):
    if not os.path.isdir(folder):
        return
    for name in sorted(os.listdir(folder)):
        if name.startswith(".") or not name.endswith(".md"):
            continue
        yield os.path.join(folder, name)


def iter_papers():
    yield from iter_markdown_files(PAPERS_PATH)


def iter_concepts():
    yield from iter_markdown_files(CONCEPTS_PATH)


def extract(pattern, text):
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def normalize_ai_hash(value):
    if value.startswith("pending:"):
        return ""
    return value


def note_title(text, fallback):
    return extract(TITLE_RE, text) or fallback


def paper_citekey(path):
    return os.path.splitext(os.path.basename(path))[0]


def concept_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def slug_filename(name):
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    return cleaned or "Untitled"


def wiki_links(text):
    return [match.strip() for match in WIKI_LINK_RE.findall(text)]


def block_between(text, start, end):
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


def section_body(text, heading):
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


def ai_status(text):
    return extract(AI_STATUS_RE, text)


def inspect_paper(path):
    text = read_text(path)
    citekey = paper_citekey(path)
    auto_hash = extract(AUTO_HASH_RE, text)
    ai_hash = normalize_ai_hash(extract(AI_HASH_RE, text))
    status = ai_status(text)

    if not auto_hash:
        digest_status = "missing-auto-hash"
    elif status == "needs-source":
        digest_status = "needs-source"
    elif status == "failed":
        digest_status = "failed"
    elif status == "review-needed":
        digest_status = "review-needed"
    elif not ai_hash:
        digest_status = "needs-digest"
    elif ai_hash != auto_hash:
        digest_status = "stale-digest"
    else:
        digest_status = "digested"

    return {
        "citekey": citekey,
        "title": note_title(text, citekey),
        "path": relpath(path),
        "auto_hash": auto_hash,
        "ai_source_hash": ai_hash,
        "ai_status": status,
        "digest_status": digest_status,
        "concept_links": sorted(set(section_links(text, "Connections"))),
    }


def section_links(text, heading):
    return wiki_links(section_body(text, heading))


def inspect_concept(path):
    text = read_text(path)
    name = concept_name(path)
    return {
        "name": name,
        "title": note_title(text, name),
        "path": relpath(path),
        "related_papers": sorted(set(section_links(text, "Related Papers"))),
        "related_concepts": sorted(set(section_links(text, "Related Concepts"))),
        "has_generated_block": CONCEPT_START in text and CONCEPT_END in text,
    }


def load_vault_state():
    papers = [inspect_paper(path) for path in iter_papers()]
    concepts = [inspect_concept(path) for path in iter_concepts()]
    return papers, concepts


def write_json(path, data):
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def append_log(event, **fields):
    os.makedirs(SYSTEM_PATH, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **fields,
    }
    with open(os.path.join(SYSTEM_PATH, "pipeline_log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")


def rebuild_manifests():
    os.makedirs(SYSTEM_PATH, exist_ok=True)
    papers, concepts = load_vault_state()
    write_json(os.path.join(SYSTEM_PATH, "papers.json"), papers)
    write_json(os.path.join(SYSTEM_PATH, "concepts.json"), concepts)
    append_log("manifest_rebuilt", papers=len(papers), concepts=len(concepts))
    return papers, concepts


def build_ai_placeholder(hash_val):
    return f"""{AI_START}

<!-- AI-SOURCE-HASH: pending:{hash_val} -->
<!-- AI-STATUS: pending -->

## Digest Summary
- Pending AI digestion.

## Key Contributions
- Pending AI digestion.

## Core Ideas / Intuition
- Pending AI digestion.

## Important Details
- Pending AI digestion.

## Candidate Concepts
- Pending AI digestion.

{AI_END}"""


def ensure_ai_block(text, hash_val):
    if AI_START in text and AI_END in text:
        return text
    block = "\n\n---\n\n" + build_ai_placeholder(hash_val)
    if AUTO_END in text:
        return text.replace(AUTO_END, AUTO_END + block, 1)
    return text.rstrip() + block + "\n"


def ensure_connections_section(text):
    if re.search(r"^##\s+Connections\s*$", text, re.MULTILINE):
        return text
    return text.rstrip() + "\n\n---\n\n## Connections\n- \n"


def dedupe_connection_links(text):
    pattern = re.compile(r"(^##\s+Connections\s*$)(.*?)(?=^---\s*$|^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        return text

    heading = match.group(1)
    body = match.group(2)
    links = []
    seen = set()
    other_lines = []

    for line in body.splitlines():
        stripped = line.strip()
        found = wiki_links(stripped)
        if stripped.startswith("-") and found:
            for link in found:
                if link not in seen:
                    seen.add(link)
                    links.append(link)
        elif stripped and stripped != "- [[ ]]":
            other_lines.append(line)

    new_body = "\n"
    for link in links:
        new_body += f"- [[{link}]]\n"
    for line in other_lines:
        new_body += line + "\n"
    if not links and not other_lines:
        new_body += "- \n"

    return text[:match.start()] + heading + new_body + text[match.end():]


def concept_stub(name):
    return f"""# {name}

{CONCEPT_START}

## Definition
- Pending concept linking.

## Key Ideas
- Pending concept linking.

## Related Papers
- 

## Related Concepts
- 

{CONCEPT_END}

---

## Notes
- 
"""
