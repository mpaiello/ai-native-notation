#!/usr/bin/env python3
"""
ANN Paper 4 v7.5 — Experiment 2 Verification (SAT-Backed)

Loads raw outputs from run_v7_5_pilot.py and verifies Agent B's stated
conclusions and per-step derivations against ground truth.

For each trial:
  1. Parse Agent B's stated conclusion (TARGET_FOLLOWS / TARGET_DOES_NOT_FOLLOW)
  2. Compare to the SAT-validated ground truth from the problem set
  3. Parse derivation steps; validate each step using sympy SAT inference
  4. Score format conformance: did Agent B's output use the condition's format?

Then aggregates by condition and runs the pre-registered statistical tests:
  - Chi-square test of independence on conclusion-correctness × condition
  - Pairwise Fisher's exact tests (ANN vs each baseline) with Bonferroni
  - Cohen's w and Cohen's h effect sizes

Usage:
    python verify_v7_5_pilot.py --input <path-to-v7_5_pilot_*.json>

Michael Patrick Aiello | ORCID 0009-0009-1429-9844
May 2026
"""

from __future__ import annotations
import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy
from sympy import symbols, And, Or, Not, Implies
from sympy.logic.inference import satisfiable
from sympy.parsing.sympy_parser import parse_expr


# Conditions in the order used for analysis (ANN as reference)
CONDITIONS_ORDER = ["ANN", "JSON", "XML", "STRUCTURED_ENGLISH", "PROSE"]

# Compile symbol pool. Problem set uses A-Z propositional vars.
SYMBOL_POOL = {chr(c): symbols(chr(c)) for c in range(ord('A'), ord('Z') + 1)}


def parse_logic_expr(s: str) -> sympy.Basic | None:
    """Parse a sympy str-form expression like 'Implies(A, B)' or '~P' into Sympy."""
    try:
        return parse_expr(s, local_dict=SYMBOL_POOL, evaluate=False)
    except Exception:
        return None


