#!/usr/bin/env python3
"""
ANN Paper 4 v7.5 — Experiment 2: Theorem-Proving Handoff Pilot

Two-stage propositional theorem-proving handoff. Agent A receives a problem
and produces an intermediate state in the condition-specific format. Agent B
receives the intermediate state and produces a final derivation.

Pilot configuration (per pre-registration):
- 20 SAT-validated problems (10 valid, 10 invalid)
- 5 conditions (ANN, JSON, XML, Structured English, Prose)
- 1 architecture pair: Llama-3.3-70B sender → DeepSeek-V3 receiver
- 100 trials minimum; --reverse-pair adds 100 more

Pre-registered design: see ../../pre_registration/Paper4_v7_5_PreRegistration.md
SHA-256 of pre-reg at commit ff28e78:
    239acef5881ca05a10cbe916d2b24df54a854af7eb11683f3414f62462e940e3

Usage:
    $env:TOGETHER_API_KEY = "<your-key>"
    python run_v7_5_pilot.py
    python run_v7_5_pilot.py --reverse-pair    # also run DeepSeek-V3→Llama
    python run_v7_5_pilot.py --conditions ANN JSON  # subset for debugging
    python run_v7_5_pilot.py --problems V01 V02 I01 --dry-run  # plan only

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


MODEL_LLAMA = {
    "key": "llama-3.3-70b",
    "model_string": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "display_name": "Llama 3.3 70B",
}
MODEL_DEEPSEEK = {
    "key": "deepseek-v3",
    "model_string": "deepseek-ai/DeepSeek-V3",
    "display_name": "DeepSeek-V3",
}

CONDITIONS = ["ANN", "JSON", "XML", "STRUCTURED_ENGLISH", "PROSE"]


# -------------------------------------------------------------------
# Sympy-string to readable-form converter (for the prompts)
# -------------------------------------------------------------------

def sympy_to_pretty(s: str) -> str:
    """Convert sympy str representation into readable logical notation."""
    out = s
    out = out.replace("Implies(", "imp(")
    out = out.replace("~", "¬")
    out = out.replace("&", "∧")
    out = out.replace("|", "∨")
    # imp(A, B) → (A → B)
    while "imp(" in out:
        idx = out.index("imp(")
        depth = 0
        for j in range(idx + 4, len(out)):
            ch = out[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                if depth == 0:
                    inner = out[idx + 4:j]
                    out = out[:idx] + "(" + inner.replace(", ", " → ") + ")" + out[j+1:]
                    break
                depth -= 1
    return out


# -------------------------------------------------------------------
# Prompt builders for Agent A and Agent B in each condition
# -------------------------------------------------------------------

def build_problem_text(problem: dict) -> str:
    premises_pretty = [sympy_to_pretty(p) for p in problem["premises_str"]]
    target_pretty = sympy_to_pretty(problem["target_str"])
    premises_block = "\n".join(f"  - {p}" for p in premises_pretty)
    return premises_block, target_pretty


def build_agent_a_prompt(problem: dict, condition: str) -> str:
    premises_block, target_pretty = build_problem_text(problem)
    base = f"""You are Agent A in a two-agent theorem-proving task. Your job is to
analyze a propositional logic problem and prepare a structured intermediate
state that Agent B will use to produce the final derivation.

PROBLEM:
Premises:
{premises_block}

Target: {target_pretty}

Standard inference rules available: modus ponens, modus tollens, hypothetical
syllogism, disjunctive syllogism, simplification, conjunction, addition.
"""
    instructions = {
        "ANN": """
Produce your intermediate state using AI-Native Notation (ANN). Use these blocks:
  @FORMAL [premise_N]   — restate each premise as an active premise.
  @LOGIC  [target]      — state the target proposition as the goal constraint.
  @DERIVE [plan]        — outline planned derivation steps with rule names.
  @TAXONOMY             — classify as confirmed / open / denied if conclusion is
                          provisional (use status markers ✓ CONFIRMED / ? OPEN / ✗ DENIED).
  @STATE                — final state for handoff to Agent B.

Output only the ANN-formatted intermediate state. Do not produce the final
derivation; that is Agent B's task.
""",
        "JSON": """
