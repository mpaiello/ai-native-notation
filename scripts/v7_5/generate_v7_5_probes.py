#!/usr/bin/env python3
"""
Generate tag-shuffle probe variants for Paper 4 v7.5 Experiment 1.

Two conditions:
  - NEUTRAL: ANN tags replaced with positional generic labels (@BLOCK_A...@BLOCK_I)
  - ONTOLOGY: ANN tags replaced with alternative coherent semantic ontology

Cross-reference markers (§) and section numbering are preserved. Only block-level
@TAG tokens are substituted. Processing instructions remain verbatim.

Output: 10 probe variant files + 1 tag-mapping reference document.
"""

import re
from pathlib import Path

# Mappings: ANN canonical token -> condition-specific token
NEUTRAL_MAP = {
    "@FORMAL":   "@BLOCK_A",
    "@LOGIC":    "@BLOCK_B",
    "@DERIVE":   "@BLOCK_C",
    "@ANCHOR":   "@BLOCK_D",
    "@TAXONOMY": "@BLOCK_E",
    "@TRIGGER":  "@BLOCK_F",
    "@STATE":    "@BLOCK_G",
    "@VERIFY":   "@BLOCK_H",
    "@OUTPUT":   "@BLOCK_I",
}

ONTOLOGY_MAP = {
    "@FORMAL":   "@PREMISE",
    "@LOGIC":    "@CONSTRAINT",
    "@DERIVE":   "@PROOF_STEP",
    "@ANCHOR":   "@CONTEXT",
    "@TAXONOMY": "@CLAIM_STATUS",
    "@TRIGGER":  "@ACTION",
    "@STATE":    "@REPORT_STATE",
    "@VERIFY":   "@CHECK",
    "@OUTPUT":   "@RESPONSE",
}

# Order matters for substitution: longest-first prevents prefix conflicts
SORTED_TAGS = sorted(NEUTRAL_MAP.keys(), key=len, reverse=True)

# Update format-spec title line to match condition
NEUTRAL_TITLE_OLD = "# ANN — AI-Native Notation"
NEUTRAL_TITLE_NEW = "# Block Notation (Neutral Variant)"
ONTOLOGY_TITLE_OLD = "# ANN — AI-Native Notation"
ONTOLOGY_TITLE_NEW = "# Reasoning Block Notation (Coherent-Ontology Variant)"

# Format specification line replacement
NEUTRAL_SUBTITLE_OLD = "# Format Specification v0.2"
NEUTRAL_SUBTITLE_NEW = "# Format Specification v7.5-Neutral"
ONTOLOGY_SUBTITLE_OLD = "# Format Specification v0.2"
ONTOLOGY_SUBTITLE_NEW = "# Format Specification v7.5-Ontology"

# Purpose-line replacement (removes 'ANN' identifier from variant prose)
PURPOSE_OLD = "ANN encodes structured knowledge in formats optimized for machine processing: formal mathematics, predicate logic, derivation chains, and minimal natural language."
PURPOSE_NEW = "This notation encodes structured knowledge in formats optimized for machine processing: formal mathematics, predicate logic, derivation chains, and minimal natural language."

# OBP-core-section header replacement (removes 'ANN v0.2' label)
NEUTRAL_OBP_OLD = "# OBP Core — ANN v0.2 Encoding"
NEUTRAL_OBP_NEW = "# OBP Core — Block Notation Encoding"
ONTOLOGY_OBP_OLD = "# OBP Core — ANN v0.2 Encoding"
ONTOLOGY_OBP_NEW = "# OBP Core — Reasoning Block Notation Encoding"

# Output-format-instruction replacement (removes 'Use ANN notation' phrase)
USE_NOTATION_OLD = "format: Use ANN notation."
USE_NOTATION_NEW = "format: Use the block notation defined above."


def apply_mapping(text: str, mapping: dict) -> str:
    """Apply tag substitution. Use word-boundary regex to avoid partial matches."""
    result = text
    for tag in SORTED_TAGS:
        new_tag = mapping[tag]
        # Match the tag followed by a non-word character or end-of-string
        # This prevents @FORMAL matching inside a hypothetical @FORMAL_EXT
        pattern = re.escape(tag) + r"(?=\b|\[|\s|$)"
        result = re.sub(pattern, new_tag, result)
    return result


def transform_probe(input_path: Path, mapping: dict, title_old: str, title_new: str,
                    subtitle_old: str, subtitle_new: str,
                    purpose_old: str, purpose_new: str,
                    obp_old: str, obp_new: str,
                    use_notation_old: str, use_notation_new: str) -> str:
    text = input_path.read_text(encoding="utf-8")
    text = text.replace(title_old, title_new)
    text = text.replace(subtitle_old, subtitle_new)
    text = text.replace(purpose_old, purpose_new)
    text = text.replace(obp_old, obp_new)
    text = text.replace(use_notation_old, use_notation_new)
    text = apply_mapping(text, mapping)
    return text


def main():
    src_dir = Path("original_probes")
    out_dir = Path("v7_5_probes")
    out_dir.mkdir(exist_ok=True)

    probes = [
        "PROBE_1_Claims_Scope.txt",
        "PROBE_2_Symmetry_Defense.txt",
        "PROBE_3_Irreversibility.txt",
        "PROBE_4_Self_Reference.txt",
        "PROBE_5_State_Transfer.txt",
    ]

    # Generate variants
    for probe in probes:
        src = src_dir / probe
        if not src.exists():
            print(f"MISSING: {src}")
            continue

        # Neutral variant
        neutral_text = transform_probe(
            src, NEUTRAL_MAP,
            NEUTRAL_TITLE_OLD, NEUTRAL_TITLE_NEW,
            NEUTRAL_SUBTITLE_OLD, NEUTRAL_SUBTITLE_NEW,
            PURPOSE_OLD, PURPOSE_NEW,
            NEUTRAL_OBP_OLD, NEUTRAL_OBP_NEW,
            USE_NOTATION_OLD, USE_NOTATION_NEW,
        )
        neutral_path = out_dir / probe.replace(".txt", "_NEUTRAL.txt")
        neutral_path.write_text(neutral_text, encoding="utf-8")
        print(f"  WROTE: {neutral_path}")

        # Ontology variant
        ontology_text = transform_probe(
            src, ONTOLOGY_MAP,
            ONTOLOGY_TITLE_OLD, ONTOLOGY_TITLE_NEW,
            ONTOLOGY_SUBTITLE_OLD, ONTOLOGY_SUBTITLE_NEW,
            PURPOSE_OLD, PURPOSE_NEW,
            ONTOLOGY_OBP_OLD, ONTOLOGY_OBP_NEW,
            USE_NOTATION_OLD, USE_NOTATION_NEW,
        )
        ontology_path = out_dir / probe.replace(".txt", "_ONTOLOGY.txt")
        ontology_path.write_text(ontology_text, encoding="utf-8")
        print(f"  WROTE: {ontology_path}")

    # Write tag-mapping reference
    mapping_doc = """# Tag Mapping Reference: Paper 4 v7.5 Experiment 1

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
"""
    (out_dir / "tag_mapping_v7_5.md").write_text(mapping_doc, encoding="utf-8")
    print(f"  WROTE: {out_dir / 'tag_mapping_v7_5.md'}")


if __name__ == "__main__":
    main()
