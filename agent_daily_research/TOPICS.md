# TOPICS.md

Maintain durable topics here. Each topic section must contain exactly one YAML block followed by a short plain-language description.

## Formalisation and Proof Assistants

```yaml
id: formalisation
default_weight: 8
weekday_weights:
  monday: 8
  tuesday: 8
  wednesday: 8
  thursday: 8
  friday: 8
  saturday: 8
  sunday: 8
daily_min_items: 0
daily_max_items: 5
source_preferences:
  primary:
    - official project blogs
    - papers and preprints
    - GitHub releases
    - X (Twitter) — authoritative accounts only, as an intermediate lead to credible primary sources
  avoid:
    - unsourced social reposts
```

Track Lean, Rocq/Coq, Isabelle, HOL Light, mathlib, proof search, autoformalisation, theorem-proving benchmarks, and formal verification work.

## AI Research and Tooling

```yaml
id: ai-research
default_weight: 5
weekday_weights:
  monday: 5
  tuesday: 5
  wednesday: 5
  thursday: 5
  friday: 5
  saturday: 5
  sunday: 5
daily_min_items: 0
daily_max_items: 5
source_preferences:
  primary:
    - research papers
    - model release notes
    - reproducible evaluation writeups
    - X (Twitter) — authoritative accounts only, as an intermediate lead to credible primary sources
  avoid:
    - rumor threads
    - claims without linked artifacts
```

Track model capability updates, agent workflows, evaluation methods, developer tooling, and evidence about what is becoming practically repeatable.

## AI for Maths

```yaml
id: ai-for-maths
default_weight: 4
weekday_weights:
  monday: 4
  tuesday: 4
  wednesday: 4
  thursday: 4
  friday: 4
  saturday: 4
  sunday: 4
daily_min_items: 0
daily_max_items: 5
source_preferences:
  primary:
    - research papers and preprints
    - benchmark results and writeups
    - X (Twitter) — authoritative accounts only, as an intermediate lead to credible primary sources
  avoid:
    - claims without linked artifacts
```

Track AI applied to mathematics, with emphasis on probability, statistics, optimisation, applied mathematics, and machine learning — new methods, benchmarks, and tools where AI advances or accelerates mathematical work in these areas.

## Local and Cloud LLM Infra

```yaml
id: local-and-cloud-llm-infra
default_weight: 5
weekday_weights:
  monday: 5
  tuesday: 5
  wednesday: 5
  thursday: 5
  friday: 5
  saturday: 5
  sunday: 5
daily_min_items: 0
daily_max_items: 3
source_preferences:
  primary:
    - engineering blogs
    - official docs and release notes
    - reproducible benchmarks
    - X (Twitter) — authoritative accounts only, as an intermediate lead to credible primary sources
  avoid:
    - unsourced performance claims
```

Track infrastructure for running LLMs locally and in the cloud, with preference for cost-efficient approaches to inference and fine-tuning, and for understanding security, software compatibility, and speed issues (e.g. quantization, memory footprint, serving throughput).

## Code Translation

```yaml
id: code-translation
default_weight: 7
weekday_weights:
  monday: 7
  tuesday: 7
  wednesday: 7
  thursday: 7
  friday: 7
  saturday: 7
  sunday: 7
daily_min_items: 0
daily_max_items: 5
source_preferences:
  primary:
    - research papers and preprints
    - industry case studies
    - product and release announcements
    - X (Twitter) — authoritative accounts only, as an intermediate lead to credible primary sources
  avoid:
    - marketing content without technical detail
```

Track translation of code between programming languages, covering both market demand (industry adoption, legacy modernization projects, commercial offerings) and technical progress (models, transpilers, benchmarks, correctness and verification methods).

## RL Environment

```yaml
id: rl-environment
default_weight: 4
weekday_weights:
  monday: 4
  tuesday: 4
  wednesday: 4
  thursday: 4
  friday: 4
  saturday: 4
  sunday: 4
daily_min_items: 0
daily_max_items: 5
source_preferences:
  primary:
    - research papers and preprints
    - environment and benchmark releases
    - company announcements
    - X (Twitter) — authoritative accounts only, as an intermediate lead to credible primary sources
  avoid:
    - rumor threads
```

Track RL environments for training and evaluating models, with emphasis on judging and grading criteria (reward design, rubrics, verifiers, auto-graders) and on the kinds of tasks environments focus on, covering both market demands and technical progress.
