#!/usr/bin/env python3
"""Sync references/*.md into a Zotero group library (one-way: repo -> Zotero).

Each reference file becomes one Zotero item. Items are matched by a hidden tag
`hm-ref:<key>` (key = the reference filename stem), so re-running updates the same
item instead of creating duplicates — no local state file needed.

Environment:
  ZOTERO_API_KEY    API key with write access to the group
  ZOTERO_GROUP_ID   numeric group id
  ZOTERO_COLLECTION collection (folder) name to file items under (default "HiveMind";
                    set empty to sync to the group's top level)

Usage:
  python3 scripts/sync_zotero.py [--dry-run] [file ...]
  (no files given -> all references/*.md except README/TEMPLATE)

Standard library only.
"""

import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "references"
SKIP = {"README", "TEMPLATE"}
API = "https://api.zotero.org"
HEADERS = {"Zotero-API-Version": "3", "Content-Type": "application/json"}


def parse_reference(path):
    """Pull title, authors, link, and summary out of a reference .md file."""
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    authors = re.search(r"^\*Authors:\*\s*(.+)$", text, re.MULTILINE)
    link = re.search(r"^\*Link:\*\s*(\S+)", text, re.MULTILINE)
    summary = re.search(r"^##\s+Summary\s*$(.+)", text, re.MULTILINE | re.DOTALL)
    return {
        "key": path.stem,
        "title": title.group(1).strip() if title else path.stem,
        "authors": authors.group(1).strip() if authors else "",
        "link": link.group(1).strip() if link else "",
        "summary": summary.group(1).strip() if summary else "",
    }


def creators(authors):
    """Turn an author string into Zotero creator objects."""
    out = []
    for name in re.split(r",|;|\band\b|&", authors):
        name = name.strip().rstrip(".")
        if not name or name.lower() in {"et al", "others"}:
            continue
        parts = name.split()
        if len(parts) == 1:
            out.append({"creatorType": "author", "name": parts[0]})
        else:
            out.append({"creatorType": "author",
                        "firstName": " ".join(parts[:-1]), "lastName": parts[-1]})
    return out


def build_item(ref, collection_key=None):
    year = re.search(r"(\d{4})", ref["key"])
    link = ref["link"]
    extra = f"HiveMind summary:\n{ref['summary']}" if ref["summary"] else ""
    tags = [{"tag": f"hm-ref:{ref['key']}"}, {"tag": "HiveMind"}]
    base = {
        "title": ref["title"],
        "creators": creators(ref["authors"]),
        "date": year.group(1) if year else "",
        "url": link,
        "extra": extra,
        "tags": tags,
        "collections": [collection_key] if collection_key else [],
    }
    if "arxiv.org" in link:
        m = re.search(r"arxiv\.org/abs/([\w.\-/]+)", link)
        return {**base, "itemType": "preprint", "repository": "arXiv",
                "archiveID": f"arXiv:{m.group(1)}" if m else ""}
    if "doi.org" in link or "/10." in link:
        doi = re.search(r"(10\.\d{4,}/\S+)", link)
        return {**base, "itemType": "journalArticle", "DOI": doi.group(1) if doi else ""}
    return {**base, "itemType": "webpage"}


def request(method, path, key, params=None, data=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={**HEADERS, "Zotero-API-Key": key})
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode()
        return resp.status, (json.loads(raw) if raw else None)


def resolve_collection(gid, key, name):
    """Return the collection key for a collection named `name` in the group, else None."""
    _, cols = request("GET", f"/groups/{gid}/collections", key, params={"limit": 100})
    for c in cols or []:
        if c["data"]["name"].strip().lower() == name.strip().lower():
            return c["key"]
    return None


def find_existing(gid, key, refkey):
    """Return (item_key, version) for an existing item tagged hm-ref:<refkey>, else None."""
    _, items = request("GET", f"/groups/{gid}/items", key,
                        params={"tag": f"hm-ref:{refkey}", "limit": 1})
    if items:
        return items[0]["key"], items[0]["version"]
    return None


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    api_key = os.environ.get("ZOTERO_API_KEY")
    gid = os.environ.get("ZOTERO_GROUP_ID")
    if not dry and (not api_key or not gid):
        print("error: set ZOTERO_API_KEY and ZOTERO_GROUP_ID (or use --dry-run)")
        return 1

    files = [pathlib.Path(a) for a in args] if args else \
        [p for p in sorted(REFERENCES.glob("*.md")) if p.stem not in SKIP]

    collection_name = os.environ.get("ZOTERO_COLLECTION", "HiveMind")
    collection_key = None
    if not dry and collection_name:
        collection_key = resolve_collection(gid, api_key, collection_name)
        if not collection_key:
            print(f"error: no collection named {collection_name!r} in group {gid}. "
                  f"Create it in Zotero, or set ZOTERO_COLLECTION='' to sync to the top level.")
            return 1
        print(f"filing references under collection {collection_name!r} ({collection_key})")

    for path in files:
        ref = parse_reference(path)
        item = build_item(ref, collection_key)
        if dry:
            print(f"--- {ref['key']} ({item['itemType']}) -> collection {collection_name or '(top level)'} ---")
            print(json.dumps(item, indent=2, ensure_ascii=False))
            continue
        existing = find_existing(gid, api_key, ref["key"])
        if existing:
            item_key, version = existing
            item["key"], item["version"] = item_key, version
            request("PUT", f"/groups/{gid}/items/{item_key}", api_key, data=item)
            print(f"updated {ref['key']} -> {item_key}")
        else:
            _, resp = request("POST", f"/groups/{gid}/items", api_key, data=[item])
            failed = (resp or {}).get("failed") or {}
            if failed:
                print(f"FAILED {ref['key']}: {failed}")
            else:
                new_key = resp["successful"]["0"]["key"]
                print(f"created {ref['key']} -> {new_key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
