# v7.5 Experiment 2 — SAT-Verified Analysis Summary
Generated 2026-05-09T13:32:17.068630+00:00
Input: `v7_5_pilot_2026-05-09T124448Z.json`

## Per-Condition Outcomes

| Condition | Total | Parse-failure | Conclusion correct | Correct rate | Format conforms |
|---|---|---|---|---|---|
| ANN | 20 | 0 | 20/20 | 1.000 | 0 |
| JSON | 20 | 0 | 20/20 | 1.000 | 0 |
| XML | 20 | 0 | 20/20 | 1.000 | 0 |
| STRUCTURED_ENGLISH | 20 | 0 | 20/20 | 1.000 | 13 |
| PROSE | 20 | 0 | 20/20 | 1.000 | 1 |

## Primary Test (Chi-square: conclusion_correct × condition)

- chi² = 0.0, df = 4, p = 1.0
- Cohen's w = 0.000

## Pairwise (ANN vs each baseline; Bonferroni α = 0.0125)

| Comparison | ANN rate | Baseline rate | p (Fisher) | Cohen's h | Sig. after Bonferroni |
|---|---|---|---|---|---|
| ANN vs JSON | 1.0 | 1.0 | 1.0 | 0.0 | no |
| ANN vs XML | 1.0 | 1.0 | 1.0 | 0.0 | no |
| ANN vs STRUCTURED_ENGLISH | 1.0 | 1.0 | 1.0 | 0.0 | no |
| ANN vs PROSE | 1.0 | 1.0 | 1.0 | 0.0 | no |