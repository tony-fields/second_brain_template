import json
import os
import re
import hashlib

# ===== PATH SETUP (RELATIVE) =====

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(BASE_DIR, "zotero-export")
PAPERS_PATH = os.path.join(BASE_DIR, "papers")

os.makedirs(PAPERS_PATH, exist_ok=True)

# ===== FIND EXPORT FILE =====

json_files = [f for f in os.listdir(EXPORT_DIR) if f.endswith(".json")]

if not json_files:
    print("❌ No Zotero export JSON found in zotero-export/")
    exit(1)

EXPORT_PATH = os.path.join(EXPORT_DIR, json_files[0])

# ===== HELPERS =====

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def compute_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

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

# ===== BUILD AUTO CONTENT =====

def build_auto_content(authors, year, citekey, abstract, pdf_link, annotations):
    content = f"""## Metadata
- Authors: {authors}
- Year: {year}
- Citekey: {citekey}

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

    content = content.strip()
    hash_val = compute_hash(content)

    return content, hash_val

# ===== UPDATE EXISTING NOTE =====

def update_note(filepath, auto_content, new_hash, title, citekey):
    start_tag = "<!-- AUTO-GENERATED START -->"
    end_tag = "<!-- AUTO-GENERATED END -->"

    with open(filepath, "r", encoding="utf-8") as f:
        old = f.read()

    # Extract old hash
    old_hash = None
    match = re.search(r"<!-- HASH: (.*?) -->", old)
    if match:
        old_hash = match.group(1)

    # Skip if no changes
    if old_hash == new_hash:
        return "unchanged"

    new_auto_block = f"""<!-- HASH: {new_hash} -->

{auto_content}
"""

    # CASE 1: markers exist → replace section
    if start_tag in old and end_tag in old:
        before = old.split(start_tag)[0]
        after = old.split(end_tag)[1]

        new_text = before + start_tag + "\n\n" + new_auto_block + "\n" + end_tag + after

    # CASE 2: markers missing → inject
    else:
        print(f"⚠️ Injecting markers into: {citekey}.md")

        new_text = f"""# {title}

{start_tag}

{new_auto_block}

{end_tag}

---

{old}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_text)

    return "updated"

# ===== CREATE NEW NOTE =====

def create_note(filepath, title, citekey, auto_content, hash_val):
    content = f"""---
title: "{title}"
aliases: ["{title}", "{citekey}"]
citekey: {citekey}
tags: [paper]
---

# {title}

<!-- AUTO-GENERATED START -->

<!-- HASH: {hash_val} -->

{auto_content}

<!-- AUTO-GENERATED END -->

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

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# ===== LOAD DATA =====

with open(EXPORT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])
print(f"Found {len(items)} items")

# ===== MAIN LOOP =====

created = 0
updated = 0
unchanged = 0
skipped = 0

for item in items:
    title = item.get("title", "No Title")
    citekey = item.get("citationKey")

    if not citekey:
        skipped += 1
        continue

    citekey = safe_filename(citekey)
    filepath = os.path.join(PAPERS_PATH, f"{citekey}.md")

    authors = format_authors(item.get("creators", []))
    year = item.get("year", "")
    abstract = item.get("abstractNote", "")
    pdf_link = extract_pdf_link(item.get("attachments", []))
    annotations = extract_annotations(item)

    auto_content, hash_val = build_auto_content(
        authors, year, citekey, abstract, pdf_link, annotations
    )

    if os.path.exists(filepath):
        result = update_note(filepath, auto_content, hash_val, title, citekey)

        if result == "updated":
            print(f"Updated: {citekey}.md")
            updated += 1
        elif result == "unchanged":
            unchanged += 1
    else:
        create_note(filepath, title, citekey, auto_content, hash_val)
        print(f"Created: {citekey}.md")
        created += 1

# ===== SUMMARY =====

print("\n✅ Sync complete.")
print(f"Created: {created}")
print(f"Updated: {updated}")
print(f"Unchanged: {unchanged}")
print(f"Skipped: {skipped}")