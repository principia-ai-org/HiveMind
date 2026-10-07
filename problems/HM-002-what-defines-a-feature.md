# What defines a "feature"? Exploring interpretability

*HM-002 · status: open · tags: interpretability · added: 2026-10-07*

## Problem statement

What makes for a good feature in a neural network? This is a starting point for understanding what a “feature” means in different approaches to interpretability, rather than an attempt to settle on a universal definition. The aim is to identify desirable properties and compare examples until we can formulate more precise questions.

Rumelhart, Hinton, and Williams [5] emphasize that back-propagation can learn internal representations of regularities in a task, rather than requiring those features to be specified beforehand. Their work motivates asking what structure training produces, and how that structure can be recognized as a feature.

### What properties should a feature have?

**Human interpretability.** Does a feature have to correspond to a human-recognizable concept, or can it be a mathematically useful quantity without an obvious semantic interpretation? Should human interpretability be part of the definition, or a separate property that some features have?

**Dependence on data and depth.** Is a feature a property of the learned function on its entire input space, or is it defined relative to a data distribution? Can a feature be formed, or become recognizable, only once the network is sufficiently deep? How should we compare features at different depths?

**Coarse information.** Is a feature meant to give a coarse description of the learned function? The SVD of a linear map and the coefficient list of a polynomial determine their respective functions exactly. What information should a feature retain, and what should it discard?

**Coordinate invariance.** Should a feature be independent of the coordinates used to describe it? With fixed input and output inner products, the singular values and singular subspaces of a linear map are independent of the choice of orthonormal bases. Polynomial coefficients, by contrast, depend on the variables in which the polynomial is expanded. A separate question concerns the weights: should features be unchanged under reparametrizations that preserve the learned function?

Park, Choe, and Veitch [6] formalize the hypothesis that concepts in a language model correspond to directions in its representation space. They define a *causal inner product* under which concepts that can be varied independently have orthogonal representations. This gives a concrete example of why identifying a direction is only part of the question: the inner product used to compare feature directions also needs justification.

### From the DLN to the DQN

For a deep linear network (DLN), the learned function is determined by the end-to-end matrix

$$
M=W_N\cdots W_1.
$$

Its singular value decomposition gives

$$
M=\sum_i s_i\,u_i v_i^\top,
\qquad
Mx=\sum_i s_i\,u_i\,(v_i^\top x).
$$

The functions $x\mapsto v_i^\top x$ are natural candidates for input features. The vectors $u_i$ specify their output directions, and the singular values $s_i$ their strengths. The SVD identifies orthogonal directions and separates their contributions to the learned map. These can be recovered from $M$, with the usual sign ambiguity and freedom within repeated singular subspaces.

**What is the analogue for a deep quadratic network (DQN), whose learned function is a polynomial?** Consider a scalar-output DQN,

$$
\begin{aligned}
h_0(x)&=x,\\
h_\ell(x)&=\bigl(W_\ell h_{\ell-1}(x)\bigr)^{\odot 2},
\qquad \ell=1,\ldots,L,\\
f_W(x)&=a^\top h_L(x),
\end{aligned}
$$

where $v^{\odot 2}$ denotes coordinatewise squaring. Its output is a homogeneous polynomial of degree $2^L$.

The polynomial coefficients play the role of the entries of $M$. They determine the function, but identifying features requires choosing which structures in that function to single out. For example,

$$
\begin{aligned}
f_W(x,y)&=x^4-2x^2y^2+y^4\\
&=q(x,y)^2,
\qquad q(x,y)=x^2-y^2.
\end{aligned}
$$

Factoring the polynomial identifies $q$. What makes $q$ a useful feature, and how should such features be recognized from the learned polynomial or weights?

Gromov’s modular-arithmetic model [1] gives a task-dependent example. He obtains explicit feature maps with a Fourier structure in a network with quadratic activation, and finds corresponding structure in trained weights. The relation to modular arithmetic makes these features informative. Should the task help determine which structures we recognize as features?

#### An SVD for the learned polynomial

Furman et al. [3] study tree tensor networks (TTNs), which extend matrix products to compositions of multilinear maps. A corresponding extension of the matrix SVD is the **hierarchical SVD** [4]. This suggests looking for polynomial features by decomposing the tensor of coefficients and translating its singular vectors back into functions of the input.

For $f=f_W$ of degree $m=2^L$, the symmetric coefficient tensor is

$$
C_f=\frac{1}{m!}D^m f,
\qquad
f(x)=C_f(x,\ldots,x).
$$

Here $C_f$ is a function of $m$ vectors, linear in each separately and unchanged by permuting them. It contains exactly the coefficient data of $f$.

