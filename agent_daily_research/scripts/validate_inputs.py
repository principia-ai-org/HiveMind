#!/usr/bin/env python3
"""Validate knowledge workflow inputs.

The module is intentionally small and importable so the later pytest step can
exercise parsing and validation without shelling out.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DAY_NAMES = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)
TOPIC_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
QUESTION_ID_RE = re.compile(r"^Q-\d{4}-\d{2}-\d{2}-\d{3}$")
YAML_BLOCK_RE = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
DEFAULT_CONFIG_PATH = Path("config.yml")
RECYCLEBIN_CONFIG_KEYS = frozenset({"retention_days"})
EMAIL_CONFIG_KEYS = frozenset({"agent_name"})


@dataclass(frozen=True)
class MarkdownSection:
    title: str
    body: str
    line: int


@dataclass(frozen=True)
class Topic:
    title: str
    topic_id: str
    metadata: Mapping[str, Any]
    description: str
    line: int


@dataclass(frozen=True)
class Question:
    title: str
    question_id: str
    metadata: Mapping[str, Any]
    details: str
    line: int


def require_yaml() -> Any:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "PyYAML is required to validate config and Markdown YAML blocks. "
            "Install it in the environment before running this script."
        ) from exc
    return yaml


def read_text(path: Path) -> tuple[str | None, list[str]]:
    try:
        return path.read_text(encoding="utf-8"), []
    except FileNotFoundError:
        return None, [f"{path}: file does not exist"]
    except OSError as exc:
        return None, [f"{path}: could not read file: {exc}"]


def load_yaml_text(text: str, label: str) -> tuple[Any | None, list[str]]:
    yaml = require_yaml()
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return None, [f"{label}: invalid YAML: {exc}"]
    return data, []


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


def yaml_block_for_section(
    section: MarkdownSection, label: str
) -> tuple[Mapping[str, Any] | None, str, list[str]]:
    matches = list(YAML_BLOCK_RE.finditer(section.body))
    if len(matches) != 1:
        return (
            None,
            section.body.strip(),
            [
                f"{label}:{section.line}: section '{section.title}' must contain "
                f"exactly one yaml code block; found {len(matches)}"
            ],
        )

    data, errors = load_yaml_text(matches[0].group(1), f"{label}:{section.line}")
    description = (section.body[: matches[0].start()] + section.body[matches[0].end() :]).strip()
    if errors:
        return None, description, errors
    if not isinstance(data, Mapping):
        return None, description, [f"{label}:{section.line}: YAML block must be a mapping"]
    return data, description, []


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_int_range(
    value: Any,
    label: str,
    minimum: int,
    maximum: int,
    errors: list[str],
) -> None:
    if not is_int(value):
        errors.append(f"{label}: must be an integer")
        return
    if value < minimum or value > maximum:
        errors.append(f"{label}: must be between {minimum} and {maximum}")


def validate_day_mapping(
    value: Any,
    label: str,
    minimum: int,
    maximum: int,
    errors: list[str],
) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        errors.append(f"{label}: must be a mapping with one entry per weekday")
        return None

    keys = set(value)
    expected = set(DAY_NAMES)
    missing = sorted(expected - keys)
    extra = sorted(keys - expected)
    if missing:
        errors.append(f"{label}: missing weekdays: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: unknown weekdays: {', '.join(str(day) for day in extra)}")

    for day in DAY_NAMES:
        if day in value:
            validate_int_range(value[day], f"{label}.{day}", minimum, maximum, errors)
    return value


def parse_topics(path: Path) -> tuple[list[Topic], list[str]]:
    text, errors = read_text(path)
    if text is None:
        return [], errors

    sections = markdown_h2_sections(text)
    topics: list[Topic] = []
    seen_ids: dict[str, int] = {}
    for section in sections:
        metadata, description, section_errors = yaml_block_for_section(section, str(path))
        errors.extend(section_errors)
        if metadata is None:
            continue

        topic_id = metadata.get("id")
        if not isinstance(topic_id, str):
            errors.append(f"{path}:{section.line}: id must be a string")
            topic_id = ""
        elif not TOPIC_ID_RE.fullmatch(topic_id):
            errors.append(
                f"{path}:{section.line}: id '{topic_id}' must be lowercase kebab-case"
            )
        elif topic_id in seen_ids:
            errors.append(
                f"{path}:{section.line}: duplicate topic id '{topic_id}' "
                f"(first seen on line {seen_ids[topic_id]})"
            )
        else:
            seen_ids[topic_id] = section.line

        for required_key in ("id", "default_weight", "weekday_weights"):
            if required_key not in metadata:
                errors.append(f"{path}:{section.line}: missing required key '{required_key}'")

        if "default_weight" in metadata:
            validate_int_range(
                metadata["default_weight"],
                f"{path}:{section.line}: default_weight",
                0,
                10,
                errors,
            )
        if "weekday_weights" in metadata:
            validate_day_mapping(
                metadata["weekday_weights"],
                f"{path}:{section.line}: weekday_weights",
                0,
                10,
                errors,
            )

        min_items = metadata.get("daily_min_items")
        max_items = metadata.get("daily_max_items")
        if min_items is not None:
            validate_int_range(
                min_items,
                f"{path}:{section.line}: daily_min_items",
                0,
                100,
                errors,
            )
        if max_items is not None:
            validate_int_range(
                max_items,
                f"{path}:{section.line}: daily_max_items",
                0,
                100,
                errors,
            )
        if is_int(min_items) and is_int(max_items) and min_items > max_items:
            errors.append(f"{path}:{section.line}: daily_min_items cannot exceed daily_max_items")

        source_preferences = metadata.get("source_preferences")
        if source_preferences is not None:
            validate_source_preferences(source_preferences, f"{path}:{section.line}", errors)

        if not description:
            errors.append(f"{path}:{section.line}: topic description must not be empty")

        if topic_id:
            topics.append(
                Topic(
                    title=section.title,
                    topic_id=topic_id,
                    metadata=metadata,
                    description=description,
                    line=section.line,
                )
            )
    return topics, errors


def validate_source_preferences(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{label}: source_preferences must be a mapping")
        return
    for key in ("primary", "avoid"):
        if key not in value:
            continue
        items = value[key]
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            errors.append(f"{label}: source_preferences.{key} must be a list of strings")


def parse_questions(path: Path, valid_topic_ids: Iterable[str]) -> tuple[list[Question], list[str]]:
    text, errors = read_text(path)
    if text is None:
        return [], errors

    valid_topics = set(valid_topic_ids)
    sections = markdown_h2_sections(text)
    questions: list[Question] = []
    seen_ids: dict[str, int] = {}
    for section in sections:
        question_id, question_title = parse_question_heading(section.title)
        if question_id is None:
            errors.append(
                f"{path}:{section.line}: question heading must start with "
                "'Q-YYYY-MM-DD-NNN: '"
            )
            question_id = ""
            question_title = section.title
        elif question_id in seen_ids:
            errors.append(
                f"{path}:{section.line}: duplicate question id '{question_id}' "
                f"(first seen on line {seen_ids[question_id]})"
            )
        else:
            seen_ids[question_id] = section.line

        metadata, details, section_errors = yaml_block_for_section(section, str(path))
        errors.extend(section_errors)
        if metadata is None:
            continue

        status = metadata.get("status")
        if not isinstance(status, str):
            errors.append(f"{path}:{section.line}: status must be a string")
            status = ""

        if status == "active":
            validate_active_question(
                metadata,
                details,
                question_title,
                valid_topics,
                f"{path}:{section.line}",
                errors,
            )
        elif status and status not in {"inactive", "paused", "answered", "archived"}:
            errors.append(
                f"{path}:{section.line}: status must be active, inactive, paused, "
                "answered, or archived"
            )

        if question_id:
            questions.append(
                Question(
                    title=question_title,
                    question_id=question_id,
                    metadata=metadata,
                    details=details,
                    line=section.line,
                )
            )
    return questions, errors


def parse_question_heading(title: str) -> tuple[str | None, str]:
    if ": " not in title:
        return None, title.strip()
    question_id, question_title = title.split(": ", 1)
    if not QUESTION_ID_RE.fullmatch(question_id):
        return None, question_title.strip()
    return question_id, question_title.strip()


def validate_active_question(
    metadata: Mapping[str, Any],
    details: str,
    title: str,
    valid_topic_ids: set[str],
    label: str,
    errors: list[str],
) -> None:
    for required_key in ("priority", "topics", "created"):
        if required_key not in metadata:
            errors.append(f"{label}: active question missing required key '{required_key}'")

    if "priority" in metadata:
        validate_int_range(metadata["priority"], f"{label}: priority", 1, 10, errors)

    topics = metadata.get("topics")
    if not isinstance(topics, list) or not topics:
        errors.append(f"{label}: topics must be a non-empty list")
    else:
        seen_topics: set[str] = set()
        for topic_id in topics:
            if not isinstance(topic_id, str):
                errors.append(f"{label}: topics entries must be strings")
                continue
            if topic_id not in valid_topic_ids:
                errors.append(f"{label}: unknown topic id '{topic_id}'")
            if topic_id in seen_topics:
                errors.append(f"{label}: duplicate topic id '{topic_id}' in question topics")
            seen_topics.add(topic_id)

    if "created" in metadata and not is_iso_date(metadata["created"]):
        errors.append(f"{label}: created must be an ISO date in YYYY-MM-DD form")
    if not title:
        errors.append(f"{label}: active question title must not be empty")
    if not details:
        errors.append(f"{label}: active question detail must not be empty")


def is_iso_date(value: Any) -> bool:
    if isinstance(value, datetime):
        return False
    if isinstance(value, date):
        return True
    if not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_config(path: Path) -> list[str]:
    text, errors = read_text(path)
    if text is None:
        return errors

    data, yaml_errors = load_yaml_text(text, str(path))
    errors.extend(yaml_errors)
    if yaml_errors:
        return errors
    if not isinstance(data, Mapping):
        return [f"{path}: root must be a mapping"]

    validate_top_level_config(data, str(path), errors)
    return errors


def validate_recyclebin_config(
    recyclebin: Mapping[str, Any], label: str, errors: list[str]
) -> None:
    for key in sorted(set(recyclebin) - RECYCLEBIN_CONFIG_KEYS):
        errors.append(f"{label}: unknown recyclebin config key '{key}'")

    if "retention_days" not in recyclebin:
        errors.append(f"{label}: missing required key 'retention_days'")
    else:
        validate_int_range(recyclebin["retention_days"], f"{label}.retention_days", 1, 3650, errors)


def validate_email_config(email: Mapping[str, Any], label: str, errors: list[str]) -> None:
    for key in sorted(set(email) - EMAIL_CONFIG_KEYS):
        errors.append(f"{label}: unknown email config key '{key}'")

    agent_name = email.get("agent_name")
    if not isinstance(agent_name, str) or not agent_name.strip():
        errors.append(f"{label}.agent_name: must be a non-empty string")


def validate_top_level_config(config: Mapping[str, Any], label: str, errors: list[str]) -> None:
    for key in ("timezone", "daily", "fortnightly", "quality", "recyclebin", "email"):
        if key not in config:
            errors.append(f"{label}: missing required key '{key}'")

    timezone = config.get("timezone")
    if not isinstance(timezone, str) or not timezone:
        errors.append(f"{label}: timezone must be a non-empty string")
    else:
        try:
            ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            errors.append(f"{label}: timezone '{timezone}' is not recognized")

    daily_totals: Mapping[str, Any] | None = None
    daily_notes: Mapping[str, Any] | None = None
    daily = config.get("daily")
    if isinstance(daily, Mapping):
        daily_totals, daily_notes = validate_daily_config(daily, f"{label}: daily", errors)
    elif "daily" in config:
        errors.append(f"{label}: daily must be a mapping")

    fortnightly = config.get("fortnightly")
    if isinstance(fortnightly, Mapping):
        validate_fortnightly_config(fortnightly, f"{label}: fortnightly", errors)
    elif "fortnightly" in config:
        errors.append(f"{label}: fortnightly must be a mapping")

    quality = config.get("quality")
    if isinstance(quality, Mapping):
        validate_quality_config(quality, f"{label}: quality", errors)
    elif "quality" in config:
        errors.append(f"{label}: quality must be a mapping")

    recyclebin = config.get("recyclebin")
    if isinstance(recyclebin, Mapping):
        validate_recyclebin_config(recyclebin, f"{label}: recyclebin", errors)
    elif "recyclebin" in config:
        errors.append(f"{label}: recyclebin must be a mapping")

    email = config.get("email")
    if isinstance(email, Mapping):
        validate_email_config(email, f"{label}: email", errors)
    elif "email" in config:
        errors.append(f"{label}: email must be a mapping")

    if daily_totals and daily_notes:
        for day in DAY_NAMES:
            if is_int(daily_totals.get(day)) and is_int(daily_notes.get(day)):
                if daily_notes[day] > daily_totals[day]:
                    errors.append(
                        f"{label}: daily.max_topic_notes_by_weekday.{day} cannot exceed "
                        f"daily.max_total_items_by_weekday.{day}"
                    )


def validate_daily_config(
    daily: Mapping[str, Any], label: str, errors: list[str]
) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
    totals = validate_day_mapping(
        daily.get("max_total_items_by_weekday"),
        f"{label}.max_total_items_by_weekday",
        0,
        100,
        errors,
    )
    notes = validate_day_mapping(
        daily.get("max_topic_notes_by_weekday"),
        f"{label}.max_topic_notes_by_weekday",
        0,
        100,
        errors,
    )
    return totals, notes


def validate_fortnightly_config(
    fortnightly: Mapping[str, Any], label: str, errors: list[str]
) -> None:
    if not is_iso_date(fortnightly.get("anchor_date")):
        errors.append(f"{label}.anchor_date: must be an ISO date in YYYY-MM-DD form")
    validate_int_range(fortnightly.get("interval_days"), f"{label}.interval_days", 1, 366, errors)
    validate_int_range(fortnightly.get("lookback_days"), f"{label}.lookback_days", 1, 366, errors)


def validate_quality_config(quality: Mapping[str, Any], label: str, errors: list[str]) -> None:
    if not isinstance(quality.get("require_links_for_factual_claims"), bool):
        errors.append(f"{label}.require_links_for_factual_claims: must be true or false")
    validate_int_range(
        quality.get("min_primary_sources_for_high_confidence"),
        f"{label}.min_primary_sources_for_high_confidence",
        0,
        10,
        errors,
    )
    validate_int_range(
        quality.get("max_overview_words"),
        f"{label}.max_overview_words",
        50,
        5000,
        errors,
    )


def validate_inputs(
    topics_path: Path = Path("TOPICS.md"),
    questions_path: Path = Path("QUESTIONS.md"),
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> list[str]:
    topics, topic_errors = parse_topics(topics_path)
    topic_ids = [topic.topic_id for topic in topics if TOPIC_ID_RE.fullmatch(topic.topic_id)]
    _, question_errors = parse_questions(questions_path, topic_ids)
    config_errors = validate_config(config_path)
    return topic_errors + question_errors + config_errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate knowledge workflow inputs.")
    parser.add_argument("--topics", type=Path, default=Path("TOPICS.md"))
    parser.add_argument("--questions", type=Path, default=Path("QUESTIONS.md"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--quiet", action="store_true", help="Only print validation failures.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        errors = validate_inputs(
            args.topics,
            args.questions,
            args.config,
        )
    except RuntimeError as exc:
        print(f"Input validation could not run: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("Input validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if not args.quiet:
        print("Input validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
