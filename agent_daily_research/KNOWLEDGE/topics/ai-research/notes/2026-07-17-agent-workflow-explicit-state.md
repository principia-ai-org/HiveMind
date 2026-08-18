# Agent Workflows Move Toward Explicit State and Evidence Gates

## Summary

Several 2026-07-16 arXiv preprints surfaced in the 2026-07-17 run converge on a practical agent-workflow pattern: [SearchOS-V1](https://arxiv.org/abs/2607.15257) keeps search state external and inspectable, [MCPEvol-Bench](https://arxiv.org/abs/2607.14642) tests agents against changing tool interfaces, and [Proof-or-Stop](https://arxiv.org/abs/2607.14890) requires evidence before lifecycle transitions such as "done" or "ready to merge."

## Why It Matters

This directly advances the active question about repeatable AI workflow changes. The common pattern is not a single tool feature; it is a control architecture for making agent work less dependent on hidden context and self-reported progress.

## Evidence

- [SearchOS-V1](https://arxiv.org/abs/2607.15257) (primary preprint, submitted 2026-07-16) proposes evidence graphs, coverage maps, failure memory, and middleware for open-domain search agents, and reports leading metrics on WideSearch and GISA. Confidence: medium.
- [MCPEvol-Bench](https://arxiv.org/abs/2607.14642) (primary preprint, submitted 2026-07-16) evaluates LLM agents across simulated MCP server tool evolution in 123 servers and reports performance declines for frontier models under evolved tools. Confidence: medium.
- [Proof-or-Stop](https://arxiv.org/abs/2607.14890) (primary preprint, submitted 2026-07-16) proposes evidence-gated lifecycle control for autonomous coding agents and reports zero false-DONE in its 10-scenario mechanism test. Confidence: medium.

## Uncertainties

- These are preprints, and no independent replications were found during this run.
- Reported improvements may depend on task selection, model family, implementation details, or benchmark construction.
- The durable takeaway is the recurring workflow pattern, not the exact quantitative gains.

## Related Questions

- Q-2026-07-08-002
