import argparse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(BASE_DIR, "zotero-export")


def default_export_path():
    preferred = os.path.join(EXPORT_DIR, "library.json")
    if os.path.exists(preferred):
        return preferred

    json_files = sorted(name for name in os.listdir(EXPORT_DIR) if name.endswith(".json"))
    if json_files:
        return os.path.join(EXPORT_DIR, json_files[0])

    return None


def main():
    parser = argparse.ArgumentParser(description="Count papers/items in the Zotero Better BibTeX export.")
    parser.add_argument("--export", help="Path to a Zotero Better BibTeX JSON export.")
    args = parser.parse_args()

    export_path = os.path.abspath(args.export) if args.export else default_export_path()
    if not export_path:
        print("Zotero export papers: 0")
        print("No JSON export found. Expected: zotero-export/library.json")
        return 1

    with open(export_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", [])
    with_citekey = [item for item in items if item.get("citationKey")]
    without_citekey = [item for item in items if not item.get("citationKey")]

    print(f"Export file: {os.path.relpath(export_path, BASE_DIR)}")
    print(f"Zotero export papers: {len(items)}")
    print(f"Importable papers with citationKey: {len(with_citekey)}")
    print(f"Skipped papers missing citationKey: {len(without_citekey)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
