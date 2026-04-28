import argparse
import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(BASE_DIR, "zotero-export")


def default_export_path():
    json_paths = [
        os.path.join(EXPORT_DIR, name)
        for name in os.listdir(EXPORT_DIR)
        if name.endswith(".json")
    ]
    if json_paths:
        return max(json_paths, key=os.path.getmtime)

    return None


def json_export_files():
    return sorted(name for name in os.listdir(EXPORT_DIR) if name.endswith(".json"))


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
    return (
        item.get("citationKey")
        or item.get("citation-key")
        or item.get("id")
        or ""
    )


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


def load_items(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return extract_items(data)


def main():
    parser = argparse.ArgumentParser(description="Count papers/items in the Zotero Better BibTeX export.")
    parser.add_argument("--export", help="Path to a Zotero Better BibTeX JSON export.")
    parser.add_argument("--all", action="store_true", help="Show counts for every JSON file in zotero-export/.")
    parser.add_argument("--list", action="store_true", help="List importable item citekeys and titles.")
    args = parser.parse_args()

    if args.all:
        json_files = json_export_files()
        if not json_files:
            print("No JSON exports found in zotero-export/.")
            return 1
        for name in json_files:
            path = os.path.join(EXPORT_DIR, name)
            items, shape = load_items(path)
            with_citekey = [item for item in items if item_citekey(item)]
            print(describe_file(path))
            print(f"  JSON shape: {shape}")
            print(f"  Zotero export papers/items: {len(items)}")
            print(f"  Importable with citationKey/id: {len(with_citekey)}")
        return 0

    export_path = os.path.abspath(args.export) if args.export else default_export_path()
    if not export_path:
        print("Zotero export papers: 0")
        print("No JSON export found. Expected: any .json file in zotero-export/")
        return 1

    items, shape = load_items(export_path)
    with_citekey = [item for item in items if item_citekey(item)]
    without_citekey = [item for item in items if not item_citekey(item)]

    print(f"Export file: {describe_file(export_path)}")
    print(f"JSON shape: {shape}")
    print(f"Zotero export papers: {len(items)}")
    print(f"Importable papers with citationKey/id: {len(with_citekey)}")
    print(f"Skipped papers missing citationKey/id: {len(without_citekey)}")

    if args.list and with_citekey:
        print("")
        print("Importable items:")
        for item in with_citekey:
            print(f"- {item_citekey(item)}: {item_title(item)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
