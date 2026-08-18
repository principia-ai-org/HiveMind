# Agent persona selection

*HM-002 · status: open · tags: interpretability, alignment, reinforcement-learning · added: 2026-08-18*

<!-- The ID, date, and tags in the line above are placeholders filled in automatically
     when your PR is processed: the ID becomes the next free number (and the file is
     renamed to match), the date becomes today, and the tags are drawn from
     problems/TAGS.md based on your problem statement. To set the date or tags yourself,
     replace their placeholder with real values (tags must come from problems/TAGS.md);
     the ID is always assigned automatically. See problems/README.md for how to name the
     file. -->

## Problem statement

Our current intuition of RLHF and persona is that among multiple `personas` or `latents` learned in the pre-trained model from diverse training corpus, RLHF increases the probability density of the `helpful agent` persona, but there still exists non-zero probability of other personas [[marks2026]](../references/marks2026.md). On the other hand, many empirical papers showed that certain role play-like prompts can trigger another persona. We can roughly view this as conditional amplification of certain `persona`, given the in-context information [[xie2021]](../references/xie2021.md), [[chen2025]](../references/chen2025.md), [[anil2024]](../references/anil2024.md).

However, it is unclear how to make a quantitative or clearer mechanistic model of such `persona selection`, especially entangled with training method - including RLHF and the latents from pretraining. Can we build a toy model of persona development/selection? The ideal model should be able to predict 1) quantitative prediction on the probability of each persona and 2) the developmental dynamics of such persona -- when they are developed, what is actually changed during the fine-tuning period (including RLHF). We think some viable models are RL perceptron and its variants [[patel2023]](../references/patel2023.md), [[lee2024]](../references/lee2024.md).

## Potential resources

<Datasets, tools, codebases, benchmarks, related open problems, or people/leads that
could help. Bullet points are fine.>

## References

- [[marks2026]](../references/marks2026.md) — Sam Marks, Jack Lindsey, Christopher Olah, *The Persona Selection Model: Why AI Assistants might Behave like Humans*, Anthropic Alignment Science Blog 2026. https://alignment.anthropic.com/2026/psm/
- [[xie2021]](../references/xie2021.md) — Sang Michael Xie, Aditi Raghunathan, Percy Liang, Tengyu Ma, *An Explanation of In-context Learning as Implicit Bayesian Inference*, ICLR 2022. https://arxiv.org/abs/2111.02080
- [[chen2025]](../references/chen2025.md) — Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, Jack Lindsey, *Persona Vectors: Monitoring and Controlling Character Traits in Language Models*, arXiv preprint 2025. https://arxiv.org/abs/2507.21509
- [[anil2024]](../references/anil2024.md) — Cem Anil et al., *Many-shot Jailbreaking*, Anthropic 2024. https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf
- [[patel2023]](../references/patel2023.md) — Nishil Patel, Sebastian Lee, Stefano Sarao Mannelli, Sebastian Goldt, Andrew Saxe, *The RL Perceptron: Generalisation Dynamics of Policy Learning in High Dimensions*, Phys. Rev. X 2025. https://arxiv.org/abs/2306.10404
- [[lee2024]](../references/lee2024.md) — Jin Hwa Lee, Stefano Sarao Mannelli, Andrew Saxe, *Why Do Animals Need Shaping? A Theory of Task Composition and Curriculum Learning*, ICML 2024. https://arxiv.org/abs/2402.18361
