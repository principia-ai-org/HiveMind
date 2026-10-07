# Grokking modular arithmetic

*Authors:* Andrey Gromov
*Link:* https://arxiv.org/abs/2301.02679

## Summary

The paper presents a simple neural network that learns modular arithmetic tasks and shows grokking, a sudden jump in generalization. The setting is fully-connected two-layer networks trained with vanilla gradient descent and MSE loss, without any regularization.

The author gives evidence that grokking modular arithmetic corresponds to learning specific feature maps whose structure is determined by the task, and derives analytic expressions for the weights (and hence the feature maps) that solve a large class of modular arithmetic tasks. He also reports evidence that these feature maps are found by vanilla gradient descent as well as AdamW, which he takes to establish complete interpretability of the learned representations.

For the citing problem, it is a task-dependent example of features: explicit feature maps with Fourier structure in a network with quadratic activation, matched by structure in the trained weights.

## Cited by

- [HM-002](../problems/HM-002-what-defines-a-feature.md)