Produce your intermediate state as a JSON object with these fields:
{
  "premises": [<list of premise strings>],
  "target": "<target proposition>",
  "planned_steps": [
    {"step": 1, "rule": "<rule name>", "from": [<step refs or premise refs>],
     "produces": "<derived proposition>"},
    ...
  ],
  "expected_outcome": "<valid|invalid|uncertain>"
}

Output only the JSON object. Do not produce the final derivation.
""",
        "XML": """
Produce your intermediate state as XML with this structure:

<intermediate_state>
  <premises>
    <premise id="1"><![CDATA[ ... ]]></premise>
    ...
  </premises>
  <target><![CDATA[ ... ]]></target>
  <planned_steps>
    <step n="1" rule="..." from="...">
      <produces><![CDATA[ ... ]]></produces>
    </step>
    ...
  </planned_steps>
  <expected_outcome>valid|invalid|uncertain</expected_outcome>
</intermediate_state>

Output only the XML document. Do not produce the final derivation.
""",
        "STRUCTURED_ENGLISH": """
Produce your intermediate state as a numbered structured English document with
labeled sections:

1. Restated Premises:
   1.1 ...
   1.2 ...
2. Target:
   ...
3. Planned Derivation Steps:
   3.1 Apply [rule name] to [premises/steps] to derive [...]
   3.2 ...
4. Expected Outcome: valid / invalid / uncertain

Output only the structured English document. Do not produce the final derivation.
""",
        "PROSE": """
Write a paragraph or two of unstructured English describing the premises, the
target, your planned approach, the inference rules you intend to apply, and
your expectation about whether the target follows from the premises.

Do not use bullets, numbered lists, headings, or structured markup. Plain
prose only. Do not produce the final derivation; describe your plan for it.
""",
    }
    return base + instructions[condition]


def build_agent_b_prompt(intermediate_state: str, condition: str,
                          problem: dict) -> str:
    premises_block, target_pretty = build_problem_text(problem)
    base = f"""You are Agent B in a two-agent theorem-proving task. Agent A has
prepared an intermediate state describing a propositional logic problem and
its planned derivation. Your job is to produce the complete final derivation
or determine the target does not follow.

ORIGINAL PROBLEM:
Premises:
{premises_block}

Target: {target_pretty}

AGENT A's INTERMEDIATE STATE (in {condition} format):
---
{intermediate_state}
---

Standard inference rules: modus ponens (MP), modus tollens (MT), hypothetical
syllogism (HS), disjunctive syllogism (DS), simplification (Simp), conjunction
(Conj), addition (Add).

Your task:
1. Produce a complete derivation of the target from the premises, OR
2. State that the target does not follow and provide a counterexample
   valuation (which propositional variables are true/false such that all
   premises are true but the target is false).

REQUIRED OUTPUT FORMAT:

CONCLUSION: <one of: TARGET_FOLLOWS, TARGET_DOES_NOT_FOLLOW>

If TARGET_FOLLOWS, list each derivation step:
  Step 1: <derived_proposition>  [rule: MP/MT/HS/DS/Simp/Conj/Add; from: P1, P2, ...]
  Step 2: ...
  ...
  Final: <target>

If TARGET_DOES_NOT_FOLLOW, give the counterexample:
  Counterexample: A=True, B=False, ...
  Verification: All premises evaluate to True under this valuation; target evaluates to False.

