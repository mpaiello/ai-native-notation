#!/usr/bin/env python3
"""
ANN Paper 4 v7.5 — Consolidated Analysis Script

Loads the scored Experiment 1 output (from score_v7_5_tagshuffle.py) and
the verified Experiment 2 output (from verify_v7_5_pilot.py), consolidates
results into manuscript-ready tables and figures, and runs the pre-registered
interpretive-threshold check.

Usage:
    python v7_5_analyze.py --exp1 <scored.json> --exp2 <verified.json>
    python v7_5_analyze.py --exp1 <scored.json>          # Exp 1 only
    python v7_5_analyze.py --exp2 <verified.json>        # Exp 2 only

Outputs:
    v7_5_results_tables.md       — manuscript-ready Markdown tables
    v7_5_interpretive_threshold_check.md — pre-committed framing decision

Michael Patrick Aiello | ORCID 0009-0009-1429-9844
May 2026
"""

from __future__ import annotations
import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict


# Pre-registered interpretive thresholds (from Paper4_v7_5_PreRegistration.md §3.7, §4.8)
EXP1_THRESHOLDS = {
    "both_match_baseline": "Tag tokens not load-bearing; schema-plus-instructions is the active pattern. ANN repositioned as one realization of a pattern; convergence-based promotion mechanism reframed at the schema level.",
    "neutral_lower_only": "Coherent ontology required; specific ANN tags not. Convergence mechanism survives at ontology level; ANN is a particular coherent ontology, not the only one.",
    "both_lower_than_baseline": "ANN-specific tag semantics load-bearing. Format-mimicry counter-hypothesis directly refuted.",
    "anomalous": "Anomalous; possible training-data contamination on ANN-specific tokens. Investigated; result reported with caveat.",
}

EXP2_THRESHOLDS = {
    "ann_beats_all": "Pilot supports H2. v7.5 frames pilot as preliminary evidence; full §4.2 execution recommended.",
    "ann_beats_some": "Partial support. Full §4.2 should disambiguate which baselines.",
    "no_difference": "Null at pilot scale. v7.5 reports honestly; full §4.2 may still be warranted; ANN's coordination claim re-scoped.",
    "ann_loses": "Negative pilot. v7.5 reports honestly; v8 priorities reassessed.",
}


def analyze_exp1(scored_path: Path) -> dict:
    """Process scored Experiment 1 output and return analysis dict."""
    data = json.loads(scored_path.read_text(encoding="utf-8"))
    trials = data.get("scored_trials") or data
    if isinstance(trials, dict):
        trials = trials.get("scored_trials", [])

    # Aggregate by (condition, model, dimension)
    # Use Rater A scores as primary (Rater B serves as concordance check via kappa)
    aggregate = defaultdict(lambda: {"trials": 0, "accuracy": 0,
                                     "epistemic_fidelity": 0,
                                     "structural_adoption": 0})
    for t in trials:
        if not t.get("rater_a", {}).get("success"):
            continue
        scores = t["rater_a"]["scores"]
        key = (t["condition"], t["display_name"])
        aggregate[key]["trials"] += 1
        for d in ["accuracy", "epistemic_fidelity", "structural_adoption"]:
            if scores.get(d):
                aggregate[key][d] += 1

    # Adoption rate per condition (collapsing across models)
    adoption_by_cond = defaultdict(lambda: {"adopted": 0, "total": 0})
    for (cond, model), v in aggregate.items():
        adoption_by_cond[cond]["adopted"] += v["structural_adoption"]
        adoption_by_cond[cond]["total"] += v["trials"]

    return {
        "kappa_per_dimension": data.get("kappa_per_dimension"),
        "n_disagreements": data.get("n_disagreements"),
        "by_condition_model": {f"{c}|{m}": v for (c, m), v in aggregate.items()},
        "adoption_by_condition": dict(adoption_by_cond),
    }


def analyze_exp2(verified_path: Path) -> dict:
    data = json.loads(verified_path.read_text(encoding="utf-8"))
    return {
        "by_condition": data.get("by_condition", {}),
        "primary_chi_square": data.get("primary_chi_square_conclusion_x_condition"),
        "cohens_w": data.get("cohens_w"),
        "pairwise": data.get("pairwise_ann_vs_baselines_fishers", {}),
    }


def determine_exp1_threshold(adoption_by_cond: dict) -> tuple[str, str]:
    """Return (threshold_key, threshold_text) per pre-registered logic."""
    # We need a v7.0.2 baseline reference. For now, document the interpretation
    # logic. Actual threshold check requires loading the v7.0.2 §6 baseline data.
    adoption_rates = {c: (d["adopted"] / d["total"] if d["total"] else 0.0)
                      for c, d in adoption_by_cond.items()}
    # Placeholder: report rates; actual threshold requires baseline ANN rate.
    return "data_collected", (
        "Adoption rates: " +
        ", ".join(f"{c}={r:.3f}" for c, r in adoption_rates.items()) +
        ". Compare against v7.0.2 §6 baseline ANN rate (4/4 = 1.000) to determine threshold."
    )


def determine_exp2_threshold(pairwise: dict) -> tuple[str, str]:
    """Apply pre-committed threshold logic."""
    sig_baselines = [c for c, r in pairwise.items()
                     if r.get("significant_after_bonferroni")
                     and r.get("ann_correct_rate", 0) > r.get("baseline_correct_rate", 0)]
    sig_against = [c for c, r in pairwise.items()
                   if r.get("significant_after_bonferroni")
                   and r.get("ann_correct_rate", 0) < r.get("baseline_correct_rate", 0)]
    n_baselines = len(pairwise)
    if len(sig_baselines) == n_baselines and not sig_against:
        return "ann_beats_all", EXP2_THRESHOLDS["ann_beats_all"]
    if sig_baselines and not sig_against:
        return "ann_beats_some", EXP2_THRESHOLDS["ann_beats_some"]
    if sig_against:
        return "ann_loses", EXP2_THRESHOLDS["ann_loses"]
    return "no_difference", EXP2_THRESHOLDS["no_difference"]


