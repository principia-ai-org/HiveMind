from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from scripts.check_knowledge_links import check_knowledge_links


TOPICS_MD = """
# TOPICS.md

## Formalisation and Proof Assistants

```yaml
id: formalisation
default_weight: 8
weekday_weights:
  monday: 10
  tuesday: 8
  wednesday: 8
  thursday: 8
  friday: 7
  saturday: 5
  sunday: 4
```

Track proof assistants and theorem-proving benchmarks.
"""


def write_fixture(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")
    return path


def knowledge_tree(tmp_path: Path) -> tuple[Path, Path, Path]:
    daily_dir = tmp_path / "KNOWLEDGE" / "daily"
    topics_dir = tmp_path / "KNOWLEDGE" / "topics"
    note_path = topics_dir / "formalisation" / "notes" / "2026-07-08-proof-search.md"

    write_fixture(
        topics_dir / "formalisation" / "OVERVIEW.md",
        """
        # Formalisation and Proof Assistants

        ## Short Summary

        Tracks theorem-proving benchmarks.

        ## Notes Index

        - 2026-07-08: [Proof Search](notes/2026-07-08-proof-search.md)
        """,
    )
    write_fixture(
        note_path,
        """
        # Proof Search

        ## Summary

        A durable benchmark note.
        """,
    )
    return daily_dir, topics_dir, note_path


def test_check_knowledge_links_accepts_existing_topic_note_and_external_url(
    tmp_path: Path,
) -> None:
    daily_dir, topics_dir, _ = knowledge_tree(tmp_path)
    write_fixture(
        daily_dir / "2026" / "2026-07-08.md",
        """
        # Daily Knowledge Summary: 2026-07-08

        ## Topic Notes Created

        - [Proof Search](../../topics/formalisation/notes/2026-07-08-proof-search.md)

        ## Sources and Confidence

        - [Project note](https://example.com/project-note)
        """,
    )

    assert check_knowledge_links(daily_dir=daily_dir, topics_dir=topics_dir) == []


def test_check_knowledge_links_rejects_missing_topic_note(tmp_path: Path) -> None:
    daily_dir, topics_dir, _ = knowledge_tree(tmp_path)
    write_fixture(
        daily_dir / "2026" / "2026-07-08.md",
        """
        # Daily Knowledge Summary: 2026-07-08

        ## Topic Notes Created

        - [Missing Note](../../topics/formalisation/notes/2026-07-08-missing.md)
        """,
    )

    errors = check_knowledge_links(daily_dir=daily_dir, topics_dir=topics_dir)

    assert any("linked topic note does not exist" in error for error in errors)


def test_check_knowledge_links_requires_overview_sections(tmp_path: Path) -> None:
    daily_dir = tmp_path / "KNOWLEDGE" / "daily"
    topics_dir = tmp_path / "KNOWLEDGE" / "topics"
    write_fixture(
        topics_dir / "formalisation" / "OVERVIEW.md",
        """
        # Formalisation and Proof Assistants

        ## Short Summary

        Tracks theorem-proving benchmarks.
        """,
    )

    errors = check_knowledge_links(daily_dir=daily_dir, topics_dir=topics_dir)

    assert any("missing required section '## Notes Index'" in error for error in errors)


def test_check_knowledge_links_accepts_fortnightly_link_to_daily_summary(
    tmp_path: Path,
) -> None:
    daily_dir, topics_dir, _ = knowledge_tree(tmp_path)
    write_fixture(
        daily_dir / "2026" / "2026-07-08.md",
        """
        # Daily Knowledge Summary: 2026-07-08

        ## Highlights

        - One deterministic fixture item.
        """,
    )
    fortnightly_dir = tmp_path / "KNOWLEDGE" / "fortnightly"
    write_fixture(
        fortnightly_dir / "2026" / "2026-07-01_to_2026-07-14.md",
        """
        # Fortnightly Report: 2026-07-01 to 2026-07-14

        ## Daily Summaries

        - [2026-07-08](../../daily/2026/2026-07-08.md)
        """,
    )

    assert (
        check_knowledge_links(
            daily_dir=daily_dir,
            topics_dir=topics_dir,
            fortnightly_dir=fortnightly_dir,
        )
        == []
    )


def test_check_knowledge_links_rejects_fortnightly_link_to_missing_daily_summary(
    tmp_path: Path,
) -> None:
    daily_dir, topics_dir, _ = knowledge_tree(tmp_path)
    fortnightly_dir = tmp_path / "KNOWLEDGE" / "fortnightly"
    write_fixture(
        fortnightly_dir / "2026" / "2026-07-01_to_2026-07-14.md",
        """
        # Fortnightly Report: 2026-07-01 to 2026-07-14

        ## Daily Summaries

        - [2026-07-09](../../daily/2026/2026-07-09.md)
        """,
    )

    errors = check_knowledge_links(
        daily_dir=daily_dir,
        topics_dir=topics_dir,
        fortnightly_dir=fortnightly_dir,
    )

    assert any("linked daily summary does not exist" in error for error in errors)


def test_check_knowledge_links_reports_topic_id_without_overview(tmp_path: Path) -> None:
    daily_dir, topics_dir, _ = knowledge_tree(tmp_path)
    topics_file = write_fixture(
        tmp_path / "TOPICS.md",
        TOPICS_MD.replace("id: formalisation", "id: missing-topic"),
    )

    errors = check_knowledge_links(
        daily_dir=daily_dir,
        topics_dir=topics_dir,
        fortnightly_dir=tmp_path / "KNOWLEDGE" / "fortnightly",
        topics_file=topics_file,
    )

    assert any(
        "topic id 'missing-topic' has no" in error and "OVERVIEW.md" in error
        for error in errors
    )


def test_check_knowledge_links_topic_id_with_overview_passes(tmp_path: Path) -> None:
    daily_dir, topics_dir, _ = knowledge_tree(tmp_path)
    topics_file = write_fixture(tmp_path / "TOPICS.md", TOPICS_MD)

    assert (
        check_knowledge_links(
            daily_dir=daily_dir,
            topics_dir=topics_dir,
            fortnightly_dir=tmp_path / "KNOWLEDGE" / "fortnightly",
            topics_file=topics_file,
        )
        == []
    )
