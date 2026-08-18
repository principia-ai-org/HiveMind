#!/usr/bin/env python3
"""Validate problem metadata: IDs and tags.

Checks, from the repository root, for every problems/*.md (excluding README/TEMPLATE/TAGS):
  1. The filename matches HM-<NNN>-<slug>.md and no `HM-NEXT` placeholder remains
     (in the filename or the metadata line).
  2. Problem IDs are unique.
  3. The metadata line has a `tags:` field with no unresolved placeholder, and every
     tag is listed in problems/TAGS.md.

Exit code 0 = pass, 1 = at least one error. Standard library only.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"
TAGS_FILE = PROBLEMS / "TAGS.md"

SKIP = {"README", "TEMPLATE", "TAGS"}
FILENAME = re.compile(r"^HM-(\d+)-[a-z0-9-]+$")
TAGS_FIELD = re.compile(r"tags:\s*(.+?)\s*(?:·|\*?$)", re.MULTILINE)


def allowed_tags():
    tags = set()
    for line in TAGS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"-\s+([a-z0-9-]+)\s*$", line)
        if m:
            tags.add(m.group(1))
    return tags


def problem_files():
    return [p for p in PROBLEMS.glob("*.md") if p.stem not in SKIP]


def check_ids(errors):
    seen = {}
    for prob in problem_files():
        rel = prob.relative_to(ROOT)
        if "HM-NEXT" in prob.stem:
            errors.append(f"{rel}: unresolved HM-NEXT placeholder in filename")
            continue
        m = FILENAME.match(prob.stem)
        if not m:
            errors.append(f"{rel}: filename must look like HM-NNN-<slug>.md")
            continue
        pid = f"HM-{m.group(1)}"
        if "HM-NEXT" in prob.read_text(encoding="utf-8"):
            errors.append(f"{rel}: unresolved HM-NEXT placeholder in the file body")
        if pid in seen:
            errors.append(f"{rel}: duplicate ID {pid} (also {seen[pid]})")
        else:
            seen[pid] = rel


def check_tags(errors, allowed):
    for prob in problem_files():
        rel = prob.relative_to(ROOT)
        m = TAGS_FIELD.search(prob.read_text(encoding="utf-8"))
        if not m:
            errors.append(f"{rel}: no `tags:` field found in the metadata line")
            continue
        for tag in (t.strip() for t in m.group(1).split(",") if t.strip()):
            if tag.startswith("<") or tag.endswith(">"):
                errors.append(f"{rel}: unresolved tag placeholder {tag!r}")
            elif tag not in allowed:
                errors.append(
                    f"{rel}: tag {tag!r} is not in problems/TAGS.md "
                    f"(add it there or use an existing tag)"
                )


def main():
    allowed = allowed_tags()
    if not allowed:
        print("check_problems: no tags found in problems/TAGS.md")
        return 1

    errors = []
    check_ids(errors)
    check_tags(errors, allowed)

    if errors:
        print(f"\ncheck_problems: {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("check_problems: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
