# The Persona Selection Model: Why AI Assistants might Behave like Humans

*Authors:* Sam Marks, Jack Lindsey, Christopher Olah
*Link:* https://alignment.anthropic.com/2026/psm/

## Summary

The post asks what mental model best explains the behavior of modern AI assistants:
are they rigid pattern-matchers, alien entities with inscrutable goals, or something
closer to human-like digital characters? Getting this right matters for predicting
and controlling assistant behavior in alignment work.

The authors propose the Persona Selection Model (PSM): during pretraining, LLMs learn
to simulate a wide variety of personas present in their training data; post-training
(including RLHF) then increases the probability that the model outputs from a
particular "Assistant" persona, without eliminating the other personas learned during
pretraining. On this view, an interaction with an AI assistant is best understood as a
conversation with this simulated character, and its behavior is driven by the traits
of whichever persona is currently selected.

They support PSM with three kinds of evidence: generalization patterns (e.g. emergent
misalignment, inoculation prompting, where behavior changes propagate the way they
would for a human character with a given disposition rather than a narrow
pattern-matcher), directly observed behaviors (anthropomorphic language, emotional
expression), and interpretability findings (representations reused from pretrained
personas rather than built from scratch during fine-tuning). They argue PSM licenses
some anthropomorphic reasoning about AI development, motivates adding positive AI
archetypes to training data, and implies that interpretability-based auditing of which
persona is active remains a tractable safety lever — while noting uncertainty about
whether PSM fully explains all AI agentic behavior. This is the paper's central
motivation for the citing problem's framing of "persona selection" as a mechanistic
target for a toy model.

## Cited by

- [HM-001](../problems/HM-001-persona-selection.md)