Fix an inner product on the input space and use orthonormal coordinates. Group $k$ indices of $C_f$ as rows and the remaining $m-k$ as columns. The resulting matrix has an ordinary SVD,

$$
C_f^{(k)}=\sum_j s_{k,j}\,u_{k,j}v_{k,j}^{\top}.
$$

The sum runs over the nonzero singular values. Reshape each singular vector $u_{k,j}$ as a multilinear form $P_{k,j}$ with $k$ arguments, and $v_{k,j}$ as a form $Q_{k,j}$ with $m-k$ arguments. Setting all arguments equal to $x$ gives polynomial functions

$$
\begin{aligned}
p_{k,j}(x)&=P_{k,j}(x,\ldots,x),
&\deg p_{k,j}&=k,\\
q_{k,j}(x)&=Q_{k,j}(x,\ldots,x),
&\deg q_{k,j}&=m-k.
\end{aligned}
$$

The SVD therefore gives an exact decomposition of the learned polynomial:

$$
f(x)=\sum_j s_{k,j}\,p_{k,j}(x)\,q_{k,j}(x).
$$

The singular vectors have become polynomial functions, and the singular values specify their coefficients in this decomposition. These are candidates for the analogue of the DLN’s singular vectors and values.

For the middle split, $k=m/2$, the matrix is symmetric. Its eigendecomposition gives the particularly simple form

$$
f(x)=\sum_j\lambda_j\,q_j(x)^2,
\qquad \deg q_j=m/2.
$$

The $\lambda_j$ can have either sign; their absolute values are the singular values. Thus, for a quartic, this construction identifies quadratic polynomial features.

In a hierarchical SVD, the groups of indices are split recursively along a tree [4]. The singular tensors are combined through the tree’s coefficients; evaluating every input slot at $x$ turns these contractions into sums and products of polynomial functions, ending at $f(x)$. Working with $C_f$ ensures that this decomposition concerns the learned polynomial itself.

An exact decomposition retains the same information as the polynomial coefficients, but displays it differently. Its interpretation depends on the chosen split or tree and on the inner product. **Which choices make these polynomial features informative, and what should distinguish one spectral interpretation from another?**

### The algorithms perspective

A related question arises when identifying algorithms in learned weights. Once the weights are fixed, the network’s numerical computation is fixed. There may nevertheless be several ways to interpret it as a familiar algorithm.

XOR gives a simple example: for $x,y\in\{0,1\}$, it returns $1$ exactly when $x\ne y$. One interpretation checks “$x$ but not $y$” and “$y$ but not $x$”, then combines the answers with OR. Another checks “at least one” and “not both”, then combines the answers with AND:

$$
\begin{aligned}
x\oplus y
&=(x\land\neg y)\lor(\neg x\land y)\\
&=(x\lor y)\land\neg(x\land y).
\end{aligned}
$$

Here $\land$, $\lor$, and $\neg$ denote AND, OR, and NOT.

In the preliminary XOR calculations, both interpretations can be identified in the same fixed threshold network. On the four Boolean inputs, its hidden activations and output are

$$
\begin{aligned}
h(x,y)&=(x,y,xy),\\
f(x,y)&=\mathbf 1\!\left\{h_1+h_2-2h_3>\tfrac12\right\},
\end{aligned}
$$

where $\mathbf 1\{\cdot\}$ is $1$ when the stated condition holds and $0$ otherwise. The Boolean quantities in the two interpretations can be recovered from these activations:

$$
\begin{aligned}
A&=(h_1-h_3,\;h_2-h_3),
& f&=A_1\lor A_2,\\
B&=(h_1+h_2-h_3,\;1-h_3),
& f&=B_1\land B_2.
\end{aligned}
$$

The pair $A$ records “$x$ but not $y$” and “$y$ but not $x$”; $B$ records “at least one” and “not both”. Both give the correct output on all four inputs. The weights, activations, and output rule remain unchanged. The ambiguity lies in which Boolean structure we recognize in that fixed computation.

Méloux et al. [2] investigate this ambiguity in small networks computing Boolean functions. They find that a fixed circuit can admit several interpretations, and that several candidate algorithms can satisfy their tests for correspondence with a trained network.

For features, the question is how to distinguish a useful interpretation from an arbitrary reformulation. **Should the desired properties above identify a unique set of features, or can distinct interpretations of the same fixed network be equally informative?**

## References

[1] https://arxiv.org/abs/2301.02679

[2] https://arxiv.org/abs/2502.20914

[3] https://arxiv.org/abs/2609.13057

[4] https://doi.org/10.1137/090764189

[5] https://doi.org/10.1038/323533a0

[6] https://proceedings.mlr.press/v235/park24c.html
