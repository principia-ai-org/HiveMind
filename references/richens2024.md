# Robust agents learn causal world models

*Authors:* Jonathan Richens, Tom Everitt
*Link:* https://arxiv.org/abs/2402.10877

## Summary

The paper addresses a foundational question: is learning a *causal* model necessary for
an agent to generalize across domains, or do weaker inductive biases suffice? The authors
answer it theoretically. They prove that any agent able to satisfy a regret bound under a
sufficiently large set of distributional shifts must have learned an approximate causal
model of the data-generating process; for optimal agents, that learned model converges to
the true causal structure. The result runs in both directions — robustness under
intervention-style shifts and knowledge of causal structure are shown to be essentially
equivalent.

This establishes a formal link between robustness and causality: causal reasoning is not
merely helpful but necessary for the kind of transfer that survives distribution shift.
For AI safety the relevance is direct — it suggests that agents which generalize reliably
to novel environments must be representing causal structure internally, which bears on
interpretability (what such agents encode), on predicting out-of-distribution behavior,
and on the prospects for extracting a world model from a capable agent. Published at ICLR
2024 (oral).
