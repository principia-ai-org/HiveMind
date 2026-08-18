# Local and Cloud LLM Infra

## Short Summary

Track infrastructure for running LLMs locally and in the cloud, with preference for cost-efficient inference and fine-tuning and for understanding security, software compatibility, and speed (quantization, memory footprint, serving throughput). Source-backed engineering blogs, official docs/release notes, and reproducible benchmarks are preferred over unsourced performance claims.

## Durable Takeaways

- 2026-07-20: AMD's open-source (Apache-2.0) GEAK V3 parallelizes an iterative kernel improve-and-check loop by running independent candidate strategies in isolated git workspaces with a patch generate/evaluate/select step. The durable, transferable pattern (parallel candidates + isolation + selection gate + cached exploration) bears on scaling verification-style pipelines, not just kernel tuning; speedups are vendor-reported. See [AMD GEAK V3](notes/2026-07-20-amd-geak-v3-agentic-kernel-optimization.md).

## Open Questions

- Q-2026-07-17-001: How can auto-verification pipelines (especially Lean) scale toward near-real-time verification? (shared with formalisation; infra/parallelism angle)
- Q-2026-07-17-004: How to best budget Claude and Codex API spend alongside Google Cloud GPU costs for local LLM inference?

## Notes Index

- 2026-07-20: [AMD GEAK V3: Repository-Level, Parallel-Agent GPU Kernel Optimization](notes/2026-07-20-amd-geak-v3-agentic-kernel-optimization.md)
