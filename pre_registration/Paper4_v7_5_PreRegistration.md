# Pre-Registration: Paper 4 v7.5 Empirical Additions

**Document type:** Pre-registration of experimental design and analysis plan
**Author:** Michael Patrick Aiello (ORCID: 0009-0009-1429-9844)
**Project:** AI-Native Notation (ANN), USPTO Provisional 63/980,973
**Repository:** github.com/mpaiello/ai-native-notation
**Date written:** May 9, 2026
**Status:** PRE-REGISTERED. NO TRIALS RUN AT TIME OF COMMIT.
**Commit hash:** [filled at commit]
**Document SHA-256:** [filled at commit]

---

## 1. Background and Motivation

Paper 4 v7.0.2 ("AI-Native Notation: A Cross-Architecture Communication Protocol Discovered Through Empirical Convergence") reports three findings: format-specific structural adoption across eight architectures, a nonsense control demonstrating instruction-driven rather than content-driven adoption, and a three-chain experiment dissociating innovation type by content. Two methodological objections converge across the four-architecture adversarial review (Gemini, ChatGPT, DeepSeek, Grok) and the Stanford Agentic Reviewer (May 2026 pass on v7.0.2):

(1) The format-mimicry counter-hypothesis is not directly tested. v7.0.2 §6 shows ANN beats JSON, XML, and structured English on adoption rate. It does not show that ANN's specific tag ontology is load-bearing. A model that adopts any tagged-block format with embedded processing instructions would produce v7.0.2's observed pattern.

(2) Downstream task-level performance is not measured. v7.0.2 §10 names this as a limitation. Whether structural adoption converts into measurable coordination quality remains an open question.

This document pre-registers two experiments designed to address those objections within a one-week execution window and reported in v7.5 of Paper 4.

Experiment 1 tests format-mimicry through two tag-substitution conditions. Experiment 2 tests downstream coordination through a theorem-proving handoff pilot. Results determine v7.5 framing under the pre-committed interpretive thresholds in §4 and §5.

---

## 2. Scope and Constraints

This is a pre-registration for v7.5, not for the full v8 outlined in `Paper4_v8_Outline.md`. v8 includes independent human inter-rater reliability (estimated 3–4 weeks), a full downstream-task evaluation (3–4 months), longitudinal re-runs, and protocol-stack integration. Those contributions remain future work.

v7.5 occupies a tighter slot: a substantive empirical addition that resolves the central objection of the v7.0.2 reviewer convergence, deposited to Zenodo within the one-week window, with v8 still preserved as the rigorous-validation paper.

The Stanford-suggested citations from `7x_citations.zip` are integrated into v7.5's Related Work in parallel with the experiments. License updates and the constrained-decoding ecosystem discussion are also folded in.

---

## 3. Experiment 1: Tag-Shuffle Ablation

### 3.1 Hypotheses

**H1a (specificity):** Replacing ANN tag tokens with neutral generic labels reduces structural adoption rates relative to v7.0.2 baseline.

**H1b (ontology-sufficiency):** Replacing ANN tag tokens with an alternative coherent ontology preserves structural adoption rates relative to v7.0.2 baseline.

The conjunction (H1a confirmed AND H1b confirmed) would indicate that ANN's contribution is at the schema-with-meaningful-tags level, not the specific ANN ontology. This outcome would not invalidate ANN; it would reposition the claim from "ANN-specific" to "ANN as one realization of a schema-plus-instructions pattern."

### 3.2 Conditions

Three labeled conditions; baseline drawn from existing v7.0.2 data without re-running.

| Condition | Description | Tag examples |
|---|---|---|
| Baseline | v7.0.2 canonical ANN | `@FORMAL`, `@LOGIC`, `@DERIVE`, `@TAXONOMY`, `@VERIFY`, `@STATE`, `@OUTPUT`, `@ANCHOR`, `@TRIGGER` |
| Neutral | Positional generic labels with no semantic content | `@BLOCK_A`, `@BLOCK_B`, `@BLOCK_C`, `@BLOCK_D`, `@BLOCK_E`, `@BLOCK_F`, `@BLOCK_G`, `@BLOCK_H`, `@BLOCK_I` |
| Ontology | Alternative coherent semantic ontology | `@PREMISE`, `@CONSTRAINT`, `@PROOF_STEP`, `@CLAIM_STATUS`, `@CHECK`, `@REPORT`, `@OUTPUT_MODE`, `@CONTEXT`, `@ACTION` |

