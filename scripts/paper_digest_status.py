import argparse
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS_PATH = os.path.join(BASE_DIR, "papers")

AUTO_HASH_RE = re.compile(r"<!-- HASH: (.*?) -->")
AI_HASH_RE = re.compile(r"<!-- AI-SOURCE-HASH: (.*?) -->")
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract(pattern, text):
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def normalize_ai_hash(value):
    if value.startswith("pending:"):
        return ""
    return value


def inspect_paper(path):
    text = read_text(path)
    citekey = os.path.splitext(os.path.basename(path))[0]
    auto_hash = extract(AUTO_HASH_RE, text)
    ai_hash = normalize_ai_hash(extract(AI_HASH_RE, text))
    title = extract(TITLE_RE, text) or citekey

    if not auto_hash:
        status = "missing-auto-hash"
    elif not ai_hash:
        status = "needs-digest"
    elif ai_hash != auto_hash:
        status = "stale-digest"
    else:
        status = "digested"

    return {
        "citekey": citekey,
        "title": title,
        "path": os.path.relpath(path, BASE_DIR),
        "auto_hash": auto_hash,
        "ai_source_hash": ai_hash,
        "status": status,
    }


def iter_papers():
    if not os.path.isdir(PAPERS_PATH):
        return

    for name in sorted(os.listdir(PAPERS_PATH)):
        if name.startswith(".") or not name.endswith(".md"):
            continue
        yield os.path.join(PAPERS_PATH, name)


def main():
    parser = argparse.ArgumentParser(description="List paper notes that need AI digestion.")
    parser.add_argument("--all", action="store_true", help="Show all papers, including already digested papers.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    papers = [inspect_paper(path) for path in iter_papers()]
    if not args.all:
        papers = [paper for paper in papers if paper["status"] != "digested"]

    if args.json:
        print(json.dumps(papers, indent=2))
        return

    if not papers:
        print("No papers need AI digestion.")
        return

    for paper in papers:
        print(f"{paper['status']}: {paper['path']} ({paper['title']})")


if __name__ == "__main__":
    main()
