from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from scripts.purge_recyclebin import (
    RecycleBinConfigError,
    load_retention_days,
    main,
    purge_recyclebin,
)


TODAY = date(2026, 7, 16)
RETENTION_DAYS = 30


def make_bin_dir(root: Path, name: str) -> Path:
    entry = root / name
    entry.mkdir(parents=True)
    (entry / "marker.txt").write_text("content\n", encoding="utf-8")
    return entry


def test_old_directory_is_purged(tmp_path: Path) -> None:
    root = tmp_path / ".recyclebin"
    old = make_bin_dir(root, (TODAY - timedelta(days=RETENTION_DAYS + 1)).isoformat())

    result = purge_recyclebin(root, RETENTION_DAYS, TODAY)

    assert not old.exists()
    assert result.deleted == [old.name]
    assert result.kept == []


def test_recent_directory_is_kept(tmp_path: Path) -> None:
    root = tmp_path / ".recyclebin"
    recent = make_bin_dir(root, (TODAY - timedelta(days=5)).isoformat())

    result = purge_recyclebin(root, RETENTION_DAYS, TODAY)

    assert recent.exists()
    assert result.kept == [recent.name]
    assert result.deleted == []


def test_boundary_day_is_kept(tmp_path: Path) -> None:
    root = tmp_path / ".recyclebin"
    boundary = make_bin_dir(root, (TODAY - timedelta(days=RETENTION_DAYS)).isoformat())

    result = purge_recyclebin(root, RETENTION_DAYS, TODAY)

    assert boundary.exists()
    assert result.kept == [boundary.name]
    assert result.deleted == []


def test_unparseable_name_is_kept_and_warned(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / ".recyclebin"
    keep_me = make_bin_dir(root, "not-a-date")
    invalid_date = make_bin_dir(root, "2026-13-01")

    result = purge_recyclebin(root, RETENTION_DAYS, TODAY)

    assert keep_me.exists()
    assert invalid_date.exists()
    assert sorted(result.skipped) == ["2026-13-01", "not-a-date"]
    assert result.deleted == []
    captured = capsys.readouterr()
    assert "not-a-date" in captured.err
    assert "2026-13-01" in captured.err


def test_missing_root_is_a_no_op(tmp_path: Path) -> None:
    root = tmp_path / ".recyclebin"

    result = purge_recyclebin(root, RETENTION_DAYS, TODAY)

    assert result.deleted == []
    assert result.kept == []
    assert result.skipped == []


def test_dry_run_deletes_nothing(tmp_path: Path) -> None:
    root = tmp_path / ".recyclebin"
    old = make_bin_dir(root, (TODAY - timedelta(days=RETENTION_DAYS + 1)).isoformat())

    result = purge_recyclebin(root, RETENTION_DAYS, TODAY, dry_run=True)

    assert old.exists()
    assert result.deleted == [old.name]


def test_load_retention_days_rejects_invalid(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text("recyclebin:\n  retention_days: 0\n", encoding="utf-8")

    with pytest.raises(RecycleBinConfigError):
        load_retention_days(config_path)


def test_load_retention_days_requires_recyclebin_section(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text('timezone: "Etc/UTC"\n', encoding="utf-8")

    with pytest.raises(RecycleBinConfigError):
        load_retention_days(config_path)


def test_load_retention_days_requires_file(tmp_path: Path) -> None:
    with pytest.raises(RecycleBinConfigError):
        load_retention_days(tmp_path / "missing.yml")


def test_main_missing_recyclebin_dir_exits_zero_silently(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["--recyclebin-dir", str(tmp_path / ".recyclebin")])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == ""
    assert captured.err == ""


def test_main_dry_run_reports_would_delete(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        'timezone: "Etc/UTC"\nrecyclebin:\n  retention_days: 30\n',
        encoding="utf-8",
    )
    root = tmp_path / ".recyclebin"
    old = make_bin_dir(root, "2020-01-01")

    exit_code = main(
        [
            "--config",
            str(config_path),
            "--recyclebin-dir",
            str(root),
            "--dry-run",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert old.exists()
    assert "would delete 1 entries" in captured.out
