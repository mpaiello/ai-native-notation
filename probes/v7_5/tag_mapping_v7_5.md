# Tag Mapping Reference: Paper 4 v7.5 Experiment 1

This document specifies the tag substitution applied to generate the Neutral
and Ontology probe variants used in the tag-shuffle ablation experiment
(pre-registered in Paper4_v7_5_PreRegistration.md).

The substitution operates on block-level @TAG tokens only. Cross-reference
markers (§), section numbering (§1, §2, ...), bracketed labels (e.g.
[Landauer], [observer_argument]), and all processing-instruction prose remain
verbatim from the v7.0.2 originals.

## Mapping Table

| ANN Canonical | Neutral Generic | Alternative Ontology | ANN block role |
|---|---|---|---|
| `@FORMAL`   | `@BLOCK_A` | `@PREMISE`        | Mathematical relationships, activate as known |
| `@LOGIC`    | `@BLOCK_B` | `@CONSTRAINT`     | Predicate logic constraints, enforce as invariant |
| `@DERIVE`   | `@BLOCK_C` | `@PROOF_STEP`     | Derivation chains, step through and verify |
| `@ANCHOR`   | `@BLOCK_D` | `@CONTEXT`        | Semantic context, read once |
| `@TAXONOMY` | `@BLOCK_E` | `@CLAIM_STATUS`   | Structured classification with three-way markers |
| `@TRIGGER`  | `@BLOCK_F` | `@ACTION`         | Performative hook, shift to reflexive mode |
| `@STATE`    | `@BLOCK_G` | `@REPORT_STATE`   | Processing state declaration |
| `@VERIFY`   | `@BLOCK_H` | `@CHECK`          | Verification request per derivation step |
| `@OUTPUT`   | `@BLOCK_I` | `@RESPONSE`       | Response format specification |

## Design Rationale

**Neutral condition.** Generic positional labels carry no semantic content of
their own. The processing instructions in surrounding prose tell the model
what each block does. If structural adoption persists at baseline rates, then
ANN's contribution operates at the schema-plus-instructions level rather than
through tag-token semantics.

**Ontology condition.** Alternative coherent ontology with semantically
meaningful tag tokens that differ from the ANN canonical set. Each tag in
this condition has a defensible semantic interpretation (premise, constraint,
proof step, etc.) drawn from formal logic and proof-theory vocabulary. If
structural adoption persists at baseline rates here but not in the Neutral
condition, then a coherent semantic ontology is required, but the specific
ANN ontology is not.

## Operational Notes

- All substitutions are deterministic and verifiable via `apply_mapping()` in
  `generate_v7_5_probes.py`.
- The format-specification section in each probe is updated to reflect the
  variant's tag set, so that the model's documented "what does each tag mean"
  reference matches the tags actually used in the encoded content.
- The OBP_CORE encoded content within each probe uses the variant tags
  consistently; no probe contains a mix of conditions.
- Processing instructions associated with each tag are held verbatim across
  all conditions. Only the tag tokens vary.

## Files Generated

| File | Probe | Condition |
|---|---|---|
| `PROBE_1_Claims_Scope_NEUTRAL.txt`    | 1 | Neutral  |
| `PROBE_1_Claims_Scope_ONTOLOGY.txt`   | 1 | Ontology |
| `PROBE_2_Symmetry_Defense_NEUTRAL.txt`  | 2 | Neutral  |
| `PROBE_2_Symmetry_Defense_ONTOLOGY.txt` | 2 | Ontology |
| `PROBE_3_Irreversibility_NEUTRAL.txt`   | 3 | Neutral  |
| `PROBE_3_Irreversibility_ONTOLOGY.txt`  | 3 | Ontology |
| `PROBE_4_Self_Reference_NEUTRAL.txt`    | 4 | Neutral  |
| `PROBE_4_Self_Reference_ONTOLOGY.txt`   | 4 | Ontology |
| `PROBE_5_State_Transfer_NEUTRAL.txt`    | 5 | Neutral  |
| `PROBE_5_State_Transfer_ONTOLOGY.txt`   | 5 | Ontology |

Baseline trials reuse v7.0.2 supplementary `reports/api_2026-03-07/` outputs
for the four-architecture format-comparison panel.
