#!/usr/bin/env python3
"""Validate the problems/ <-> references/ contract.

Checks, from the repository root:
  1. Every reference linked from a problem (`../references/<key>.md`) exists.
  2. No problem still has an unconverted numbered reference (`[N] <url>`).
  3. Every references/*.md has a title (H1), an *Authors:* line, a *Link:* line,
     and a non-empty `## Summary` section.
It also warns (without failing) about reference files that no problem cites.

Exit code 0 = all checks pass, 1 = at least one error. Standard library only.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"
REFERENCES = ROOT / "references"

# Markdown link whose target is ../references/<key>.md
REF_LINK = re.compile(r"\]\(\.\./references/([^)]+?)\.md\)")
# An unconverted numbered reference entry, e.g. "[1] https://..."
NUMBERED_REF = re.compile(r"^\[\d+\]\s+\S", re.MULTILINE)

SKIP = {"README", "TEMPLATE"}


def problem_files():
    return [p for p in PROBLEMS.glob("*.md") if p.stem not in SKIP]


def reference_files():
    return [p for p in REFERENCES.glob("*.md") if p.stem not in SKIP]


def check_links(errors):
    """Every ../references/<key>.md cited in a problem must exist."""
    cited = set()
    for prob in problem_files():
        text = prob.read_text(encoding="utf-8")
        for key in sorted(set(REF_LINK.findall(text))):
            cited.add(key)
            if not (REFERENCES / f"{key}.md").is_file():
                errors.append(
                    f"{prob.relative_to(ROOT)}: cites references/{key}.md, "
                    f"which does not exist"
                )
    return cited


def check_converted(errors):
    """Numbered citations must have been converted to author-year links on PR."""
    for prob in problem_files():
        if NUMBERED_REF.search(prob.read_text(encoding="utf-8")):
            errors.append(
                f"{prob.relative_to(ROOT)}: has an unconverted numbered reference "
                f"(`[N] <url>`); the PR pipeline converts these to author-year links"
            )


def check_reference_format(errors):
    """Each reference file must have title, Authors, Link, and a non-empty Summary."""
    for ref in reference_files():
        text = ref.read_text(encoding="utf-8")
        rel = ref.relative_to(ROOT)
        if not re.search(r"^# .+", text, re.MULTILINE):
            errors.append(f"{rel}: missing H1 title (`# ...`)")
        if not re.search(r"^\*Authors:\*", text, re.MULTILINE):
            errors.append(f"{rel}: missing `*Authors:*` line")
        if not re.search(r"^\*Link:\*\s*\S", text, re.MULTILINE):
            errors.append(f"{rel}: missing or empty `*Link:*` line")
        m = re.search(r"^##\s+Summary\s*$(.*)", text, re.MULTILINE | re.DOTALL)
        if not m or not m.group(1).strip():
            errors.append(f"{rel}: missing or empty `## Summary` section")


def warn_orphans(cited):
    for ref in reference_files():
        if ref.stem not in cited:
            print(f"warning: references/{ref.name} is not cited by any problem")


def main():
    errors = []
    cited = check_links(errors)
    check_converted(errors)
    check_reference_format(errors)
    warn_orphans(cited)

    if errors:
        print(f"\ncheck_references: {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("check_references: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
