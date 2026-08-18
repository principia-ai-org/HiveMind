from __future__ import annotations

import pytest

from scripts.extract_overview import OverviewError, extract_overview


def test_extracts_daily_overview() -> None:
    markdown = """# Daily Knowledge Summary: 2026-07-08

## Overview

A quiet day: two leads, neither durable.

- **Formalisation:** one medium-confidence benchmark update.
- **AI Research:** one low-confidence workflow signal.

## Highlights

- No durable topic notes were created.
"""

    overview = extract_overview(markdown, "daily.md")

    assert overview == (
        "A quiet day: two leads, neither durable.\n"
        "\n"
        "- **Formalisation:** one medium-confidence benchmark update.\n"
        "- **AI Research:** one low-confidence workflow signal."
    )


def test_extracts_fortnightly_overview() -> None:
    markdown = """# Fortnightly Knowledge Review: 2026-07-01 to 2026-07-14

## Overview
Across the window, formalisation updates were benchmark-centered, AI tooling
claims remained unevenly sourced, and no durable conflicts were found.

## What Was Gathered

- 7 daily summaries were scanned.
"""

    overview = extract_overview(markdown, "fortnightly.md")

    assert overview == (
        "Across the window, formalisation updates were benchmark-centered, AI tooling\n"
        "claims remained unevenly sourced, and no durable conflicts were found."
    )


def test_keeps_blank_lines_and_dividers() -> None:
    markdown = """# Daily Knowledge Summary: 2026-07-08

## Overview

Six items today; two durable.

- **Infra:** one repository-level kernel-optimization agent.

---

- **Formalisation:** no Lean-specific update in the window.

## Highlights

- Nothing further.
"""

    overview = extract_overview(markdown, "daily.md")

    assert overview == (
        "Six items today; two durable.\n"
        "\n"
        "- **Infra:** one repository-level kernel-optimization agent.\n"
        "\n"
        "---\n"
        "\n"
        "- **Formalisation:** no Lean-specific update in the window."
    )


def test_rejects_empty_overview() -> None:
    markdown = """# Daily Knowledge Summary: 2026-07-08

## Overview

## Highlights

- Nothing.
"""

    with pytest.raises(OverviewError, match="must not be empty"):
        extract_overview(markdown, "daily.md")
