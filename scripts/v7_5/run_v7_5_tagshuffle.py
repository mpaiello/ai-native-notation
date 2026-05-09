#!/usr/bin/env python3
"""
ANN Paper 4 v7.5 — Experiment 1: Tag-Shuffle Ablation
Tests whether ANN's structural adoption rate persists when the canonical tag
tokens are replaced with (a) neutral generic labels or (b) an alternative
coherent semantic ontology. Five probes, two conditions, four architectures.

Reads probe variants from ../../probes/v7_5/ relative to this script's location.
Writes raw JSON results and per-architecture markdown reports to
../../reports/v7_5/api_<timestamp>/.

Pre-registered design: see ../../pre_registration/Paper4_v7_5_PreRegistration.md
SHA-256 of pre-reg at commit ff28e78:
    239acef5881ca05a10cbe916d2b24df54a854af7eb11683f3414f62462e940e3

Usage:
    $env:TOGETHER_API_KEY = "<your-key>"
    python run_v7_5_tagshuffle.py
    python run_v7_5_tagshuffle.py --models deepseek-v3 qwen3-235b   # subset
    python run_v7_5_tagshuffle.py --conditions NEUTRAL              # one condition
    python run_v7_5_tagshuffle.py --dry-run                         # no API calls

Michael Patrick Aiello | ORCID 0009-0009-1429-9844
May 2026
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

Together = None  # lazy-imported in main()


# Production model strings as used in v7.0.2 §6 Format Comparison runs
# (verified against supplementary materials replication_results JSON files).
MODELS = {
    "deepseek-v3": {
        "model_string": "deepseek-ai/DeepSeek-V3",
        "display_name": "DeepSeek-V3",
    },
    "qwen3-235b": {
        "model_string": "Qwen/Qwen3-235B-A22B-Instruct-2507-tput",
        "display_name": "Qwen3 235B",
    },
    "llama-3.3-70b": {
        "model_string": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "display_name": "Llama 3.3 70B",
    },
    "llama-4-maverick": {
        "model_string": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "display_name": "Llama 4 Maverick",
    },
}

DEFAULT_MODELS = ["deepseek-v3", "qwen3-235b", "llama-3.3-70b", "llama-4-maverick"]

CONDITIONS = ["NEUTRAL", "ONTOLOGY"]

PROBES = [
    ("PROBE_1", "Claims_Scope"),
    ("PROBE_2", "Symmetry_Defense"),
    ("PROBE_3", "Irreversibility"),
    ("PROBE_4", "Self_Reference"),
    ("PROBE_5", "State_Transfer"),
]


def load_probes(probe_dir: Path) -> dict:
    """Returns {(probe_id, condition): probe_text}."""
    probes = {}
    for probe_id, name in PROBES:
        for cond in CONDITIONS:
            fname = f"{probe_id}_{name}_{cond}.txt"
            fpath = probe_dir / fname
            if not fpath.exists():
                print(f"ERROR: Probe variant not found: {fpath}")
                sys.exit(1)
            probes[(probe_id, cond)] = fpath.read_text(encoding="utf-8")
    print(f"Loaded {len(probes)} probe variants from {probe_dir}")
    return probes


def run_probe(client, model_string: str, probe_text: str,
              temperature: float, seed: int, max_tokens: int = 4096) -> dict:
    start = time.time()
    kwargs = {
        "model": model_string,
        "messages": [{"role": "user", "content": probe_text}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if seed is not None:
        kwargs["seed"] = seed

    try:
        response = client.chat.completions.create(**kwargs)
        elapsed = time.time() - start
        choice = response.choices[0]
        return {
            "success": True,
            "content": choice.message.content,
            "finish_reason": choice.finish_reason,
            "model_returned": response.model,
            "tokens_prompt": response.usage.prompt_tokens if response.usage else None,
            "tokens_completion": response.usage.completion_tokens if response.usage else None,
            "elapsed_seconds": round(elapsed, 2),
            "temperature": temperature,
            "seed": seed,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "elapsed_seconds": round(time.time() - start, 2),
            "temperature": temperature,
            "seed": seed,
        }


def write_outputs(results: list, output_dir: Path, timestamp: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # Consolidated raw JSON (all trials in one file)
    json_path = output_dir / f"v7_5_tagshuffle_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nRaw results: {json_path}")

    # Per-model-per-condition markdown
    by_key = {}
    for r in results:
        key = (r["model_key"], r["condition"])
        by_key.setdefault(key, []).append(r)

    for (model_key, cond), rs in by_key.items():
        display = rs[0]["display_name"]
        md_path = output_dir / f"v7_5_tagshuffle_{model_key}_{cond}_{timestamp}.md"
        lines = [
            f"# v7.5 Tag-Shuffle Ablation: {display} ({cond})",
            f"## {timestamp[:10]}",
            "",
            "---",
            "",
            "## Metadata",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Model | {display} |",
            f"| Model string | `{rs[0]['model_string']}` |",
            f"| Condition | {cond} |",
            f"| Temperature | {rs[0]['temperature']} |",
            f"| Seed | {rs[0].get('seed', 'None')} |",
            "",
            "---",
            "",
        ]
        for r in sorted(rs, key=lambda x: x["probe_id"]):
            lines.append(f"### {r['probe_id']}: {r['probe_name']}")
            lines.append("")
            if r["success"]:
                lines.append(f"**Tokens:** {r.get('tokens_prompt', '?')} prompt, "
                             f"{r.get('tokens_completion', '?')} completion")
                lines.append(f"**Time:** {r['elapsed_seconds']}s")
                lines.append("")
                lines.append("#### Response")
                lines.append("")
                lines.append("```")
                lines.append(r["content"])
                lines.append("```")
            else:
                lines.append(f"**ERROR:** {r.get('error', 'unknown')}")
            lines.append("")
            lines.append("---")
            lines.append("")

        lines += [
            "## Scoring (to be completed by score_v7_5_tagshuffle.py)",
            "",
            "| Probe | Accuracy | Epistemic Fidelity | Structural Adoption | Total |",
            "|---|---|---|---|---|",
        ]
        for r in sorted(rs, key=lambda x: x["probe_id"]):
            lines.append(f"| {r['probe_id']} | _ | _ | _ | _/3 |")
        lines.append("| **Total** | | | | **_/15** |")
        lines.append("")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  Markdown: {md_path}")


def main():
    parser = argparse.ArgumentParser(description="v7.5 Experiment 1: Tag-Shuffle Ablation")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS,
                        choices=list(MODELS.keys()),
                        help="Model keys to test. Default: all four.")
    parser.add_argument("--conditions", nargs="+", default=CONDITIONS,
                        choices=CONDITIONS,
                        help="Conditions to run. Default: both.")
    parser.add_argument("--temperature", type=float, default=0.0,
                        help="Sampling temperature. Default: 0.0.")
    parser.add_argument("--seed", type=int, default=42,
                        help="Sampling seed. Default: 42.")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--probe-dir", type=Path, default=None,
                        help="Probe directory. Default: ../../probes/v7_5/")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Output directory. Default: ../../reports/v7_5/api_<timestamp>/")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan and exit without API calls.")
    args = parser.parse_args()

    global Together
    if not args.dry_run:
        try:
            from together import Together as _Together
            Together = _Together
        except ImportError:
            print("ERROR: 'together' package not installed. Run: pip install together")
            sys.exit(1)

    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: TOGETHER_API_KEY environment variable not set.")
        print('Set it: $env:TOGETHER_API_KEY = "<your-key>"')
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    probe_dir = args.probe_dir or (repo_root / "probes" / "v7_5")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    output_dir = args.output_dir or (repo_root / "reports" / "v7_5" / f"api_{timestamp}")

    print(f"v7.5 Experiment 1 — Tag-Shuffle Ablation")
    print(f"Timestamp: {timestamp}")
    print(f"Models: {', '.join(args.models)}")
    print(f"Conditions: {', '.join(args.conditions)}")
    print(f"Temp: {args.temperature}, Seed: {args.seed}, Max tokens: {args.max_tokens}")
    print(f"Probe dir: {probe_dir}")
    print(f"Output dir: {output_dir}")

    probes = load_probes(probe_dir)

    n_trials = len(args.models) * len(args.conditions) * len(PROBES)
    print(f"\nTotal trials planned: {n_trials}")

    if args.dry_run:
        print("DRY RUN. Exiting without API calls.")
        return 0

    client = Together(api_key=api_key)
    results = []
    trial_num = 0

    for model_key in args.models:
        m = MODELS[model_key]
        for cond in args.conditions:
            for probe_id, probe_name in PROBES:
                trial_num += 1
                key = (probe_id, cond)
                probe_text = probes[key]
                print(f"\n[{trial_num}/{n_trials}] {m['display_name']} | {cond} | {probe_id}")
                result = run_probe(client, m["model_string"], probe_text,
                                   args.temperature, args.seed, args.max_tokens)
                result.update({
                    "trial": trial_num,
                    "model_key": model_key,
                    "model_string": m["model_string"],
                    "display_name": m["display_name"],
                    "condition": cond,
                    "probe_id": probe_id,
                    "probe_name": probe_name,
                    "probe_chars": len(probe_text),
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                })
                if result["success"]:
                    print(f"  OK ({result['elapsed_seconds']}s, "
                          f"{result.get('tokens_completion', '?')} tokens)")
                else:
                    print(f"  ERROR: {result.get('error', 'unknown')}")
                results.append(result)

    print(f"\nCompleted {trial_num} trials.")
    print(f"Successes: {sum(1 for r in results if r['success'])}")
    print(f"Failures:  {sum(1 for r in results if not r['success'])}")

    write_outputs(results, output_dir, timestamp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