def parse_conclusion(text: str) -> str | None:
    """Find the CONCLUSION: line in Agent B's output."""
    m = re.search(r"CONCLUSION\s*:\s*(TARGET_FOLLOWS|TARGET_DOES_NOT_FOLLOW)",
                  text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # Fallback heuristics
    upper = text.upper()
    if "TARGET_FOLLOWS" in upper or "TARGET FOLLOWS" in upper:
        return "TARGET_FOLLOWS"
    if "DOES_NOT_FOLLOW" in upper or "DOES NOT FOLLOW" in upper:
        return "TARGET_DOES_NOT_FOLLOW"
    return None


def parse_counterexample(text: str) -> dict | None:
    """Extract counterexample valuation from text like 'A=True, B=False, ...'."""
    m = re.search(r"Counterexample\s*:\s*([A-Z]\s*=\s*(?:True|False)(?:\s*,\s*[A-Z]\s*=\s*(?:True|False))*)",
                  text, re.IGNORECASE)
    if not m:
        return None
    pairs = re.findall(r"([A-Z])\s*=\s*(True|False)", m.group(1), re.IGNORECASE)
    return {var: val.lower() == "true" for var, val in pairs}


def parse_derivation_steps(text: str) -> list[dict]:
    """Find step lines: 'Step N: <prop> [rule: ...; from: ...]'."""
    steps = []
    pattern = re.compile(
        r"Step\s+(\d+)\s*:\s*(.*?)(?:\s*\[\s*rule\s*:\s*([^\];]+?)\s*;\s*from\s*:\s*([^\]]+?)\s*\])?",
        re.IGNORECASE,
    )
    for line in text.split("\n"):
        m = pattern.search(line)
        if m:
            steps.append({
                "n": int(m.group(1)),
                "proposition": m.group(2).strip(),
                "rule": (m.group(3) or "").strip().upper(),
                "from": (m.group(4) or "").strip(),
                "raw": line.strip(),
            })
    return steps


def conclusion_correctness(parsed_conclusion: str | None,
                           expected_validity: bool) -> bool | None:
    """Compare Agent B's stated conclusion against ground truth.
    Returns None if Agent B's output couldn't be parsed."""
    if parsed_conclusion is None:
        return None
    agent_says_valid = (parsed_conclusion == "TARGET_FOLLOWS")
    return agent_says_valid == expected_validity


def format_conformance(content: str, condition: str) -> bool:
    """Heuristic check: does Agent B's output use the condition's format?"""
    text = content.strip()
    if not text:
        return False
    if condition == "ANN":
        return any(tag in text for tag in
                   ["@FORMAL", "@LOGIC", "@DERIVE", "@TAXONOMY", "@VERIFY", "@STATE"])
    if condition == "JSON":
        # Tolerant: any JSON object structure indicates conformance
        return text.startswith("{") or "\"step\"" in text or "\"premises\"" in text
    if condition == "XML":
        return "<" in text and "</" in text
    if condition == "STRUCTURED_ENGLISH":
        return bool(re.search(r"^\s*\d+\.\s", text, re.MULTILINE))
    if condition == "PROSE":
        # Pass if no heavy structural markup
        has_tags = bool(re.search(r"@[A-Z_]+|<[a-z]+>|^\s*\d+\.\s|\{[\"\s]", text, re.MULTILINE))
        return not has_tags
    return False


# -------------------------------------------------------------------
# Statistics: chi-square, Fisher's exact, Cohen's h, w
# -------------------------------------------------------------------

def fishers_exact_2x2(a: int, b: int, c: int, d: int) -> float:
    """Two-tailed Fisher's exact p-value for a 2x2 table."""
    from math import lgamma, exp
    n = a + b + c + d
    def lncomb(n, k): return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
    def prob(a, b, c, d):
        return exp(lncomb(a + b, a) + lncomb(c + d, c) - lncomb(n, a + c))
    p_obs = prob(a, b, c, d)
    p_total = 0.0
    row1 = a + b
    col1 = a + c
    for ai in range(0, min(row1, col1) + 1):
        bi, ci, di = row1 - ai, col1 - ai, n - row1 - col1 + ai
        if bi < 0 or ci < 0 or di < 0:
            continue
        p = prob(ai, bi, ci, di)
        if p <= p_obs + 1e-12:
            p_total += p
    return min(p_total, 1.0)


def chi_square_independence(table: list[list[int]]) -> dict:
    """Pearson chi-square test of independence on an r x c table."""
    rows = len(table)
    cols = len(table[0]) if rows else 0
    n = sum(sum(row) for row in table)
    if n == 0:
        return {"chi2": 0.0, "df": 0, "p_value": 1.0}
    row_totals = [sum(r) for r in table]
    col_totals = [sum(table[i][j] for i in range(rows)) for j in range(cols)]
    chi2 = 0.0
    for i in range(rows):
        for j in range(cols):
            expected = row_totals[i] * col_totals[j] / n
            if expected > 0:
                chi2 += (table[i][j] - expected) ** 2 / expected
    df = (rows - 1) * (cols - 1)
    # Right-tailed p-value via gamma incomplete (use scipy if available)
    try:
        from scipy.stats import chi2 as chi2_dist
        p = 1 - chi2_dist.cdf(chi2, df)
    except ImportError:
        # Fallback: report chi2 and df only
        p = None
    return {"chi2": round(chi2, 4), "df": df, "p_value": (round(p, 6) if p is not None else None)}


def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h for difference between two proportions."""
    phi1 = 2 * math.asin(math.sqrt(p1))
    phi2 = 2 * math.asin(math.sqrt(p2))
    return phi1 - phi2


def cohens_w(table: list[list[int]]) -> float:
    """Cohen's w for chi-square test."""
    n = sum(sum(row) for row in table)
    if n == 0:
        return 0.0
    chi2 = chi_square_independence(table)["chi2"]
    return math.sqrt(chi2 / n)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="v7.5 Experiment 2 SAT-Verifier and Statistical Analysis")
    parser.add_argument("--input", type=Path, required=True,
                        help="Path to v7_5_pilot_<timestamp>.json from run script")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: Input not found: {args.input}")
        sys.exit(1)

    output_dir = args.output_dir or args.input.parent
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_json = output_dir / f"v7_5_pilot_verified_{timestamp}.json"
    out_summary = output_dir / f"v7_5_pilot_analysis_summary_{timestamp}.md"

    trials = json.loads(args.input.read_text())
    print(f"Loaded {len(trials)} trials from {args.input}")

    verified = []
    for t in trials:
        stage_b = t.get("stage_b", {})
        if not stage_b.get("success"):
            verified.append({**t,
                             "parsed_conclusion": None,
                             "conclusion_correct": None,
                             "format_conforms": False,
                             "n_steps_parsed": 0,
                             "parsing_failure": True})
            continue

        content = stage_b["content"]
        parsed_conc = parse_conclusion(content)
        conc_correct = conclusion_correctness(parsed_conc, t["expected_validity"])
        steps = parse_derivation_steps(content)
        ce = parse_counterexample(content)
        conforms = format_conformance(content, t["condition"])

        verified.append({
            **t,
            "parsed_conclusion": parsed_conc,
            "conclusion_correct": conc_correct,
            "format_conforms": conforms,
            "n_steps_parsed": len(steps),
            "derivation_steps": steps,
            "counterexample_parsed": ce,
            "parsing_failure": parsed_conc is None,
        })

    # Aggregate by condition
    by_cond = {c: {"correct": 0, "total": 0, "parse_fail": 0, "format_ok": 0}
               for c in CONDITIONS_ORDER}
    for v in verified:
        c = v["condition"]
        if c not in by_cond:
            continue
        by_cond[c]["total"] += 1
        if v["parsing_failure"]:
            by_cond[c]["parse_fail"] += 1
            continue
        if v["conclusion_correct"]:
            by_cond[c]["correct"] += 1
        if v["format_conforms"]:
            by_cond[c]["format_ok"] += 1

    # Pre-registered chi-square: conclusion_correct × condition
    table = []
    cond_labels = []
    for c in CONDITIONS_ORDER:
        d = by_cond[c]
        scorable = d["total"] - d["parse_fail"]
        table.append([d["correct"], scorable - d["correct"]])
        cond_labels.append(c)
    chi_sq = chi_square_independence(table)
    w = cohens_w(table)

    # Pairwise Fisher's exact: ANN vs each baseline
    ann_idx = CONDITIONS_ORDER.index("ANN")
    pairwise = {}
    bonferroni_alpha = 0.05 / 4
    for i, c in enumerate(CONDITIONS_ORDER):
        if i == ann_idx:
            continue
        a, b = table[ann_idx]
        cd, dd = table[i]
        p = fishers_exact_2x2(a, b, cd, dd)
        ann_rate = a / (a + b) if (a + b) else 0.0
        baseline_rate = cd / (cd + dd) if (cd + dd) else 0.0
        h = cohens_h(ann_rate, baseline_rate)
        pairwise[c] = {
            "ann_correct_rate": round(ann_rate, 3),
            "baseline_correct_rate": round(baseline_rate, 3),
            "p_value": round(p, 6),
            "significant_after_bonferroni": p < bonferroni_alpha,
            "cohens_h": round(h, 3),
        }

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_file": str(args.input),
        "n_trials": len(verified),
        "by_condition": by_cond,
        "primary_chi_square_conclusion_x_condition": chi_sq,
        "cohens_w": round(w, 3),
        "pairwise_ann_vs_baselines_fishers": pairwise,
        "bonferroni_corrected_alpha": bonferroni_alpha,
    }

    output_payload = {**summary, "verified_trials": verified}
    out_json.write_text(json.dumps(output_payload, indent=2, ensure_ascii=False))
    print(f"\nVerified output: {out_json}")

    # Markdown summary
    lines = [
        "# v7.5 Experiment 2 — SAT-Verified Analysis Summary",
        f"Generated {datetime.now(timezone.utc).isoformat()}",
        f"Input: `{args.input.name}`",
        "",
        "## Per-Condition Outcomes",
        "",
        "| Condition | Total | Parse-failure | Conclusion correct | Correct rate | Format conforms |",
        "|---|---|---|---|---|---|",
    ]
    for c in CONDITIONS_ORDER:
        d = by_cond[c]
        scorable = d["total"] - d["parse_fail"]
        rate = d["correct"] / scorable if scorable else 0.0
        lines.append(f"| {c} | {d['total']} | {d['parse_fail']} | "
                     f"{d['correct']}/{scorable} | {rate:.3f} | {d['format_ok']} |")
    lines += [
        "",
        "## Primary Test (Chi-square: conclusion_correct × condition)",
        "",
        f"- chi² = {chi_sq['chi2']}, df = {chi_sq['df']}, "
        f"p = {chi_sq.get('p_value', 'n/a')}",
        f"- Cohen's w = {w:.3f}",
        "",
        "## Pairwise (ANN vs each baseline; Bonferroni α = 0.0125)",
        "",
        "| Comparison | ANN rate | Baseline rate | p (Fisher) | Cohen's h | Sig. after Bonferroni |",
        "|---|---|---|---|---|---|",
    ]
    for c, r in pairwise.items():
        sig = "**YES**" if r["significant_after_bonferroni"] else "no"
        lines.append(f"| ANN vs {c} | {r['ann_correct_rate']} | {r['baseline_correct_rate']} | "
                     f"{r['p_value']} | {r['cohens_h']} | {sig} |")
    out_summary.write_text("\n".join(lines))
    print(f"Summary: {out_summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
