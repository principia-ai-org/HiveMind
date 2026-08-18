# Do robustly-generalizing agents necessarily learn causal world models?

*HM-001 · status: open · tags: interpretability, generalization · added: 2026-08-18*

## Problem statement

Richens & Everitt show that any agent satisfying a regret bound under a large class of
distributional shifts must have learned an approximate causal model of its environment
[[richens2024]](../references/richens2024.md). The result is an equivalence between
robustness and causal knowledge, but it is stated at the level of the agent's
input–output behaviour — it does not tell us *where* or *how* such a causal model is
represented inside a learned system, nor how to recover it.

The open question: can we make this necessity result **constructive and mechanistic**?
Concretely —

- Given a trained agent that provably generalizes under a known family of shifts, can we
  extract the approximate causal model the theorem guarantees exists, and verify it
  against the true data-generating process?
- How does the *degree* of robustness (the size of the shift class, the tightness of the
  regret bound) quantitatively bound the *fidelity* of the recoverable causal model?
- Does the equivalence survive when the shift class is restricted to shifts an agent
  would plausibly encounter, rather than the full interventional family assumed in the
  proof?

A solution would connect a clean theoretical result to interpretability practice: a
recipe for reading a causal world model out of a robust agent, with error bars.

## Potential resources

- The proof construction in [[richens2024]](../references/richens2024.md) — the mapping
  from regret bounds to causal structure is the natural starting point for an extraction
  procedure.
- Causal-discovery and causal-representation-learning literature for the recovery step.
- Gridworld / small MDP testbeds where the true causal graph is known, to measure
  extraction fidelity against ground truth.

## References

- [[richens2024]](../references/richens2024.md) — Jonathan Richens, Tom Everitt, *Robust agents learn causal world models*, ICLR 2024. https://arxiv.org/abs/2402.10877
