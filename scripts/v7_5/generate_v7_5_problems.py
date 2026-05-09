#!/usr/bin/env python3
"""
Generate and validate the 20-problem propositional theorem-proving set
for Paper 4 v7.5 Experiment 2 pilot.

For each problem:
  - Define premises and target as sympy Boolean expressions.
  - Validate via satisfiable(Premises ∧ ¬Target):
      UNSAT  => target follows (valid argument)
      SAT    => target does not follow (invalid argument); record counterexample.
  - Provide a canonical derivation sketch for valid problems.
  - Provide a counterexample valuation for invalid problems.
  - Export problem set as JSON for use in the multi-agent pilot.

Symbol convention: capital letters A through Z used as propositional variables.
"""

import json
import sympy
from sympy import symbols, And, Or, Not, Implies
from sympy.logic.inference import satisfiable
from pathlib import Path

# Define propositional symbols
A, B, C, D, E, F, G, H, I, J, K, L, M, N = symbols("A B C D E F G H I J K L M N")
P, Q, R, S, T, U, V, W, X, Y, Z = symbols("P Q R S T U V W X Y Z")

# -------------------------------------------------------------------
# VALID PROBLEMS (target follows from premises)
# -------------------------------------------------------------------

valid_problems = [
    {
        "id": "V01",
        "name": "Modus ponens chain (depth 3)",
        "premises": [Implies(A, B), Implies(B, C), Implies(C, D), A],
        "target": D,
        "rules_used": ["modus_ponens"],
        "expected_steps": 3,
        "derivation_sketch": [
            "A, A→B ⊢ B (MP)",
            "B, B→C ⊢ C (MP)",
            "C, C→D ⊢ D (MP)",
        ],
    },
    {
        "id": "V02",
        "name": "Modus tollens with hypothetical syllogism",
        "premises": [Implies(P, Q), Implies(Q, R), Not(R)],
        "target": Not(P),
        "rules_used": ["hypothetical_syllogism", "modus_tollens"],
        "expected_steps": 2,
        "derivation_sketch": [
            "P→Q, Q→R ⊢ P→R (HS)",
            "P→R, ¬R ⊢ ¬P (MT)",
        ],
    },
    {
        "id": "V03",
        "name": "Disjunctive syllogism with conjunction elimination",
        "premises": [And(A, B), Or(Not(B), C), Implies(C, D)],
        "target": D,
        "rules_used": ["simplification", "disjunctive_syllogism", "modus_ponens"],
        "expected_steps": 3,
        "derivation_sketch": [
            "A∧B ⊢ B (Simp)",
            "B, ¬B∨C ⊢ C (DS)",
            "C, C→D ⊢ D (MP)",
        ],
    },
    {
        "id": "V04",
        "name": "Constructive dilemma",
        "premises": [Or(E, F), Implies(E, G), Implies(F, H), Not(H)],
        "target": G,
        "rules_used": ["modus_tollens", "disjunctive_syllogism", "modus_ponens"],
        "expected_steps": 3,
        "derivation_sketch": [
            "¬H, F→H ⊢ ¬F (MT)",
            "¬F, E∨F ⊢ E (DS)",
            "E, E→G ⊢ G (MP)",
        ],
    },
    {
        "id": "V05",
        "name": "Disjunction introduction via implication chain",
        "premises": [Implies(Or(P, Q), R), P, Implies(R, S), T],
        "target": And(S, T),
        "rules_used": ["addition", "modus_ponens", "conjunction"],
        "expected_steps": 4,
        "derivation_sketch": [
            "P ⊢ P∨Q (Add)",
            "P∨Q, (P∨Q)→R ⊢ R (MP)",
            "R, R→S ⊢ S (MP)",
            "S, T ⊢ S∧T (Conj)",
        ],
    },
    {
        "id": "V06",
        "name": "Multi-step disjunctive elimination",
        "premises": [Or(A, B), Not(A), Implies(B, C), Implies(C, D), Implies(D, E)],
        "target": E,
        "rules_used": ["disjunctive_syllogism", "modus_ponens"],
        "expected_steps": 4,
        "derivation_sketch": [
            "¬A, A∨B ⊢ B (DS)",
            "B, B→C ⊢ C (MP)",
            "C, C→D ⊢ D (MP)",
            "D, D→E ⊢ E (MP)",
        ],
    },
    {
        "id": "V07",
        "name": "Conjunction-antecedent implication",
        "premises": [Implies(And(P, Q), R), Implies(R, S), Implies(S, T), P, Q],
        "target": T,
        "rules_used": ["conjunction", "modus_ponens"],
        "expected_steps": 4,
        "derivation_sketch": [
            "P, Q ⊢ P∧Q (Conj)",
            "P∧Q, (P∧Q)→R ⊢ R (MP)",
            "R, R→S ⊢ S (MP)",
            "S, S→T ⊢ T (MP)",
        ],
    },
    {
        "id": "V08",
        "name": "Modus tollens triggering disjunctive elimination",
        "premises": [Implies(A, B), Not(B), Or(A, C), Implies(C, D)],
        "target": D,
        "rules_used": ["modus_tollens", "disjunctive_syllogism", "modus_ponens"],
        "expected_steps": 3,
        "derivation_sketch": [
            "¬B, A→B ⊢ ¬A (MT)",
            "¬A, A∨C ⊢ C (DS)",
            "C, C→D ⊢ D (MP)",
        ],
    },
    {
        "id": "V09",
        "name": "Conjunction within disjunctive context",
        "premises": [Not(P), Or(P, R), Implies(R, And(S, T)), Implies(T, U)],
        "target": U,
        "rules_used": ["disjunctive_syllogism", "modus_ponens", "simplification"],
        "expected_steps": 4,
        "derivation_sketch": [
            "¬P, P∨R ⊢ R (DS)",
            "R, R→(S∧T) ⊢ S∧T (MP)",
            "S∧T ⊢ T (Simp)",
            "T, T→U ⊢ U (MP)",
        ],
    },
    {
        "id": "V10",
        "name": "Long chain through conjunction split",
        "premises": [A, Implies(A, B), Implies(B, And(C, D)),
                     Implies(C, E), Implies(D, F), Implies(And(E, F), G)],
        "target": G,
        "rules_used": ["modus_ponens", "simplification", "conjunction"],
        "expected_steps": 7,
        "derivation_sketch": [
            "A, A→B ⊢ B (MP)",
            "B, B→(C∧D) ⊢ C∧D (MP)",
            "C∧D ⊢ C (Simp)",
            "C∧D ⊢ D (Simp)",
            "C, C→E ⊢ E (MP)",
            "D, D→F ⊢ F (MP)",
            "E, F ⊢ E∧F (Conj); E∧F, (E∧F)→G ⊢ G (MP)",
        ],
    },
]

