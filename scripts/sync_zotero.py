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


def request(method, path, key, params=None, data=None, extra_headers=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(data).encode() if data is not None else None
    hdrs = {**HEADERS, "Zotero-API-Key": key, **(extra_headers or {})}
    req = urllib.request.Request(url, data=body, method=method, headers=hdrs)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {detail}") from None


def resolve_collection(gid, key, name):
    """Return the collection key for a collection named `name` in the group, else None."""
    _, cols = request("GET", f"/groups/{gid}/collections", key, params={"limit": 100})
    for c in cols or []:
        if c["data"]["name"].strip().lower() == name.strip().lower():
            return c["key"]
    return None


def find_all(gid, key, refkey):
    """Return [(item_key, version), ...] for every item tagged hm-ref:<refkey>."""
    _, items = request("GET", f"/groups/{gid}/items", key,
                        params={"tag": f"hm-ref:{refkey}", "limit": 50})
    return [(it["key"], it["version"]) for it in (items or [])]


def delete_item(gid, key, item_key, version):
    request("DELETE", f"/groups/{gid}/items/{item_key}", key,
            extra_headers={"If-Unmodified-Since-Version": str(version)})


def audit(gid, key):
    """Print every item tagged 'HiveMind' with its key, type, tags, and collections."""
    _, items = request("GET", f"/groups/{gid}/items", key,
                        params={"tag": "HiveMind", "limit": 100})
    print(f"{len(items or [])} item(s) tagged 'HiveMind':")
    for it in items or []:
        d = it["data"]
        tags = ",".join(t["tag"] for t in d.get("tags", []))
        print(f"  {it['key']}  [{d.get('itemType')}]  cols={d.get('collections')}  "
              f"tags=({tags})  {d.get('title','')[:60]}")


def main():
    flags = {"--dry-run", "--audit"}
    args = [a for a in sys.argv[1:] if a not in flags]
    dry = "--dry-run" in sys.argv
    do_audit = "--audit" in sys.argv
    api_key = os.environ.get("ZOTERO_API_KEY")
    gid = os.environ.get("ZOTERO_GROUP_ID")
    if not dry and (not api_key or not gid):
        print("error: set ZOTERO_API_KEY and ZOTERO_GROUP_ID (or use --dry-run)")
        return 1

    if do_audit:
        audit(gid, api_key)
        return 0

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
        matches = find_all(gid, api_key, ref["key"])
        if not matches:
            _, resp = request("POST", f"/groups/{gid}/items", api_key, data=[item])
            failed = (resp or {}).get("failed") or {}
            if failed:
                print(f"FAILED {ref['key']}: {failed}")
            else:
                print(f"created {ref['key']} -> {resp['successful']['0']['key']}")
        else:
            keep_key, keep_ver = matches[0]
            request("PATCH", f"/groups/{gid}/items/{keep_key}", api_key, data=item,
                    extra_headers={"If-Unmodified-Since-Version": str(keep_ver)})
            extras = matches[1:]
            for dup_key, dup_ver in extras:
                delete_item(gid, api_key, dup_key, dup_ver)
            note = f" (removed {len(extras)} duplicate(s))" if extras else ""
            print(f"updated {ref['key']} -> {keep_key}{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
