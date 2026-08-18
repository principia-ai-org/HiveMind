# The RL Perceptron: Generalisation Dynamics of Policy Learning in High Dimensions

*Authors:* Nishil Patel, Sebastian Lee, Stefano Sarao Mannelli, Sebastian Goldt, Andrew Saxe
*Link:* https://arxiv.org/abs/2306.10404

## Summary

Modern reinforcement learning uses neural networks to learn policies from
high-dimensional inputs, but theoretical understanding of policy-learning dynamics in
this regime is limited: most existing RL theory covers discrete state spaces or
worst-case analysis, not the typical-case, high-dimensional setting these systems
actually operate in.

The authors introduce the "RL Perceptron," a tractable theoretical model of
policy-gradient learning that is expressive enough to capture a variety of learning
protocols and reward structures. Using tools from statistical physics, they derive
closed-form ordinary differential equations that describe the typical learning
dynamics in high dimensions, which in turn let them derive optimal learning-rate
schedules and task-difficulty curricula analytically.

The model reproduces several phenomena seen in practice: delayed learning onset under
sparse rewards (with the delay depending on reward structure), qualitatively different
learning regimes depending on the reward baseline, and speed–accuracy trade-offs
governed by reward stringency. These predictions are validated empirically on Procgen's
"Bossfight" and Atari's "Pong." For the citing problem, the RL Perceptron is cited as a
candidate toy-model framework — tractable, statistical-physics-style dynamics for
policy learning — that could be adapted to model the developmental dynamics of persona
selection during RLHF.
