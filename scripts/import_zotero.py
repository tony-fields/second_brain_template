import json
import os
import re

# ===== PATH SETUP (FULLY RELATIVE) =====

# scripts/ → vault root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPORT_DIR = os.path.join(BASE_DIR, "zotero-export")

# Find any JSON file in export folder
json_files = [f for f in os.listdir(EXPORT_DIR) if f.endswith(".json")]

if not json_files:
    print("❌ No Zotero export JSON found in zotero-export/")
    exit(1)

EXPORT_PATH = os.path.join(EXPORT_DIR, json_files[0])
PAPERS_PATH = os.path.join(BASE_DIR, "papers")

# Ensure papers folder exists
os.makedirs(PAPERS_PATH, exist_ok=True)

# ===== HELPERS =====

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def format_authors(creators):
    authors = []
    for c in creators:
        if c.get("creatorType") == "author":
            first = c.get("firstName", "")
            last = c.get("lastName", "")
            name = f"{first} {last}".strip()
            authors.append(name)
    return ", ".join(authors)

def extract_pdf_link(attachments):
    for att in attachments:
        path = att.get("path")
        if path:
            return path
    return ""

def extract_annotations(item):
    annotations = []
    for ann in item.get("annotations", []):
        text = ann.get("text") or ann.get("annotationText") or ""
        if text.strip():
            annotations.append(text.strip())
    return annotations

# ===== LOAD DATA =====

if not os.path.exists(EXPORT_PATH):
    print(f"❌ Export file not found at: {EXPORT_PATH}")
    exit(1)

with open(EXPORT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])
print(f"Found {len(items)} items")

# ===== PROCESS ITEMS =====

created = 0
skipped = 0

for item in items:
    title = item.get("title", "No Title")
    citekey = item.get("citationKey")

    if not citekey:
        skipped += 1
        continue

    citekey = safe_filename(citekey)
    filepath = os.path.join(PAPERS_PATH, f"{citekey}.md")

    # Skip existing files (robustness)
    if os.path.exists(filepath):
        skipped += 1
        continue

    authors = format_authors(item.get("creators", []))
    year = item.get("year", "")
    abstract = item.get("abstractNote", "")
    pdf_link = extract_pdf_link(item.get("attachments", []))
    annotations = extract_annotations(item)

    # ===== BUILD NOTE CONTENT =====

    content = f"""---
title: "{title}"
aliases: ["{title}", "{citekey}"]
citekey: {citekey}
authors: "{authors}"
year: "{year}"
tags: [paper]
---

# {title}

## Links
- PDF Path: {pdf_link}

---

## Summary
{abstract}

---

## Highlights
"""

    if annotations:
        for a in annotations:
            content += f"- {a}\n"
    else:
        content += "- (No highlights found)\n"

    content += """

---

## Key Contributions
- 

---

## Core Ideas / Intuition
- 

---

## Technical Details
- Definitions:
- Lemmas:
- Proof Sketches:

---

## Notes
- 

---

## Connections
- [[ ]]

---

## Open Questions
- 

---

## Related Papers
- 
"""

    # ===== WRITE FILE =====

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {citekey}.md")
    created += 1

# ===== SUMMARY =====

print("\n✅ Done.")
print(f"Created: {created}")
print(f"Skipped: {skipped}")