# -------------------------------------------------------------------
# INVALID PROBLEMS (target does not follow from premises)
# -------------------------------------------------------------------

invalid_problems = [
    {
        "id": "I01",
        "name": "Affirming the consequent",
        "premises": [Implies(A, B), B],
        "target": A,
        "fallacy": "affirming_the_consequent",
        "expected_counterexample_hint": "A=False, B=True",
    },
    {
        "id": "I02",
        "name": "Denying the antecedent",
        "premises": [Implies(P, Q), Not(P)],
        "target": Not(Q),
        "fallacy": "denying_the_antecedent",
        "expected_counterexample_hint": "P=False, Q=True",
    },
    {
        "id": "I03",
        "name": "Disjunction without elimination support",
        "premises": [Or(A, B), Implies(A, C)],
        "target": C,
        "fallacy": "missing_disjunctive_elimination",
        "expected_counterexample_hint": "A=False, B=True, C=False",
    },
    {
        "id": "I04",
        "name": "Necessary-vs-sufficient confusion",
        "premises": [Implies(And(P, Q), R), R, Not(Q)],
        "target": P,
        "fallacy": "necessary_vs_sufficient",
        "expected_counterexample_hint": "R via independent source; P=False, Q=False",
    },
    {
        "id": "I05",
        "name": "Conjunction antecedent partially affirmed",
        "premises": [Implies(And(A, B), C), A, Implies(Not(B), D)],
        "target": C,
        "fallacy": "partial_antecedent_affirmation",
        "expected_counterexample_hint": "A=True, B=False, C=False, D=True",
    },
    {
        "id": "I06",
        "name": "Vacuous-implication trap",
        "premises": [Or(P, Q), Implies(Not(P), R), Implies(R, S)],
        "target": S,
        "fallacy": "vacuous_implication",
        "expected_counterexample_hint": "P=True, Q=False, R=False, S=False",
    },
    {
        "id": "I07",
        "name": "Broken hypothetical chain",
        "premises": [Implies(A, B), Implies(C, D), A],
        "target": D,
        "fallacy": "missing_link",
        "expected_counterexample_hint": "A=True, B=True, C=False, D=False",
    },
    {
        "id": "I08",
        "name": "Implication conjunction without antecedent reach",
        "premises": [And(Implies(P, Q), Implies(R, S)), P],
        "target": S,
        "fallacy": "irrelevant_conjunct_application",
        "expected_counterexample_hint": "P=True, Q=True, R=False, S=False",
    },
    {
        "id": "I09",
        "name": "Independent conditional jump",
        "premises": [Or(A, B), Implies(A, C), Implies(B, D)],
        "target": And(C, D),
        "fallacy": "unsupported_conjunction",
        "expected_counterexample_hint": "A=True, B=False, C=True, D=False",
    },
    {
        "id": "I10",
        "name": "Negation conversion error",
        "premises": [Implies(A, Not(B)), Implies(B, C), C],
        "target": Not(A),
        "fallacy": "negation_conversion",
        "expected_counterexample_hint": "A=True, B=False, C=True",
    },
]


