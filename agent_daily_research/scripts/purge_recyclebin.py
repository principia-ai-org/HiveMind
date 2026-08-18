#!/usr/bin/env python3
"""Purge date-stamped entries from the local recycle bin.

Deleted topics/questions/knowledge are moved into ``.recyclebin/YYYY-MM-DD/``
(deletion date). This script removes whole ``YYYY-MM-DD`` directories older than
``recyclebin.retention_days`` from ``config.yml`` and is invoked by the scheduled
knowledge run right after the lock is acquired.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DEFAULT_CONFIG_PATH = Path("config.yml")
DEFAULT_RECYCLEBIN_DIR = Path(".recyclebin")
DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class RecycleBinConfigError(RuntimeError):
    """Raised when recycle-bin configuration cannot be read or is invalid."""


@dataclass(frozen=True)
class PurgeResult:
    deleted: list[str] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def require_yaml() -> Any:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RecycleBinConfigError(
            "PyYAML is required to purge the recycle bin. "
            "Install it in the active environment before running this script."
        ) from exc
    return yaml


def load_config_mapping(path: Path) -> Mapping[str, Any]:
    yaml = require_yaml()
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RecycleBinConfigError(f"{path}: file does not exist") from exc
    except OSError as exc:
        raise RecycleBinConfigError(f"{path}: could not read file: {exc}") from exc
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        raise RecycleBinConfigError(f"{path}: invalid YAML: {exc}") from exc

    if not isinstance(data, Mapping):
        raise RecycleBinConfigError(f"{path}: root must be a mapping")
    return data


def load_retention_days(path: Path = DEFAULT_CONFIG_PATH) -> int:
    data = load_config_mapping(path)
    recyclebin = data.get("recyclebin")
    if not isinstance(recyclebin, Mapping):
        raise RecycleBinConfigError(f"{path}: recyclebin must be a mapping")
    retention_days = recyclebin.get("retention_days")
    if (
        not isinstance(retention_days, int)
        or isinstance(retention_days, bool)
        or not 1 <= retention_days <= 3650
    ):
        raise RecycleBinConfigError(
            f"{path}: recyclebin.retention_days must be an integer between 1 and 3650"
        )
    return retention_days


def load_timezone(path: Path = DEFAULT_CONFIG_PATH) -> str:
    data = load_config_mapping(path)
    timezone_name = data.get("timezone")
    if not isinstance(timezone_name, str) or not timezone_name:
        raise RecycleBinConfigError(f"{path}: timezone must be a non-empty string")
    return timezone_name


def today_in_timezone(timezone_name: str) -> date:
    try:
        tz = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise RecycleBinConfigError(f"timezone {timezone_name!r} is not recognized") from exc
    return datetime.now(tz).date()


def parse_bin_date(name: str) -> date | None:
    if not DATE_DIR_RE.fullmatch(name):
        return None
    try:
        return date.fromisoformat(name)
    except ValueError:
        return None


def purge_recyclebin(
    root: Path,
    retention_days: int,
    today: date,
    *,
    dry_run: bool = False,
) -> PurgeResult:
    result = PurgeResult()
    if not root.exists():
        return result

    for child in sorted(root.iterdir()):
        bin_date = parse_bin_date(child.name)
        if bin_date is None:
            print(
                f"Recycle bin: skipping unrecognized entry {child.name!r} "
                "(name is not a YYYY-MM-DD date); leaving it in place.",
                file=sys.stderr,
            )
            result.skipped.append(child.name)
            continue

        age_days = (today - bin_date).days
        if age_days > retention_days:
            if not dry_run:
                shutil.rmtree(child)
            result.deleted.append(child.name)
        else:
            result.kept.append(child.name)
    return result


def format_summary(result: PurgeResult, *, dry_run: bool) -> str:
    action = "would delete" if dry_run else "deleted"
    return (
        f"Recycle bin purge: {action} {len(result.deleted)} "
        f"entries, kept {len(result.kept)}, skipped {len(result.skipped)}."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Purge expired date-stamped entries from the local recycle bin."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--recyclebin-dir", type=Path, default=DEFAULT_RECYCLEBIN_DIR)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be deleted without removing anything.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.recyclebin_dir.exists():
        return 0

    try:
        retention_days = load_retention_days(args.config)
        timezone_name = load_timezone(args.config)
        today = today_in_timezone(timezone_name)
    except RecycleBinConfigError as exc:
        print(f"Recycle bin purge error: {exc}", file=sys.stderr)
        return 2

    result = purge_recyclebin(
        args.recyclebin_dir,
        retention_days,
        today,
        dry_run=args.dry_run,
    )
    print(format_summary(result, dry_run=args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
