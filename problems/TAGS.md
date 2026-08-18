# Tags

The controlled vocabulary for problem tags. A problem may only use tags from this list —
CI (`scripts/check_problems.py`) fails on any tag that isn't here. This keeps the tag
space from sprawling into synonyms.

**To add a tag:** add a bullet below (lowercase, hyphenated, no spaces) in the same pull
request that first uses it. Adding a tag is a deliberate choice — prefer an existing tag
before introducing a new one.

The pipeline reads this list to auto-assign tags when a problem is submitted with the
`<auto>` placeholder.

## Allowed tags

- interpretability
- generalization
- robustness
- alignment
- evaluation
- reasoning
- agents
- reinforcement-learning
- theory
- oversight
- cooperative-ai
