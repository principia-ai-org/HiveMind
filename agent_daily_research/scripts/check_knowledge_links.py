#!/usr/bin/env python3
"""Validate local links in generated knowledge outputs."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

try:
    from scripts.validate_inputs import parse_topics
except ModuleNotFoundError:  # when run as scripts/check_knowledge_links.py
    from validate_inputs import parse_topics


INLINE_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
REQUIRED_OVERVIEW_SECTIONS = {"short summary", "notes index"}


@dataclass(frozen=True)
class MarkdownLink:
    label: str
    target: str
    line: int


def read_text(path: Path) -> tuple[str | None, list[str]]:
    try:
        return path.read_text(encoding="utf-8"), []
    except FileNotFoundError:
        return None, [f"{path}: file does not exist"]
    except OSError as exc:
        return None, [f"{path}: could not read file: {exc}"]


def strip_fenced_blocks(text: str) -> str:
    return FENCED_BLOCK_RE.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def extract_markdown_links(text: str) -> list[MarkdownLink]:
    searchable = strip_fenced_blocks(text)
    links: list[MarkdownLink] = []
    for match in INLINE_LINK_RE.finditer(searchable):
        line = searchable.count("\n", 0, match.start()) + 1
        links.append(
            MarkdownLink(
                label=match.group(1).strip(),
                target=normalize_link_target(match.group(2)),
                line=line,
            )
        )
    return links


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<"):
        end = target.find(">")
        if end != -1:
            return target[1:end].strip()
    return target.split()[0] if target.split() else ""


def is_external_url(target: str) -> bool:
    parsed = urlsplit(target)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def resolve_local_link(source_path: Path, target: str) -> Path | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None

    link_path = Path(parsed.path)
    if not link_path.is_absolute():
        link_path = source_path.parent / link_path
    return link_path.resolve(strict=False)


def is_topic_note_path(path: Path, topics_dir: Path) -> bool:
    resolved_topics_dir = topics_dir.resolve(strict=False)
    if not is_relative_to(path, resolved_topics_dir):
        return False

    relative = path.relative_to(resolved_topics_dir)
    return len(relative.parts) == 3 and relative.parts[1] == "notes" and path.suffix == ".md"


def is_daily_summary_path(path: Path, daily_dir: Path) -> bool:
    resolved_daily_dir = daily_dir.resolve(strict=False)
    if not is_relative_to(path, resolved_daily_dir):
        return False

    relative = path.relative_to(resolved_daily_dir)
    return len(relative.parts) == 2 and path.suffix == ".md"


def validate_summary_links(
    summary_path: Path,
    topics_dir: Path,
    *,
    daily_dir: Path | None = None,
) -> list[str]:
    text, errors = read_text(summary_path)
    if text is None:
        return errors

    for link in extract_markdown_links(text):
        if is_external_url(link.target):
            continue

        resolved = resolve_local_link(summary_path, link.target)
        if resolved is None:
            errors.append(
                f"{summary_path}:{link.line}: link '{link.label}' must be an http(s) URL "
                "or a local topic note"
            )
            continue

        if is_topic_note_path(resolved, topics_dir):
            if not resolved.is_file():
                errors.append(
                    f"{summary_path}:{link.line}: linked topic note does not exist: {resolved}"
                )
            continue

        if daily_dir is not None and is_daily_summary_path(resolved, daily_dir):
            if not resolved.is_file():
                errors.append(
                    f"{summary_path}:{link.line}: linked daily summary does not exist: {resolved}"
                )
            continue

        if daily_dir is not None:
            errors.append(
                f"{summary_path}:{link.line}: local link '{link.label}' must point to "
                f"{topics_dir}/<topic-id>/notes/<note>.md or {daily_dir}/<year>/<name>.md"
            )
        else:
            errors.append(
                f"{summary_path}:{link.line}: local link '{link.label}' must point to "
                f"{topics_dir}/<topic-id>/notes/<note>.md"
            )
    return errors


def section_titles(text: str) -> set[str]:
    return {match.group(1).strip().lower() for match in H2_RE.finditer(text)}


def validate_topic_overview(overview_path: Path) -> list[str]:
    text, errors = read_text(overview_path)
    if text is None:
        return errors

    titles = section_titles(text)
    missing = sorted(REQUIRED_OVERVIEW_SECTIONS - titles)
    return [f"{overview_path}: missing required section '## {title.title()}'" for title in missing]


def discover_daily_summaries(daily_dir: Path) -> list[Path]:
    if not daily_dir.exists():
        return []
    return sorted(path for path in daily_dir.rglob("*.md") if path.is_file())


def discover_topic_overviews(topics_dir: Path) -> tuple[list[Path], list[str]]:
    if not topics_dir.exists():
        return [], []

    overviews: list[Path] = []
    errors: list[str] = []
    for topic_dir in sorted(path for path in topics_dir.iterdir() if path.is_dir()):
        if topic_dir.name.startswith("."):
            continue
        overview = topic_dir / "OVERVIEW.md"
        if overview.is_file():
            overviews.append(overview)
        else:
            errors.append(f"{topic_dir}: topic folder is missing OVERVIEW.md")
    return overviews, errors


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve(strict=False)
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def check_knowledge_links(
    daily_dir: Path = Path("KNOWLEDGE/daily"),
    topics_dir: Path = Path("KNOWLEDGE/topics"),
    daily_summaries: list[Path] | None = None,
    topic_overviews: list[Path] | None = None,
    fortnightly_dir: Path = Path("KNOWLEDGE/fortnightly"),
    topics_file: Path | None = None,
) -> list[str]:
    summaries = discover_daily_summaries(daily_dir)
    if daily_summaries:
        summaries.extend(daily_summaries)

    discovered_overviews, errors = discover_topic_overviews(topics_dir)
    overviews = discovered_overviews
    if topic_overviews:
        overviews.extend(topic_overviews)

    for summary_path in unique_paths(summaries):
        errors.extend(validate_summary_links(summary_path, topics_dir))
    for report_path in unique_paths(discover_daily_summaries(fortnightly_dir)):
        errors.extend(validate_summary_links(report_path, topics_dir, daily_dir=daily_dir))
    for overview_path in unique_paths(overviews):
        errors.extend(validate_topic_overview(overview_path))

    if topics_file is not None and topics_file.exists():
        topics, _ = parse_topics(topics_file)
        for topic in topics:
            if not (topics_dir / topic.topic_id / "OVERVIEW.md").is_file():
                errors.append(
                    f"{topics_file}: topic id '{topic.topic_id}' has no "
                    f"{topics_dir}/{topic.topic_id}/OVERVIEW.md"
                )
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate generated knowledge links.")
    parser.add_argument("--daily-dir", type=Path, default=Path("KNOWLEDGE/daily"))
    parser.add_argument("--topics-dir", type=Path, default=Path("KNOWLEDGE/topics"))
    parser.add_argument("--fortnightly-dir", type=Path, default=Path("KNOWLEDGE/fortnightly"))
    parser.add_argument("--topics-file", type=Path, default=Path("TOPICS.md"))
    parser.add_argument(
        "--daily-summary",
        action="append",
        type=Path,
        default=[],
        help="Additional daily summary file to validate. May be provided more than once.",
    )
    parser.add_argument(
        "--topic-overview",
        action="append",
        type=Path,
        default=[],
        help="Additional topic overview file to validate. May be provided more than once.",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print validation failures.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = check_knowledge_links(
        daily_dir=args.daily_dir,
        topics_dir=args.topics_dir,
        daily_summaries=args.daily_summary,
        topic_overviews=args.topic_overview,
        fortnightly_dir=args.fortnightly_dir,
        topics_file=args.topics_file,
    )

    if errors:
        print("Knowledge link checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if not args.quiet:
        print("Knowledge link checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
