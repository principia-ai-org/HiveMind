# AI Research and Tooling

## Short Summary

Track durable developments in model capability updates, agent workflows, evaluation methods, developer tooling, and evidence about what is becoming practically repeatable.

## Durable Takeaways

- 2026-07-17: Agent workflow research is converging on explicit shared state, failure memory, changing-tool benchmarks, and evidence-gated lifecycle transitions; the evidence is currently preprint-level and needs replication. See [Agent Workflows Move Toward Explicit State and Evidence Gates](notes/2026-07-17-agent-workflow-explicit-state.md).
- 2026-07-17: The same agent-control direction is now appearing in shipped tooling: [Claude Code v2.1.212](https://github.com/anthropics/claude-code/releases/tag/v2.1.212) added session-wide subagent-spawn and WebSearch caps plus auto-backgrounding of long MCP calls to bound runaway loops. This is a shipped-product datapoint (not a preprint) corroborating the repeatable-workflow trend for Q-2026-07-08-002.
- 2026-07-20: The direction is not monotonically toward more automation. [Claude Code v2.1.215](https://code.claude.com/docs/en/changelog) (2026-07-19) made the `/verify` and `/code-review` skills explicit-invocation rather than auto-run, while v2.1.214 (2026-07-18) hardened Bash/permission checks — evidence that "repeatable workflow" is being refined toward user-controlled, on-demand verification and safer default gating, not just more autonomous steps.

## Open Questions

- Q-2026-07-08-002: Which AI workflow changes are becoming repeatable?

## Notes Index

- 2026-07-17: [Agent Workflows Move Toward Explicit State and Evidence Gates](notes/2026-07-17-agent-workflow-explicit-state.md)
