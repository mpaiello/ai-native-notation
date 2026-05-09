# v7.5 Run, Score, and Analyze Scripts

These scripts implement the experiments pre-registered in
`pre_registration/Paper4_v7_5_PreRegistration.md`. Run them in order.

## Prerequisites

```powershell
pip install together anthropic sympy scipy
```

`scipy` is optional but recommended (chi-square p-values use it; without scipy
the chi² statistic is still computed but the p-value is reported as `null`).

## Environment Variables

```powershell
$env:TOGETHER_API_KEY = "<your-together-key>"
$env:ANTHROPIC_API_KEY = "<your-anthropic-key>"
```

Together is required for both run scripts and Rater B in the scorer.
Anthropic is required for Rater A in the scorer (Claude Opus 4.7).

If you don't have an Anthropic API key, get one at
https://console.anthropic.com/. Free credits cover the scoring volume.

## Run Order

### Step 1: Tag-shuffle ablation (Experiment 1)

```powershell
cd scripts/v7_5
python run_v7_5_tagshuffle.py
```

40 trials. ~5–15 minutes depending on Together.ai latency. Outputs land in
`reports/v7_5/api_<UTC-timestamp>/`:
- `v7_5_tagshuffle_<timestamp>.json` — consolidated raw responses
- `v7_5_tagshuffle_<model>_<condition>_<timestamp>.md` — per-cell markdown

Optional flags:
- `--dry-run` plans without API calls
- `--models <subset>` runs only some models
- `--conditions NEUTRAL` runs only one condition

### Step 2: Theorem-proving pilot (Experiment 2)

```powershell
python run_v7_5_pilot.py
```

100 trials. ~15–30 minutes. Output in `reports/v7_5/pilot_<timestamp>/`:
- `v7_5_pilot_<timestamp>.json` — every trial with both stages

Optional flags:
- `--reverse-pair` adds 100 more trials with swapped sender/receiver
- `--problems V01 I01 V05` runs a subset for debugging

### Step 3: Score Experiment 1

```powershell
python score_v7_5_tagshuffle.py --input ../../reports/v7_5/api_<timestamp>/v7_5_tagshuffle_<timestamp>.json
```

Dual-LLM scoring. Outputs:
- `v7_5_tagshuffle_scored_<scoring-timestamp>.json` — per-trial scores from both raters, kappa
- `v7_5_tagshuffle_scoring_summary_<scoring-timestamp>.md` — kappa table

Disagreements are logged in the JSON for manual adjudication per the
pre-registration.

### Step 4: Verify Experiment 2

```powershell
python verify_v7_5_pilot.py --input ../../reports/v7_5/pilot_<timestamp>/v7_5_pilot_<timestamp>.json
```

SAT-backed verification. Outputs:
- `v7_5_pilot_verified_<verify-timestamp>.json` — per-trial conclusion
  correctness, derivation step parsing, format conformance, full pre-registered
  statistics
- `v7_5_pilot_analysis_summary_<verify-timestamp>.md` — chi-square + pairwise
  Fisher's exact + Cohen's w/h

### Step 5: Consolidate

```powershell
python v7_5_analyze.py --exp1 <scored.json> --exp2 <verified.json>
```

Generates manuscript-ready tables and applies the pre-committed interpretive
threshold logic from §3.7 and §4.8 of the pre-registration.

Outputs:
- `v7_5_results_tables.md`
- `v7_5_interpretive_threshold_check.md`

## Notes on Reproducibility

All API calls use temperature 0.0 and seed 42 (where the API supports seeds).
Model strings documented in each script match the v7.0.2 §6 production strings.

The Rater A model string is set to `claude-opus-4-7` in `score_v7_5_tagshuffle.py`.
If Anthropic's actual API model identifier for Opus 4.7 differs (e.g.,
`claude-opus-4-7-20260xxx`), update the `RATER_A_MODEL` constant at the top
of that script to the exact string shown in
https://docs.claude.com/en/docs/about-claude/models.

## Files

| File | Purpose |
|---|---|
| `run_v7_5_tagshuffle.py` | Experiment 1 trial runner (Together.ai) |
| `run_v7_5_pilot.py` | Experiment 2 two-stage handoff runner (Together.ai) |
| `score_v7_5_tagshuffle.py` | Dual-LLM scorer (Anthropic Opus 4.7 + Together Llama 3.3 70B) |
| `verify_v7_5_pilot.py` | SAT-backed verifier + pre-registered statistics |
| `v7_5_analyze.py` | Consolidated analysis + threshold check |