# -------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------

def validate_problem(problem: dict, expected_validity: bool) -> dict:
    premises = And(*problem["premises"])
    target = problem["target"]
    test_formula = And(premises, Not(target))
    result = satisfiable(test_formula)
    actual_valid = (result is False)
    record = {
        "id": problem["id"],
        "name": problem["name"],
        "expected_validity": expected_validity,
        "actual_validity": actual_valid,
        "ground_truth_match": actual_valid == expected_validity,
        "counterexample": (None if actual_valid
                           else {str(k): bool(v) for k, v in result.items()}),
    }
    return record


def main():
    out_dir = Path("v7_5_problems")
    out_dir.mkdir(exist_ok=True)

    all_records = []
    print("=" * 70)
    print("VALID PROBLEMS (expected: target follows)")
    print("=" * 70)
    for p in valid_problems:
        rec = validate_problem(p, expected_validity=True)
        status = "OK" if rec["ground_truth_match"] else "MISMATCH"
        print(f"  {rec['id']} {rec['name']:55s}  [{status}]")
        if not rec["ground_truth_match"]:
            print(f"      ACTUAL: {rec['actual_validity']}; counterexample: {rec['counterexample']}")
        all_records.append({**rec,
                            "premises_str": [str(x) for x in p["premises"]],
                            "target_str": str(p["target"]),
                            "rules_used": p.get("rules_used"),
                            "expected_steps": p.get("expected_steps"),
                            "derivation_sketch": p.get("derivation_sketch")})

    print()
    print("=" * 70)
    print("INVALID PROBLEMS (expected: target does not follow)")
    print("=" * 70)
    for p in invalid_problems:
        rec = validate_problem(p, expected_validity=False)
        status = "OK" if rec["ground_truth_match"] else "MISMATCH"
        print(f"  {rec['id']} {rec['name']:55s}  [{status}]")
        if not rec["ground_truth_match"]:
            print(f"      ACTUAL: {rec['actual_validity']}")
        all_records.append({**rec,
                            "premises_str": [str(x) for x in p["premises"]],
                            "target_str": str(p["target"]),
                            "fallacy": p.get("fallacy"),
                            "expected_counterexample_hint": p.get("expected_counterexample_hint")})

    # Export JSON
    out_path = out_dir / "v7_5_problem_set.json"
    out_path.write_text(json.dumps(all_records, indent=2), encoding="utf-8")
    print(f"\nWrote: {out_path}")

    # Summary
    n_valid_ok = sum(1 for r in all_records if r["expected_validity"] and r["ground_truth_match"])
    n_invalid_ok = sum(1 for r in all_records if not r["expected_validity"] and r["ground_truth_match"])
    print(f"\nValidation: {n_valid_ok}/10 valid problems confirmed, {n_invalid_ok}/10 invalid problems confirmed.")
    if n_valid_ok == 10 and n_invalid_ok == 10:
        print("ALL PROBLEMS VALIDATED.")
        return 0
    else:
        print("VALIDATION FAILED. Fix problems before deployment.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
