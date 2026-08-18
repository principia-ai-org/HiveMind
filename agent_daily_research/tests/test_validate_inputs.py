from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from scripts.validate_inputs import (
    parse_questions,
    parse_topics,
    validate_config,
    validate_inputs,
)


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
daily_min_items: 0
daily_max_items: 3
source_preferences:
  primary:
    - official project blogs
    - papers and preprints
  avoid:
    - unsourced social reposts
```

Track proof assistants, theorem-proving benchmarks, and formal verification work.

## AI Research and Tooling

```yaml
id: ai-research
default_weight: 7
weekday_weights:
  monday: 8
  tuesday: 8
  wednesday: 7
  thursday: 7
  friday: 6
  saturday: 4
  sunday: 4
daily_min_items: 0
daily_max_items: 2
```

Track model capability updates, agent workflows, and evaluation methods.
"""

QUESTIONS_MD = """
# QUESTIONS.md

## Q-2026-07-08-001: Are theorem-proving systems improving on hard benchmarks?

```yaml
status: active
priority: 9
topics: [formalisation, ai-research]
created: 2026-07-08
```

Focus on benchmark results, replications, and expert critiques.
"""

CONFIG_YML = """
timezone: "Etc/UTC"

daily:
  max_total_items_by_weekday:
    monday: 12
    tuesday: 10
    wednesday: 10
    thursday: 10
    friday: 8
    saturday: 5
    sunday: 5
  max_topic_notes_by_weekday:
    monday: 5
    tuesday: 4
    wednesday: 4
    thursday: 4
    friday: 3
    saturday: 2
    sunday: 2

fortnightly:
  anchor_date: "2026-07-08"
  interval_days: 14
  lookback_days: 14

quality:
  require_links_for_factual_claims: true
  min_primary_sources_for_high_confidence: 1
  max_overview_words: 500

recyclebin:
  retention_days: 30

email:
  agent_name: "Test Agent"
"""


def write_fixture(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")
    return path


def valid_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    topics_path = write_fixture(tmp_path / "TOPICS.md", TOPICS_MD)
    questions_path = write_fixture(tmp_path / "QUESTIONS.md", QUESTIONS_MD)
    config_path = write_fixture(tmp_path / "config.yml", CONFIG_YML)
    return topics_path, questions_path, config_path


def test_parses_markdown_yaml_topics_and_questions(tmp_path: Path) -> None:
    topics_path, questions_path, _ = valid_inputs(tmp_path)

    topics, topic_errors = parse_topics(topics_path)
    assert topic_errors == []
    assert [topic.topic_id for topic in topics] == ["formalisation", "ai-research"]
    assert topics[0].metadata["weekday_weights"]["monday"] == 10
    assert "theorem-proving benchmarks" in topics[0].description

    questions, question_errors = parse_questions(
        questions_path,
        [topic.topic_id for topic in topics],
    )
    assert question_errors == []
    assert [question.question_id for question in questions] == ["Q-2026-07-08-001"]
    assert questions[0].metadata["topics"] == ["formalisation", "ai-research"]
    assert "replications" in questions[0].details


def test_validate_inputs_accepts_valid_fixture(tmp_path: Path) -> None:
    topics_path, questions_path, config_path = valid_inputs(tmp_path)

    assert validate_inputs(topics_path, questions_path, config_path) == []


def test_validate_config_reports_invalid_values(tmp_path: Path) -> None:
    config_path = write_fixture(
        tmp_path / "config.yml",
        CONFIG_YML.replace('timezone: "Etc/UTC"', 'timezone: "Not/AZone"')
        .replace("interval_days: 14", "interval_days: 0")
        .replace("max_overview_words: 500", "max_overview_words: 20")
        .replace("retention_days: 30", "retention_days: 0")
        .replace('agent_name: "Test Agent"', 'agent_name: ""'),
    )

    errors = validate_config(config_path)

    assert any("timezone 'Not/AZone' is not recognized" in error for error in errors)
    assert any("fortnightly.interval_days: must be between 1 and 366" in error for error in errors)
    assert any("max_overview_words: must be between 50 and 5000" in error for error in errors)
    assert any(
        "recyclebin.retention_days: must be between 1 and 3650" in error for error in errors
    )
    assert any("email.agent_name: must be a non-empty string" in error for error in errors)


def test_validate_config_requires_recyclebin_and_email_sections(tmp_path: Path) -> None:
    config_path = write_fixture(
        tmp_path / "config.yml",
        CONFIG_YML.split("recyclebin:")[0],
    )

    errors = validate_config(config_path)

    assert any("missing required key 'recyclebin'" in error for error in errors)
    assert any("missing required key 'email'" in error for error in errors)
