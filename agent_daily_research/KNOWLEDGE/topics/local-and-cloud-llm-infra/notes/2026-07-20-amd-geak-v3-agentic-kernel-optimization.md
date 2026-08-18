# AMD GEAK V3: Repository-Level, Parallel-Agent GPU Kernel Optimization

## Summary

On 2026-07-20 AMD published GEAK V3, an open-source (Apache-2.0) agent framework that optimizes GPU kernels at repository scale across HIP, Triton, and FlyDSL on AMD CDNA and RDNA GPUs. Its architecture is the durable part: parallel sub-agents each explore a different optimization strategy in an isolated git workspace, a dual-memory system suppresses redundant exploration, MCP tools connect agents to profilers for bottleneck analysis, a RAG knowledge layer retrieves curated GPU-optimization documents, and a patch generate/evaluate/select loop promotes the best candidate and compounds improvements over multiple rounds.

## Why It Matters

This is a concrete, reproducible instance of a pattern relevant to Q-2026-07-17-001 (scaling verification-style pipelines toward near-real-time): a costly iterative "improve-then-check" loop is parallelized by running independent candidate branches in isolated workspaces and selecting the best, rather than searching serially. The same shape — parallel candidates + isolation + a selection/validation gate + caching of prior exploration — transfers to parallelizing Lean/auto-verification throughput, not just kernel tuning. It is also a primary, open-source artifact (not a vendor slide deck) that can be inspected and adapted, and it is a data point on cost-efficient inference via faster kernels on AMD hardware.

## Evidence

- [AMD ROCm blog: "GEAK V3: Agent-Driven, Repository-Level GPU Kernel Optimization across HIP, Triton, and FlyDSL on AMD GPUs"](https://rocm.blogs.amd.com/artificial-intelligence/kernel-optimization-agent/README.html) — official vendor engineering blog, dated 2026-07-20 (byline verified). Confidence: high for existence, date, and described architecture.
- [Source code: github.com/AMD-AGI/GEAK (v3.2.2)](https://github.com/AMD-AGI/GEAK) — open source, Apache-2.0. Confidence: high (primary artifact).
- Vendor-reported geomean speedups vs a "mini-swe" baseline: HIP-to-HIP 3.02×, Triton-to-Triton 2.22×, with case studies up to 14.46× on specific workloads. Confidence: medium (vendor-reported, single-vendor benchmark, no independent reproduction found).

## Uncertainties

- The speedup numbers are vendor-reported against AMD's own baseline; no independent reproduction was found during this run.
- The claimed transfer of the parallel-candidate pattern to Lean/auto-verification pipelines is an inference from architecture, not something GEAK itself demonstrates.
- FlyDSL gains were reported as marginal (~1.06× in the research pass), so benefits are uneven across backends.

## Related Questions

- Q-2026-07-17-001 (auto-verification pipelines scaling toward near-real-time — parallelism/caching pattern)
- Q-2026-07-17-004 (cost-efficient local inference — faster kernels on AMD GPUs), weakly
