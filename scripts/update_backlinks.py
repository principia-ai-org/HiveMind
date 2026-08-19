#!/usr/bin/env python3
"""Maintain a `## Cited by` section in each references/*.md.

For every reference, list the problems that cite it (problem ID + link). This is
computed deterministically from the `../references/<key>.md` links in problems/*.md, so
it needs no LLM — run it after citations are in keyed form. Standard library only.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"
REFERENCES = ROOT / "references"
SKIP = {"README", "TEMPLATE", "TAGS"}

# A link whose target is ../references/<key>.md (inline citation or reference-list entry)
REF_LINK = re.compile(r"\]\(\.\./references/([^)]+?)\.md\)")
# An existing "## Cited by" section, up to the next "## " heading or end of file
CITED_BLOCK = re.compile(r"\n*##\s+Cited by\s*\n.*?(?=\n##\s|\Z)", re.DOTALL)


def problem_files():
    return [p for p in sorted(PROBLEMS.glob("*.md")) if p.stem not in SKIP]


def citations_by_reference():
    """Map reference key -> sorted list of (problem_id, problem_filename)."""
    mapping = {}
    for prob in problem_files():
        m = re.match(r"HM-\d+", prob.stem)
        if not m:
            continue
        pid = m.group(0)
        for key in set(REF_LINK.findall(prob.read_text(encoding="utf-8"))):
            mapping.setdefault(key, set()).add((pid, prob.name))
    return {k: sorted(v) for k, v in mapping.items()}


def main():
    mapping = citations_by_reference()
    changed = 0
    for ref in sorted(REFERENCES.glob("*.md")):
        if ref.stem in {"README", "TEMPLATE"}:
            continue
        text = ref.read_text(encoding="utf-8")
        body = CITED_BLOCK.sub("", text).rstrip()
        cites = mapping.get(ref.stem, [])
        if cites:
            lines = "\n".join(f"- [{pid}](../problems/{name})" for pid, name in cites)
            new = f"{body}\n\n## Cited by\n\n{lines}\n"
        else:
            new = body + "\n"
        if new != text:
            ref.write_text(new, encoding="utf-8")
            changed += 1
            print(f"backlinks: {ref.name} -> {len(cites)} problem(s)")
    print(f"update_backlinks: {changed} file(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