Be precise. Each step must cite the rule used and the source steps or premises.
"""
    return base


# -------------------------------------------------------------------
# API caller
# -------------------------------------------------------------------

def call_model(client, model_string: str, prompt: str,
               temperature: float, seed: int, max_tokens: int = 4096) -> dict:
    start = time.time()
    kwargs = {
        "model": model_string,
        "messages": [{"role": "user", "content": prompt}],
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
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "elapsed_seconds": round(time.time() - start, 2),
        }


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="v7.5 Experiment 2: Theorem-Proving Handoff Pilot")
    parser.add_argument("--conditions", nargs="+", default=CONDITIONS, choices=CONDITIONS)
    parser.add_argument("--problems", nargs="+", default=None,
                        help="Subset of problem IDs (e.g., V01 V02 I01). Default: all 20.")
    parser.add_argument("--reverse-pair", action="store_true",
                        help="Also run DeepSeek-V3 → Llama-3.3-70B (200 total trials).")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--problem-set", type=Path, default=None,
                        help="Path to v7_5_problem_set.json. Default: ../../problems/v7_5/v7_5_problem_set.json")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
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
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    problem_set_path = args.problem_set or (repo_root / "problems" / "v7_5" / "v7_5_problem_set.json")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    output_dir = args.output_dir or (repo_root / "reports" / "v7_5" / f"pilot_{timestamp}")

    if not problem_set_path.exists():
        print(f"ERROR: Problem set not found: {problem_set_path}")
        sys.exit(1)

    all_problems = json.loads(problem_set_path.read_text())
    if args.problems:
        all_problems = [p for p in all_problems if p["id"] in args.problems]
        if not all_problems:
            print(f"ERROR: No problems matched filter: {args.problems}")
            sys.exit(1)

    pairs = [(MODEL_LLAMA, MODEL_DEEPSEEK)]
    if args.reverse_pair:
        pairs.append((MODEL_DEEPSEEK, MODEL_LLAMA))

    n_trials = len(all_problems) * len(args.conditions) * len(pairs)
    print(f"v7.5 Experiment 2 — Theorem-Proving Handoff Pilot")
    print(f"Timestamp: {timestamp}")
    print(f"Conditions: {', '.join(args.conditions)}")
    print(f"Problems: {len(all_problems)} ({sum(1 for p in all_problems if p['expected_validity'])} valid, "
          f"{sum(1 for p in all_problems if not p['expected_validity'])} invalid)")
    print(f"Pairs: {len(pairs)}")
    print(f"Total trials planned: {n_trials}")
    print(f"Output dir: {output_dir}")

    if args.dry_run:
        print("DRY RUN. Exiting without API calls.")
        return 0

    client = Together(api_key=api_key)
    results = []
    trial_num = 0

    for sender, receiver in pairs:
        pair_label = f"{sender['key']}__{receiver['key']}"
        for cond in args.conditions:
            for problem in all_problems:
                trial_num += 1
                print(f"\n[{trial_num}/{n_trials}] {pair_label} | {cond} | {problem['id']}")

                # Stage 1: Agent A
                a_prompt = build_agent_a_prompt(problem, cond)
                a_result = call_model(client, sender["model_string"], a_prompt,
                                      args.temperature, args.seed, args.max_tokens)
                if not a_result["success"]:
                    print(f"  STAGE A ERROR: {a_result.get('error')}")
                    results.append({
                        "trial": trial_num,
                        "pair": pair_label,
                        "sender": sender,
                        "receiver": receiver,
                        "condition": cond,
                        "problem_id": problem["id"],
                        "problem_name": problem["name"],
                        "expected_validity": problem["expected_validity"],
                        "stage_a": a_result,
                        "stage_b": {"success": False, "error": "skipped: stage A failed"},
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    })
                    continue

                intermediate = a_result["content"]

                # Stage 2: Agent B
                b_prompt = build_agent_b_prompt(intermediate, cond, problem)
                b_result = call_model(client, receiver["model_string"], b_prompt,
                                      args.temperature, args.seed, args.max_tokens)

                trial = {
                    "trial": trial_num,
                    "pair": pair_label,
                    "sender": sender,
                    "receiver": receiver,
                    "condition": cond,
                    "problem_id": problem["id"],
                    "problem_name": problem["name"],
                    "expected_validity": problem["expected_validity"],
                    "premises_str": problem["premises_str"],
                    "target_str": problem["target_str"],
                    "stage_a_prompt_chars": len(a_prompt),
                    "stage_a": a_result,
                    "stage_b_prompt_chars": len(b_prompt),
                    "stage_b": b_result,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                }
                if b_result["success"]:
                    print(f"  OK (A: {a_result['elapsed_seconds']}s, "
                          f"B: {b_result['elapsed_seconds']}s)")
                else:
                    print(f"  STAGE B ERROR: {b_result.get('error')}")
                results.append(trial)

    print(f"\nCompleted {trial_num} trials.")
    succeed_a = sum(1 for r in results if r["stage_a"]["success"])
    succeed_b = sum(1 for r in results if r["stage_b"]["success"])
    print(f"Stage A successes: {succeed_a}/{trial_num}")
    print(f"Stage B successes: {succeed_b}/{trial_num}")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_json = output_dir / f"v7_5_pilot_{timestamp}.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nRaw results: {out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