def write_tables(exp1: dict | None, exp2: dict | None, out_path: Path) -> None:
    lines = ["# v7.5 Results Tables\n",
             f"Generated {datetime.now(timezone.utc).isoformat()}\n", ""]

    if exp1:
        lines.append("## Experiment 1 — Tag-Shuffle Ablation\n")
        lines.append("### Inter-Rater Agreement\n")
        if exp1.get("kappa_per_dimension"):
            lines.append("| Dimension | n | Cohen's kappa | Agreement rate |")
            lines.append("|---|---|---|---|")
            for d, v in exp1["kappa_per_dimension"].items():
                lines.append(f"| {d} | {v.get('n','-')} | {v.get('kappa','-')} | {v.get('agreement_rate','-')} |")
            lines.append("")
        lines.append("### Adoption by Condition (Rater A primary)\n")
        lines.append("| Condition | Adopted | Total | Rate |")
        lines.append("|---|---|---|---|")
        for c, d in exp1["adoption_by_condition"].items():
            rate = d["adopted"] / d["total"] if d["total"] else 0
            lines.append(f"| {c} | {d['adopted']} | {d['total']} | {rate:.3f} |")
        lines.append("")
        lines.append("### Per-Condition × Model Detail\n")
        lines.append("| Condition | Model | Trials | Accuracy | Epistemic | Structural |")
        lines.append("|---|---|---|---|---|---|")
        for key, v in exp1["by_condition_model"].items():
            cond, model = key.split("|", 1)
            lines.append(f"| {cond} | {model} | {v['trials']} | "
                         f"{v['accuracy']}/{v['trials']} | "
                         f"{v['epistemic_fidelity']}/{v['trials']} | "
                         f"{v['structural_adoption']}/{v['trials']} |")
        lines.append("")

    if exp2:
        lines.append("## Experiment 2 — Theorem-Proving Pilot\n")
        lines.append("### Per-Condition Outcomes\n")
        lines.append("| Condition | Total | Parse-fail | Correct | Rate |")
        lines.append("|---|---|---|---|---|")
        for c, d in exp2["by_condition"].items():
            scorable = d["total"] - d["parse_fail"]
            rate = d["correct"] / scorable if scorable else 0.0
            lines.append(f"| {c} | {d['total']} | {d['parse_fail']} | "
                         f"{d['correct']}/{scorable} | {rate:.3f} |")
        lines.append("")
        cs = exp2.get("primary_chi_square") or {}
        lines.append(f"### Primary Chi-Square\n")
        lines.append(f"chi² = {cs.get('chi2')}, df = {cs.get('df')}, "
                     f"p = {cs.get('p_value')}, Cohen's w = {exp2.get('cohens_w')}\n")
        lines.append("### Pairwise (ANN vs each baseline)\n")
        lines.append("| Comparison | ANN rate | Baseline rate | Fisher p | Cohen's h | Sig. (Bonferroni) |")
        lines.append("|---|---|---|---|---|---|")
        for c, r in exp2["pairwise"].items():
            sig = "**YES**" if r.get("significant_after_bonferroni") else "no"
            lines.append(f"| ANN vs {c} | {r.get('ann_correct_rate')} | "
                         f"{r.get('baseline_correct_rate')} | {r.get('p_value')} | "
                         f"{r.get('cohens_h')} | {sig} |")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_threshold_check(exp1_decision, exp2_decision, out_path: Path) -> None:
    lines = ["# v7.5 Pre-Committed Interpretive Threshold Check\n",
             f"Generated {datetime.now(timezone.utc).isoformat()}\n",
             "Per Paper4_v7_5_PreRegistration.md §3.7 and §4.8.\n", ""]
    if exp1_decision:
        key, text = exp1_decision
        lines.append(f"## Experiment 1: `{key}`\n")
        lines.append(f"{text}\n")
        lines.append("")
    if exp2_decision:
        key, text = exp2_decision
        lines.append(f"## Experiment 2: `{key}`\n")
        lines.append(f"{text}\n")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="v7.5 Consolidated Analysis")
    parser.add_argument("--exp1", type=Path, default=None,
                        help="Path to v7_5_tagshuffle_scored_*.json")
    parser.add_argument("--exp2", type=Path, default=None,
                        help="Path to v7_5_pilot_verified_*.json")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    if not args.exp1 and not args.exp2:
        print("ERROR: provide at least one of --exp1, --exp2")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    exp1_data = analyze_exp1(args.exp1) if args.exp1 else None
    exp2_data = analyze_exp2(args.exp2) if args.exp2 else None

    exp1_decision = determine_exp1_threshold(exp1_data["adoption_by_condition"]) if exp1_data else None
    exp2_decision = determine_exp2_threshold(exp2_data["pairwise"]) if exp2_data else None

    tables_path = args.output_dir / "v7_5_results_tables.md"
    threshold_path = args.output_dir / "v7_5_interpretive_threshold_check.md"
    write_tables(exp1_data, exp2_data, tables_path)
    write_threshold_check(exp1_decision, exp2_decision, threshold_path)

    print(f"Tables: {tables_path}")
    print(f"Threshold check: {threshold_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
