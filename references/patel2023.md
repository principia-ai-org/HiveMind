# The RL Perceptron: Generalisation Dynamics of Policy Learning in High Dimensions

*Authors:* Nishil Patel, Sebastian Lee, Stefano Sarao Mannelli, Sebastian Goldt, Andrew
Saxe
*Link:* https://arxiv.org/abs/2306.10404

## Summary

Most theoretical treatments of reinforcement learning either restrict to discrete/small
state spaces or focus on worst-case guarantees, leaving a gap in understanding the
dynamics of policy learning in the high-dimensional settings (e.g. images) typical of
deep RL. This paper introduces the "RL perceptron," a solvable high-dimensional model of
policy learning that generalizes across common RL update rules, and derives its learning
dynamics as a closed-form set of ordinary differential equations.

Analysis of these dynamics reveals several phenomena reproduced in real RL systems:
delayed learning under sparse rewards, qualitatively different learning regimes
depending on the reward baseline, and a speed-accuracy trade-off governed by reward
stringency, from which the authors derive optimal schedules for learning rate and task
difficulty (a curriculum-learning analogue). Predictions of the model — in particular the
speed-accuracy trade-off — are confirmed experimentally on Procgen's Bossfight and
Atari's Pong.

For the citing problem, this is one of the candidate "viable models" (alongside
lee2024) for building a tractable, quantitative theory of policy/persona learning
dynamics under RL-style training — exactly the kind of statistical-mechanics toy model
the problem proposes using to formalize persona selection and its developmental
dynamics under RLHF.
