# Robust agents learn causal world models

*Authors:* Jonathan Richens, Tom Everitt
*Link:* https://arxiv.org/abs/2402.10877

## Summary

The paper investigates a longstanding hypothesis in AI research: whether causal
reasoning is necessary for robust, general intelligence, or whether some other
inductive bias could let an agent generalize across distributional shifts just as
well without learning anything causal.

The authors prove a necessity result: any agent that satisfies a regret bound under a
sufficiently large class of distributional shifts must have learned an approximate
causal model of the environment's data-generating process. As agents are trained to be
more robust (satisfying regret bounds over larger shift classes), their learned models
provably converge toward the true causal model. This establishes an equivalence between
robustness and causal knowledge at the level of input–output behavior, showing that
causal world models are not merely one option among many for building generalizing
agents but a necessary consequence of sufficiently strong robustness guarantees.

For the citing problem, this theorem is the starting point: it guarantees that a
robust agent's learned model is approximately causal, but says nothing about *where* or
*how* that causal model is represented internally, motivating the citing problem's
question of how to make the result constructive/mechanistic and extract the causal
model in practice.
