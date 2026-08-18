# Agent persona selection

*HM-NEXT · status: open · tags: <auto> · added: YYYY-MM-DD*

<!-- The ID, date, and tags in the line above are placeholders filled in automatically
     when your PR is processed: the ID becomes the next free number (and the file is
     renamed to match), the date becomes today, and the tags are drawn from
     problems/TAGS.md based on your problem statement. To set the date or tags yourself,
     replace their placeholder with real values (tags must come from problems/TAGS.md);
     the ID is always assigned automatically. See problems/README.md for how to name the
     file. -->

## Problem statement

Our current intuition of RLHF and persona is that among multiple `personas` or `latents` learned in the pre-trained model from diverse training corpus, RLHF increases the probability density of the `helpful agent` persona, but there still exists non-zero probability of other personas [1]. On the other hand, many empirical papers showed that certain role play-like prompts can trigger another persona. We can roughly view this as conditional amplification of certain `persona`, given the in-context information [2, 3, 4].

However, it is unclear how to make a quantitative or clearer mechanistic model of such `persona selection`, especially entangled with training method - including RLHF and the latents from pretraining. Can we build a toy model of persona development/selection? The ideal model should be able to predict 1) quantitative prediction on the probability of each persona and 2) the developmental dynamics of such persona -- when they are developed, what is actually changed during the fine-tuning period (including RLHF). We think some viable models are RL perceptron and its variants [5, 6].

## Potential resources

<Datasets, tools, codebases, benchmarks, related open problems, or people/leads that
could help. Bullet points are fine.>

## References

[1] https://alignment.anthropic.com/2026/psm/
[2] https://openreview.net/challenge?redirect=%2Fforum%3Fid%3DRdJVFCHjUMI
[3] https://arxiv.org/abs/2507.21509
[4] https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf
[5] https://arxiv.org/abs/2306.10404
[6] https://arxiv.org/abs/2402.18361
