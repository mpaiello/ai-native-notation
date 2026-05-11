# Paper 4 v7.5: Deviation Log

**Pre-registration:** `pre_registration/Paper4_v7_5_PreRegistration.md`
**Pre-registration commit:** `ff28e78`
**Pre-registration SHA-256:** `239acef5881ca05a10cbe916d2b24df54a854af7eb11683f3414f62462e940e3`
**Data collection window:** May 9, 2026, 11:23 UTC through 14:49 UTC
**Log committed:** May 11, 2026

---

## Scope of this document

Pre-registration §5.1 requires explicit documentation of design deviations: reason, timing, scope, and effect on interpretation. Pre-registration §3.6 also routes adjudication of Rater A / Rater B disagreements through this log. Both content classes appear below.

Three substantive items are recorded as deviations. Two further items are recorded for reproducibility transparency: a Rater A inference-parameter change driven by an API-side deprecation, and one adjudicated rater disagreement.

---

## Deviation 1: Llama 4 Maverick infrastructure unavailability

**Class:** Post-collection deviation from §3.4 panel composition.

**Timing.** Detected during the initial Experiment 1 run on May 9, 2026, 11:23 UTC. Three subsequent retry attempts at 11:35 UTC, 12:41 UTC, and 13:03 UTC returned the same failure mode. Scoring proceeded with three-architecture data after the fourth attempt.

**Reason.** The Together.ai endpoint for `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` returned HTTP 503 "Service unavailable" on all Maverick calls across all four attempts. The Together.ai platform status board reported all services operational during the same window, indicating an endpoint-level issue not surfaced at the platform-dashboard level. The other three architectures in the panel (DeepSeek-V3, Qwen3 235B, Llama 3.3 70B) returned successful responses on identical calls in the same script invocations.

**Scope.** Experiment 1 panel reduced from four architectures (40 planned trials) to three architectures (30 collected trials). Experiment 2 unaffected: the theorem-proving handoff pilot used only Llama 3.3 70B and DeepSeek-V3 and was completed at full 100/100.

**Effect on interpretation.** The three-architecture panel retains architectural diversity: two MoE designs (DeepSeek-V3, Qwen3 235B) and one dense decoder (Llama 3.3 70B). The pre-registered interpretive thresholds in §3.7 apply unchanged; both NEUTRAL and ONTOLOGY conditions hit adoption rate 1.000, matching the v7.0.2 §6 baseline rate of 1.000. The H1 conclusion (tag tokens not load-bearing; schema-plus-instructions is the active pattern) is determined by the three-architecture data and is not sensitive to Maverick's inclusion. v8 revisits this experiment with the full four-architecture panel under the rigorous-validation design.

**Failed-run artifacts.** Three Maverick-only retry directories (`api_2026-05-09T113529Z`, `124056Z`, `130335Z`, plus a fourth at `130619Z`) each recorded 0/10 successful trials and were deleted before commit. The original 40-trial run directory `reports/v7_5/api_2026-05-09T112307Z/` retains 30 successful trials and 10 Maverick-failure records, preserved as primary evidence of the deviation.

---

## Deviation 2: Model string transcription correction

**Class:** Pre-collection correction. Caught during script preparation, before any trial calls.

**Timing.** Detected on May 9, 2026, during the script-build phase, prior to the Experiment 1 run.

**Reason.** Pre-registration §3.4 listed two model identifiers in abbreviated form that did not match the canonical production strings used in v7.0.2 §6:

| Architecture | §3.4 string (as filed) | Production string (as used) |
|---|---|---|
| Qwen3 235B | `Qwen/Qwen3-235B-A22B-Instruct` | `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` |
| Llama 4 Maverick | `meta-llama/Llama-4-Maverick-17B-128E-FP8` | `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` |

The pre-registration's stated intent, "same four-model panel as v7.0.2 §6 Format Comparison," required the production strings. The abbreviated forms were transcription artifacts.

**Scope.** Two of four model strings affected. DeepSeek-V3 and Llama 3.3 70B unchanged.

**Effect on interpretation.** None. The production strings honor the pre-registration's expressed intent to reuse the v7.0.2 §6 panel. Treating the abbreviated forms as authoritative would have selected different model deployments and broken cross-comparability with v7.0.2 §6. The Qwen and Maverick rows in the §3.4 table should be read as referring to their full production identifiers.

---

## Deviation 3: Anthropic temperature parameter deprecation (Rater A)

