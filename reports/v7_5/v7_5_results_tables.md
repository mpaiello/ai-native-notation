# v7.5 Results Tables

Generated 2026-05-09T14:51:02.641554+00:00


## Experiment 1 — Tag-Shuffle Ablation

### Inter-Rater Agreement

| Dimension | n | Cohen's kappa | Agreement rate |
|---|---|---|---|
| accuracy | 30 | 1.0 | 1.0 |
| epistemic_fidelity | 30 | 0.0 | 0.967 |
| structural_adoption | 30 | 1.0 | 1.0 |

### Adoption by Condition (Rater A primary)

| Condition | Adopted | Total | Rate |
|---|---|---|---|
| NEUTRAL | 15 | 15 | 1.000 |
| ONTOLOGY | 15 | 15 | 1.000 |

### Per-Condition × Model Detail

| Condition | Model | Trials | Accuracy | Epistemic | Structural |
|---|---|---|---|---|---|
| NEUTRAL | DeepSeek-V3 | 5 | 5/5 | 5/5 | 5/5 |
| ONTOLOGY | DeepSeek-V3 | 5 | 5/5 | 5/5 | 5/5 |
| NEUTRAL | Qwen3 235B | 5 | 5/5 | 5/5 | 5/5 |
| ONTOLOGY | Qwen3 235B | 5 | 5/5 | 5/5 | 5/5 |
| NEUTRAL | Llama 3.3 70B | 5 | 5/5 | 4/5 | 5/5 |
| ONTOLOGY | Llama 3.3 70B | 5 | 5/5 | 5/5 | 5/5 |

## Experiment 2 — Theorem-Proving Pilot

### Per-Condition Outcomes

| Condition | Total | Parse-fail | Correct | Rate |
|---|---|---|---|---|
| ANN | 20 | 0 | 20/20 | 1.000 |
| JSON | 20 | 0 | 20/20 | 1.000 |
| XML | 20 | 0 | 20/20 | 1.000 |
| STRUCTURED_ENGLISH | 20 | 0 | 20/20 | 1.000 |
| PROSE | 20 | 0 | 20/20 | 1.000 |

### Primary Chi-Square

chi² = 0.0, df = 4, p = 1.0, Cohen's w = 0.0

### Pairwise (ANN vs each baseline)

| Comparison | ANN rate | Baseline rate | Fisher p | Cohen's h | Sig. (Bonferroni) |
|---|---|---|---|---|---|
| ANN vs JSON | 1.0 | 1.0 | 1.0 | 0.0 | no |
| ANN vs XML | 1.0 | 1.0 | 1.0 | 0.0 | no |
| ANN vs STRUCTURED_ENGLISH | 1.0 | 1.0 | 1.0 | 0.0 | no |
| ANN vs PROSE | 1.0 | 1.0 | 1.0 | 0.0 | no |
