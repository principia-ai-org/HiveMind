#!/usr/bin/env python3
"""Extract the Overview section from a knowledge Markdown file.

The section is returned verbatim, so the bullets, blank lines, and `---`
dividers that `output-rules.md` asks for survive into the email body.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SECTION_TITLE = "Overview"
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


class OverviewError(ValueError):
    """Raised when the Overview section is missing or malformed."""


@dataclass(frozen=True)
class MarkdownSection:
    title: str
    body: str
    line: int


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise OverviewError(f"{path}: file does not exist") from exc
    except OSError as exc:
        raise OverviewError(f"{path}: could not read file: {exc}") from exc


def markdown_h2_sections(text: str) -> list[MarkdownSection]:
    matches = list(H2_RE.finditer(text))
    sections: list[MarkdownSection] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        line = text.count("\n", 0, match.start()) + 1
        sections.append(
            MarkdownSection(
                title=match.group(1).strip(),
                body=text[match.end() : end].strip(),
                line=line,
            )
        )
    return sections


def extract_overview(text: str, label: str = "<markdown>") -> str:
    sections = [
        section
        for section in markdown_h2_sections(text)
        if section.title.casefold() == SECTION_TITLE.casefold()
    ]
    if not sections:
        raise OverviewError(f"{label}: missing required '## {SECTION_TITLE}' section")
    if len(sections) > 1:
        lines = ", ".join(str(section.line) for section in sections)
        raise OverviewError(
            f"{label}: expected one '## {SECTION_TITLE}' section; found {len(sections)} "
            f"on lines {lines}"
        )

    section = sections[0]
    overview = section.body.strip()
    if not overview:
        raise OverviewError(
            f"{label}:{section.line}: '## {SECTION_TITLE}' section must not be empty"
        )
    return overview


def extract_overview_file(path: Path) -> str:
    return extract_overview(read_text(path), str(path))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract the Overview section from a Markdown file."
    )
    parser.add_argument("markdown_file", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        print(extract_overview_file(args.markdown_file))
    except OverviewError as exc:
        print(f"Overview extraction failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