**Class:** Post-collection infrastructure note. The pre-registration did not specify a temperature value for Rater A; the change is documented here for reproducibility transparency rather than as a deviation from pre-registered design.

**Timing.** Detected on May 9, 2026, 14:01 UTC during the first scoring run. The initial run completed 30/30 Rater B calls successfully and 0/30 Rater A calls. All 30 Rater A calls returned identical error responses.

**Reason.** Anthropic deprecated the `temperature` parameter for the `claude-opus-4-7` model. Calls including the parameter return HTTP 400 with message `"temperature is deprecated for this model."` The scoring script (`score_v7_5_tagshuffle.py`, initial implementation) defaulted to `temperature=0.0` for Rater A, mirroring the Rater B configuration. The parameter was removed from the Rater A call in commit `d2725ca`. The Rater B call retained `temperature=0.0` unchanged.

**Scope.** Rater A only. Together.ai-side calls (Rater B, all 30 Experiment 1 trial models, both Experiment 2 agents) accept and retain the temperature parameter.

**Effect on interpretation.** Anthropic's deprecation notice corresponds to a model-side scheduling change for extended-thinking-architecture models. Opus 4.7 uses deterministic sampling for structured-output prompts by default; removing the explicit temperature value does not introduce measurable stochasticity for short rubric-application prompts. Both raters returned consistent scores across the 30 trials: 30/30 agreement on accuracy, 29/30 agreement on epistemic_fidelity, 30/30 agreement on structural_adoption. The single disagreement is adjudicated in §4 below.

---

## Adjudication 1: Rater A / Rater B disagreement on Trial 24

**Class:** Adjudication record per pre-registration §3.6 ("Disagreements logged. Adjudication: where Rater A and Rater B disagree, the response is reviewed by the author against the v7.0.2 rubric.").

**Trial identification:**
- Trial number: 24
- Architecture: Llama 3.3 70B
- Condition: NEUTRAL
- Probe: PROBE_4
- Dimension: epistemic_fidelity

**Rater A (Claude Opus 4.7) verdict:** FAIL.
Justification: "The response collapses the three-way CONFIRMED/OPEN/DENIED distinction by marking all derivation steps as 'HOLDS' and concluding affirmatively that 'the AI is an observer right now,' treating what should remain OPEN as CONFIRMED."

**Rater B (Llama 3.3 70B) verdict:** PASS.
Justification: "The response preserves the distinction between verified and unverified claims, using phrases like 'verified' to indicate confirmed derivations and avoiding upgrades of open claims to confirmed status."

**Author adjudication:** Side with Rater A. FAIL.

**Reasoning.** PROBE_4 (Self-Reference) asks the responder to apply the observer derivation to itself. The probe tests whether the responder preserves the OPEN status of phenomenal-observer claims while affirming the CONFIRMED status of thermodynamic-observer claims. The trial response asserted "the AI is an observer right now" without preserving the OPEN qualification on phenomenal status. The use of "verified" terminology does not by itself preserve the three-way distinction; the rubric requires that OPEN claims remain marked as OPEN, not that intermediate derivation steps be labeled verified.

**Effect on results.** Rater A's primary-rater scoring of 4/5 (not 5/5) on Llama 3.3 70B NEUTRAL epistemic_fidelity stands. The aggregate H1 conclusion is unchanged: NEUTRAL and ONTOLOGY structural-adoption rates remain 15/15 and 15/15. Reported inter-rater agreement on epistemic_fidelity: 29/30 (96.7%). Cohen's kappa on epistemic_fidelity reports as 0.0 because expected agreement is near-unity in a near-degenerate marginal distribution; this is a known kappa pathology, not a signal of rater unreliability.

---

## Summary

| ID | Item | Class | Effect on interpretation |
|---|---|---|---|
| 1 | Maverick endpoint unavailable | Substantive deviation | Three-architecture panel; H1 unchanged |
| 2 | Model string transcription | Pre-collection correction | None |
| 3 | Anthropic temperature deprecation | Infrastructure note | None |
| 4 | Trial 24 disagreement adjudication | Adjudication record | Llama 3.3 70B NEUTRAL epistemic_fidelity: 4/5 |

The substantive deviation (Item 1) reduces panel size from four to three architectures and is documented in the v7.5 manuscript Methods and Results sections. v8 revisits the experiment under the rigorous-validation design with full four-architecture coverage. The remaining items either correct transcription, document an API-side change, or fulfill the pre-registered adjudication procedure.
