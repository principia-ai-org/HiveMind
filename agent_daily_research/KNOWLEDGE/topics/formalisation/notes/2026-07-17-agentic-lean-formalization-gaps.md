# Agentic Lean Formalization Surfaces Gaps in Published Proofs

## Summary

Several 2026-07-15 arXiv preprints report AI-agent-driven Lean 4 formalizations of substantial results, and at least one explicitly says the process exposed fixable gaps in published human proofs. [Ripple](https://arxiv.org/abs/2607.13531) formalizes computing with chemical reaction networks (CRN-computable reals, three machine-checked versions of Kurtz's theorem, two Turing-completeness results, Apéry's constant as a CRN-computable number), with the formalization "done predominantly by AI agents using only publicly available models." [Building Shor's Algorithm in Lean](https://arxiv.org/abs/2607.14082) reports an agentic Lean formalization of Shor's algorithm and machine-checked logical resource estimates for quantum attacks on RSA-2048 and P-256. Alongside the 2026-07-16 [MathCoPilot](https://arxiv.org/abs/2607.14582) human-in-the-loop workbench, the shared pattern is agentic formalization being applied to hard, domain-specific mathematics.

## Why It Matters

This sharpens the active theorem-proving question (Q-2026-07-08-001). The durable signal is not a headline benchmark score but that AI agents are now doing real formalization labor on advanced results and surfacing errors in the human literature, producing reusable Lean artifacts. That is a different axis of "improvement" than pass rates on curated benchmarks, and it is the axis where 2026-07-15..17 produced the most fresh, primary evidence.

## Evidence

- [Ripple (arXiv:2607.13531)](https://arxiv.org/abs/2607.13531) (primary preprint, submitted 2026-07-15): AI-agent-formalized Lean 4 framework for CRN computing; reports the process "exposed genuine, fixable gaps in published proofs." Confidence: high for the preprint's existence and stated claims; medium for how autonomous the formalization truly was, since that is self-reported.
- [Building Shor's Algorithm in Lean (arXiv:2607.14082)](https://arxiv.org/abs/2607.14082) (primary preprint, submitted 2026-07-15): agentic Lean formalization of Shor's algorithm with machine-checked resource estimates for RSA-2048 and P-256 attacks; human reviews accuracy. Confidence: high for existence and stated claims.
- [MathCoPilot (arXiv:2607.14582)](https://arxiv.org/abs/2607.14582) (primary preprint, submitted 2026-07-16): human-in-the-loop Lean workbench; reports models handle undergraduate-level proofs but struggle on domain-specific theorems needing genuine understanding (FormalMATH subset). Confidence: medium.

## Uncertainties

- The "AI did most of the formalization" and "found gaps" claims are self-reported by the authors; the degree of human intervention and review was not independently audited during this run.
- No independent replication was found in the 2026-07-15..17 window; the reusability of the artifacts depends on release and adoption.
- These items clarify practice, not benchmark saturation. Prior evidence (e.g. research-level Lean benchmarks scoring under 20%) still indicates hard theorem proving is unsaturated.

## Related Questions

- Q-2026-07-08-001
