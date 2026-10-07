# Everything, Everywhere, All at Once: Is Mechanistic Interpretability Identifiable?

*Authors:* Maxime Méloux, Silviu Maniu, François Portet, Maxime Peyrard
*Link:* https://arxiv.org/abs/2502.20914

## Summary

The paper asks whether, for a given behavior and under mechanistic interpretability's own criteria, a unique explanation exists. Drawing on identifiability in statistics, it considers two MI strategies: "where-then-what", which isolates a circuit replicating model behavior and then interprets it, and "what-then-where", which starts from candidate algorithms and searches for activation subspaces implementing them using causal alignment.

The authors test both strategies on Boolean functions and small multi-layer perceptrons, fully enumerating candidate explanations. They find systematic non-identifiability: multiple circuits can replicate the behavior, a circuit can have multiple interpretations, several algorithms can align with the network, and one algorithm can align with different subspaces.

They discuss whether uniqueness is necessary: a pragmatic approach may require only predictive and manipulability standards, whereas if uniqueness is essential for understanding, stricter criteria may be needed. They also point to the inner interpretability framework, which validates explanations through multiple criteria. For the citing problem, it supplies the evidence that a fixed network can admit several equally valid algorithmic interpretations.

## Cited by

- [HM-002](../problems/HM-002-what-defines-a-feature.md)
