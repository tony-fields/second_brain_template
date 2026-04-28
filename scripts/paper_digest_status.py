import argparse
import json

from vault_utils import inspect_paper, iter_papers, rebuild_manifests


def main():
    parser = argparse.ArgumentParser(description="List paper notes that need AI digestion.")
    parser.add_argument("--all", action="store_true", help="Show all papers, including already digested papers.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    papers = [inspect_paper(path) for path in iter_papers()]
    if not args.all:
        papers = [paper for paper in papers if paper["digest_status"] != "digested"]

    if args.json:
        print(json.dumps(papers, indent=2))
        return

    if not papers:
        print("No papers need AI digestion.")
        return

    for paper in papers:
        print(f"{paper['digest_status']}: {paper['path']} ({paper['title']})")

    rebuild_manifests()


if __name__ == "__main__":
    main()
