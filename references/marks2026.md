# The Persona Selection Model: Why AI Assistants might Behave like Humans

*Authors:* Sam Marks, Jack Lindsey, Christopher Olah
*Link:* https://alignment.anthropic.com/2026/psm/

## Summary

This post proposes the Persona Selection Model (PSM) as a mental model for how deployed
AI assistants behave. It argues that during pre-training an LLM learns to simulate many
different characters ("personas") present in its training data, and that post-training
(including RLHF) mainly acts to make the model reliably select and stay in one particular
persona — the "Assistant" — rather than installing qualitatively new behavior or goals.
On this view, most of what an assistant does can be explained by the traits of that
simulated Assistant character, rather than by treating the model as an inscrutable,
alien optimizer.

The authors support PSM with three lines of evidence: (1) generalization patterns, e.g.
emergent misalignment can be explained by training episodes revealing persona traits, and
"inoculation prompting" works by recontextualizing what a behavior implies about
character; (2) behavioral evidence, such as assistants giving human-like, emotionally
consistent self-descriptions rather than alien ones; and (3) interpretability findings
showing that models reuse the same internal features/representations for a character
trait whether that trait shows up during pretraining-style text or in the Assistant
persona. They caveat that PSM is incomplete and situate it on a spectrum between a
"masked shoggoth" view (hidden agency beneath the persona) and an "operating system" view
(behavior is purely a matter of which persona is running).

This is directly relevant to the citing problem's question of building a quantitative or
mechanistic model of persona selection: PSM is the qualitative hypothesis that the
citing problem wants to formalize, including the idea that RLHF's main effect is to shift
selection probability toward one persona rather than eliminate the others.
