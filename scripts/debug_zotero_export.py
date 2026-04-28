import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(BASE_DIR, "zotero-export")
PAPERS_DIR = os.path.join(BASE_DIR, "papers")


def extract_items(data):
    if isinstance(data, dict):
        if isinstance(data.get("items"), list):
            return data["items"], "dict.items"
        if isinstance(data.get("references"), list):
            return data["references"], "dict.references"
    if isinstance(data, list):
        return data, "list"
    return [], type(data).__name__


def item_citekey(item):
    if not isinstance(item, dict):
        return ""
    return item.get("citationKey") or item.get("citation-key") or item.get("id") or ""


def item_title(item):
    if not isinstance(item, dict):
        return "No Title"
    title = item.get("title", "No Title")
    if isinstance(title, list):
        return " ".join(str(part) for part in title)
    return str(title)


def describe_file(path):
    stat = os.stat(path)
    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return f"{os.path.relpath(path, BASE_DIR)} | {stat.st_size} bytes | modified {modified}"


def main():
    json_files = sorted(name for name in os.listdir(EXPORT_DIR) if name.endswith(".json"))

    print("Zotero export diagnostic")
    print("========================")
    print(f"Export directory: zotero-export/")

    if not json_files:
        print("Status: no JSON export found")
        print("")
        print("Expected file:")
        print("  any .json file in zotero-export/")
        print("")
        print("Next step:")
        print("  Export your Zotero library with Better BibTeX into zotero-export/")
        return 1

    print("JSON files found:")
    for name in json_files:
        print(f"  - {describe_file(os.path.join(EXPORT_DIR, name))}")

    json_paths = [os.path.join(EXPORT_DIR, name) for name in json_files]
    export_path = max(json_paths, key=os.path.getmtime)
    print("")
    print(f"Using export: {describe_file(export_path)}")

    with open(export_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items, shape = extract_items(data)
    with_citekey = [item for item in items if item_citekey(item)]
    without_citekey = [item for item in items if not item_citekey(item)]
    paper_notes = [
        name for name in os.listdir(PAPERS_DIR)
        if name.endswith(".md") and not name.startswith(".")
    ] if os.path.isdir(PAPERS_DIR) else []

    print(f"JSON shape: {shape}")
    print(f"Items in export: {len(items)}")
    print(f"Items with citationKey/id: {len(with_citekey)}")
    print(f"Items skipped because citationKey/id is missing: {len(without_citekey)}")
    print(f"Paper notes currently in papers/: {len(paper_notes)}")

    if without_citekey:
        print("")
        print("First skipped items:")
        for item in without_citekey[:5]:
            print(f"  - {item_title(item)}")

    if with_citekey:
        print("")
        print("First importable items:")
        for item in with_citekey[:5]:
            print(f"  - {item_citekey(item)}: {item_title(item)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
