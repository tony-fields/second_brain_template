import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(BASE_DIR, "zotero-export")
PAPERS_DIR = os.path.join(BASE_DIR, "papers")


def main():
    preferred = os.path.join(EXPORT_DIR, "library.json")
    json_files = sorted(name for name in os.listdir(EXPORT_DIR) if name.endswith(".json"))

    print("Zotero export diagnostic")
    print("========================")
    print(f"Export directory: zotero-export/")

    if not json_files:
        print("Status: no JSON export found")
        print("")
        print("Expected file:")
        print("  zotero-export/library.json")
        print("")
        print("Next step:")
        print("  Export your Zotero library with Better BibTeX and save it as zotero-export/library.json")
        return 1

    export_path = preferred if os.path.exists(preferred) else os.path.join(EXPORT_DIR, json_files[0])
    print(f"Using export: {os.path.relpath(export_path, BASE_DIR)}")

    with open(export_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", [])
    with_citekey = [item for item in items if item.get("citationKey")]
    without_citekey = [item for item in items if not item.get("citationKey")]
    paper_notes = [
        name for name in os.listdir(PAPERS_DIR)
        if name.endswith(".md") and not name.startswith(".")
    ] if os.path.isdir(PAPERS_DIR) else []

    print(f"Items in export: {len(items)}")
    print(f"Items with citationKey: {len(with_citekey)}")
    print(f"Items skipped because citationKey is missing: {len(without_citekey)}")
    print(f"Paper notes currently in papers/: {len(paper_notes)}")

    if without_citekey:
        print("")
        print("First skipped items:")
        for item in without_citekey[:5]:
            print(f"  - {item.get('title', 'No Title')}")

    if with_citekey:
        print("")
        print("First importable items:")
        for item in with_citekey[:5]:
            print(f"  - {item.get('citationKey')}: {item.get('title', 'No Title')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
