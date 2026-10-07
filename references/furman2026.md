# Benign Loss Landscapes Can Coexist with Worst-Case Hardness

*Authors:* Zach Furman, Stephan Wäldchen, Yangda Bei, Liam Hodgkinson
*Link:* https://arxiv.org/abs/2609.13057

## Summary

Deep networks can contain worst-case targets that are evaluable in polynomial time but not learnable in polynomial time by gradient descent, yet they learn well on practical tasks. The paper studies tree tensor networks (TTNs), a model class that generalizes deep linear networks and Tucker decompositions, as a surrogate able to pose this question (deep linear networks lack hard targets; kernel methods and infinite-width limits cannot evaluate them efficiently).

The authors show that TTNs embed arbitrary read-once Boolean formulas, and so contain polynomial-size targets that gradient descent cannot learn in polynomial time. Despite this, they prove the loss landscapes are conditionally benign for every realizable target: every local minimum that is minimum-norm is global. Learning difficulty in TTNs instead can arise from high-order degenerate saddle points caused by rank-deficiency, explored through a case study of the parity function.

For the citing problem, TTNs are the model class that extends matrix products to compositions of multilinear maps, motivating a hierarchical-SVD-style analysis of learned polynomials.

## Cited by

- [HM-002](../problems/HM-002-what-defines-a-feature.md)