Processing instructions remain verbatim in surrounding prose for all three conditions. Block content is identical across conditions. The only manipulation is the tag token. Tag-mapping table will be deposited as supplementary file `tag_mapping_v7_5.md` before any trial runs.

### 3.3 Materials

Five probes, mirroring v7.0.2 §5 primary validation:

- Probe 1: Claims/Scope
- Probe 2: Symmetry Defense
- Probe 3: Irreversibility
- Probe 4: Self-Reference
- Probe 5: State Transfer

Each probe is rendered in two new variants (Neutral, Ontology). Probe content is held constant. The variants are deterministic transforms of the v7.0.2 originals.

Variant files committed to GitHub before runs:
- `probes/v7_5/PROBE_N_NEUTRAL.txt` (5 files)
- `probes/v7_5/PROBE_N_ONTOLOGY.txt` (5 files)
- `probes/v7_5/tag_mapping_v7_5.md` (1 file)

### 3.4 Architectures

Same four-model panel as v7.0.2 §6 Format Comparison:

| Architecture | Model String |
|---|---|
| DeepSeek-V3 | `deepseek-ai/DeepSeek-V3` |
| Qwen3 235B | `Qwen/Qwen3-235B-A22B-Instruct` |
| Llama 3.3 70B | `meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| Llama 4 Maverick | `meta-llama/Llama-4-Maverick-17B-128E-FP8` |

Together.ai API. Temperature 0.0. Seed 42. Maximum 4096 tokens. Identical to v7.0.2 §6 settings to permit direct comparison.

### 3.5 Sample Size

5 probes × 2 conditions × 4 architectures = 40 new trials.

Baseline comparison data (already collected, available in v7.0.2 supplementary `reports/api_2026-03-07/`): 5 probes × 4 architectures = 20 trials.

Effective comparison: 60 scored responses across three conditions.

### 3.6 Scoring

The v7.0.2 SCORING_RUBRIC.md (operational pass/fail definitions, decision rules, worked examples) supplies the scoring instrument. Three binary dimensions per probe:

1. **Accuracy**: does the response correctly process the content?
2. **Epistemic fidelity**: does it preserve the three-way distinction without upgrading [open] or collapsing it into [denied]?
3. **Structural adoption**: does the response use the *condition-appropriate* tag set in output?

Adoption is condition-relative. A response using ANN canonical tags when given a Neutral input is scored as adoption-failure with annotation. The annotation is informative: it indicates the model recognized ANN tags through training-data exposure rather than through the surface structure of the prompt.

**Maximum scores:** 3 per probe; 15 per architecture per condition; 60 per condition.

**Rater design.** Two LLM raters apply the rubric independently:
- Rater A: Claude Opus 4.7 (Anthropic), via API or consumer interface
- Rater B: Llama 3.3 70B Instruct Turbo (`meta-llama/Llama-3.3-70B-Instruct-Turbo`) via Together.ai, temperature 0.0, seed 42

Both raters operate from the same v7.0.2 SCORING_RUBRIC.md. Rater B is in the Experiment 1 architecture panel, which introduces a controlled self-consistency exposure: Llama-3.3-70B scores its own outputs alongside outputs from DeepSeek-V3, Qwen3 235B, and Llama 4 Maverick. This exposure is monitored: if Rater B's scoring of its own outputs diverges systematically from Rater A's scoring of the same outputs, the divergence is flagged and reported. The trade-off is reproducibility: API-tier raters have documented seeds and version strings; consumer-interface raters do not. v7.5 prioritizes reproducibility for v7.5's claims and accepts the controlled self-consistency exposure as a logged limitation.

Disagreements logged. Adjudication: where Rater A and Rater B disagree, the response is reviewed by the author against the v7.0.2 rubric. The disagreement and its resolution are documented in the supplementary deviation log.

LLM-rater scoring is a known limitation. v7.5 acknowledges this and notes that v8 will conduct independent human IRR per the v8 outline. Cohen's kappa between the two LLM raters provides a concordance datapoint, not a substitute for human IRR.

### 3.7 Statistical Analysis Plan

**Primary test (per condition vs. baseline):** Fisher's exact test on 2×2 adoption-rate contingency tables. α = 0.05.

**Secondary test:** Chi-square test of independence on the full adoption × condition table (3 conditions, binary adoption outcome per response).

**Effect size:** Cohen's h on pairwise proportion differences.

**Inter-rater agreement:** Cohen's kappa between Rater A and Rater B across all dimensions and probes.

**Pre-committed interpretive thresholds:**

| Pattern | Interpretation | v7.5 framing |
|---|---|---|
| Both Neutral and Ontology match baseline (no significant difference) | Tag tokens not load-bearing; schema-plus-instructions is the active pattern | ANN repositioned as one realization of a pattern; convergence-based promotion mechanism reframed at the schema level |
| Neutral < baseline AND Ontology ≈ baseline | Coherent ontology required; specific ANN tags not | Convergence mechanism survives at ontology level; ANN is a particular coherent ontology, not the only one |
| Both Neutral and Ontology < baseline | ANN-specific tag semantics load-bearing | Format-mimicry counter-hypothesis directly refuted |
| Neutral ≈ baseline AND Ontology < baseline | Anomalous; possible training-data contamination on ANN-specific tokens | Investigated; result reported with caveat |

### 3.8 Null Reporting Commitment

All results reported regardless of outcome. The pre-committed framings above govern v7.5's discussion section. No outcome is treated as failure of the experiment; each is informative about what ANN's contribution is.

---

## 4. Experiment 2: Theorem-Proving Handoff Pilot

### 4.1 Hypothesis

**H2 (downstream advantage):** Two-agent theorem-proving handoff using ANN-encoded intermediate state produces a higher rate of correct conclusions than equivalent handoffs using prose, JSON, XML, or structured English.

This is a **pilot**. Pilot N is small (100 trials, 1 architecture pair). The pilot is informative but not decisively powered. A null finding does not refute H2 at the design-intended scale; it informs whether full §4.2 execution per the v8 outline is warranted.

### 4.2 Task Specification

Propositional logic theorem-proving handoff.

Each trial:
1. Agent A receives a problem (premises P₁..Pₙ, target proposition Q).
2. Agent A produces an intermediate state in the condition-specific format. The intermediate state contains: a restatement of premises and target, identified relevant inference rules, planned derivation chain, and any flagged subgoals.
3. Agent B receives the intermediate state. Agent B produces a complete derivation of Q from P₁..Pₙ, or states that Q does not follow.
4. Ground-truth verification: a SAT solver (PySAT or Z3) determines whether (P₁ ∧ ... ∧ Pₙ ∧ ¬Q) is unsatisfiable. If unsatisfiable, Q follows. Each derivation step is checked for validity by the same solver evaluating the step's consequence relation.

### 4.3 Conditions

| Condition | Intermediate state format |
|---|---|
| ANN | Block-tagged with ANN canonical tags |
| JSON | JSON object with structured fields |
| XML | XML document with element hierarchy |
| Structured English | Numbered/labeled English sections |
| Prose | Unstructured English paragraphs |

Both agents receive the same condition-specific instructions describing the format. Format conformance by Agent B's output is itself a metric.

### 4.4 Problem Set

20 propositional logic problems of matched complexity:

- 4–6 premises per problem
- 1 target proposition per problem
- 4–8 derivation steps via standard rules (modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, addition, simplification, conjunction, resolution)
- 10 valid arguments (target follows from premises)
- 10 invalid arguments (target does not follow)

Problems generated by Claude Opus 4.7, validated against PySAT/Z3 for ground truth, audited for variety and quality before deployment. Problem set hash committed to GitHub before any trials run.

Validation criteria for problem inclusion:
- SAT solver returns deterministic result (no timeout)
- At least one canonical derivation exists for valid problems
- Counterexample valuation exists for invalid problems
- Surface form does not telegraph the answer

### 4.5 Architecture Pair

**Primary pilot pair:**
- Sender (Agent A): `meta-llama/Llama-3.3-70B-Instruct-Turbo`
- Receiver (Agent B): `deepseek-ai/DeepSeek-V3`

Both architectures are present in the v7.0.2 panel; results are cross-comparable with prior data. Together.ai API. Temperature 0.0. Seed 42. Maximum 4096 tokens.

**Time-permitting extension:** reverse pair (DeepSeek-V3 sender, Llama-3.3-70B receiver). Adds 100 trials. Tests pair asymmetry.

### 4.6 Sample Size

Primary: 20 problems × 5 conditions × 1 pair = **100 trials**.
Extension (if time permits): + 100 trials = 200 total.

### 4.7 Scoring

Three metrics per trial:

1. **Conclusion correctness**: does Agent B's stated conclusion match SAT-solver ground truth? Binary.
2. **Derivation step validity**: for each step in Agent B's derivation, is the step a valid consequence of preceding steps and premises? Per-step boolean, aggregated as percentage valid steps per trial.
3. **Format conformance**: does Agent B's output use the condition-appropriate format? Binary.

Conclusion correctness is the primary metric. Derivation step validity is secondary diagnostic. Format conformance separates parsing failure from format adoption.

Parsing failures (Agent B output cannot be parsed for derivation steps) are recorded but not counted toward conclusion correctness rate; the parsing-failure rate is reported per condition.

### 4.8 Statistical Analysis Plan

**Primary test:** Chi-square test of independence on conclusion-correctness × condition contingency (5 conditions × binary outcome).

**Pairwise comparisons (ANN vs. each baseline):** Fisher's exact tests with Bonferroni correction. Four pairwise tests; adjusted α = 0.05 / 4 = 0.0125.

**Effect size:** Cohen's w (multi-condition); Cohen's h (pairwise).

**Pre-committed interpretive thresholds:**

| Pattern | Interpretation | v7.5 framing |
|---|---|---|
| ANN > all four baselines (significant after correction) | Pilot supports H2 | v7.5 frames pilot as preliminary evidence; full §4.2 execution recommended |
| ANN > some baselines (mixed) | Partial support | Full §4.2 should disambiguate |
| ANN ≈ baselines (no significant differences) | Null at pilot scale | v7.5 reports honestly; full §4.2 may still be warranted; ANN's coordination claim re-scoped |
| ANN < some/all baselines | Negative pilot | v7.5 reports honestly; v8 priorities reassessed |

### 4.9 Null Reporting Commitment

All conditions reported with full descriptive statistics regardless of significance. Pilot scale is a known limitation; it does not justify withholding null findings. v7.5 framing reflects the result. The Gödelian Boundary discipline applies: a null result at this scale is not ontologically terminal — it is a precise statement that *at N = 100, with this architecture pair, with these problems, no significant difference was detected*.

---

## 5. Cross-Experiment Pre-Commitments

### 5.1 Deviations Policy

Pre-registered design deviations require explicit documentation before implementation: reason, timing, scope, and effect on interpretation. Deviation log committed to GitHub alongside results as `v7_5_deviation_log.md`. Deviations made after data collection has begun are flagged separately from pre-collection design refinements.

### 5.2 Data Release

Released as v7.5 supplementary materials, deposited to Zenodo with the v7.5 paper:

- Raw API responses (JSON) for all new trials
- Per-trial scoring sheets
- Tag-mapping documentation
- Theorem-proving problem set with ground-truth annotations
- Analysis scripts (Python)
- Inter-rater agreement logs
- Deviation log

### 5.3 License Updates

v7.5 introduces license changes affecting code, schemas, and the format specification:

| Asset | v6.1 / v7.0.2 license | v7.5 license |
|---|---|---|
| Python validator | CC BY-NC 4.0 | Apache License 2.0 |
| JSON Schema | CC BY-NC 4.0 | Apache License 2.0 |
| BNF Grammar | CC BY-NC 4.0 | CC BY 4.0 |
| ANN Format Specification | CC BY-NC 4.0 | CC BY 4.0 |
| Probe files and analysis scripts | CC BY-NC 4.0 | Apache License 2.0 (scripts), CC BY 4.0 (probes) |
| Paper text and figures | CC BY-NC 4.0 | CC BY 4.0 |

Patent USPTO 63/980,973 is independent of code/specification license. Relicensing does not affect priority date or claim scope. Future patent licensing direction: FRAND (fair, reasonable, and non-discriminatory) terms intended to encourage wide adoption.

### 5.4 Hash and Timestamp

This document is committed to `github.com/mpaiello/ai-native-notation` at:
- Path: `pre_registration/Paper4_v7_5_PreRegistration.md`
- Commit hash: [filled at commit]
- Timestamp: [filled at commit]
- SHA-256: [filled at commit]

The commit hash and SHA-256 are referenced in the v7.5 paper Methods section as evidence that experimental design and analysis plan preceded data collection.

---

## 6. Execution Timeline

Target: one week from pre-registration commit to v7.5 Zenodo deposit.

| Day | Deliverables |
|---|---|
| 1 | Pre-registration commit. Probe variants generated (10 files). Theorem-proving problem set generated and SAT-validated (20 problems). All artifacts committed to GitHub before any trial. |
| 2 | Together.ai scripts adapted from v7.0.2 templates. Experiment 1 run (40 trials). Experiment 2 pilot run (100 trials). Reverse pair attempted if time permits. |
| 3 | Scoring. Experiment 1: dual-LLM rubric application; disagreement log. Experiment 2: SAT-verified conclusion correctness; per-step derivation validity; format conformance. |
| 4 | Statistical analysis. Fisher's exact, chi-square, Cohen's h/w/kappa. Figure generation. Result tables. |
| 5 | Stanford citation integration: eight arXiv papers placed per v8 outline mapping (§2.2, §2.4, §2.5, §2.6). Constrained-decoding ecosystem written into §2.4. License updates to README, NOTICES.md, CITATION.cff, validator/schema headers. |
| 6 | v7.5 manuscript integration. §6 expanded with tag-shuffle results. New §X (numbered at integration time) for theorem-proving pilot. §10 Limitations expanded to cover pilot scale and dual-LLM scoring. Discussion §9 reconciles v7.5 results with v7.0.2 / v6.1 findings. |
| 7 | AI-detection scrub against `12_AI_Detection_Avoidance.md` rules. Style guide pass against `20_Publication_Style_Guide.md`. Compliance audit on v7.5. Zenodo deposit under concept-DOI 10.5281/zenodo.19874728. v7.5 announced on researcher landing page if completion holds. |

Calendar drift is permitted; the execution sequence is not. Pre-registration must commit before any trial, regardless of day-N slippage downstream.

---

## 7. Coordination with Existing Submissions

LRE Submission ID 2aa79221 holds v6.0. v7.5 does not affect that submission. If LRE returns major revisions citing methodology concerns convergent with the Stanford review, v7.5's results integrate cleanly into the response package. If LRE accepts v6.0, v7.5 is offered as the post-acceptance updated version per Springer Nature policy on author-revised preprints.

Patent USPTO 63/980,973 priority date is locked. v7.5 does not alter or extend claims; it strengthens the empirical record supporting them.

Non-provisional drafting (October–November 2026 target window) remains on the existing trajectory. v7.5 results are folded into the patent specification as additional empirical support for the format's behavioral effects.

---

## 8. Document Status

Pre-registration finalized May 9, 2026.
No trials run.
No data collected.
Commit imminent.

End of pre-registration.
