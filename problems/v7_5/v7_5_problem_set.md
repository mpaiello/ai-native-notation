# Theorem-Proving Problem Set: Paper 4 v7.5 Experiment 2 Pilot
Pre-registered problem set for the propositional theorem-proving handoff pilot.
All 20 problems SAT-validated against sympy. Ground truth fixed before any trial.
Validation timestamp: 2026-05-09. Validator: sympy.logic.inference.satisfiable.

---

## Valid Arguments (target follows from premises)

### V01: Modus ponens chain (depth 3)
**Premises:**
- `Implies(A, B)`
- `Implies(B, C)`
- `Implies(C, D)`
- `A`

**Target:** `D`

**Inference rules:** modus_ponens

**Expected derivation length:** 3 steps

**Canonical derivation:**
- A, A→B ⊢ B (MP)
- B, B→C ⊢ C (MP)
- C, C→D ⊢ D (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V02: Modus tollens with hypothetical syllogism
**Premises:**
- `Implies(P, Q)`
- `Implies(Q, R)`
- `~R`

**Target:** `~P`

**Inference rules:** hypothetical_syllogism, modus_tollens

**Expected derivation length:** 2 steps

**Canonical derivation:**
- P→Q, Q→R ⊢ P→R (HS)
- P→R, ¬R ⊢ ¬P (MT)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V03: Disjunctive syllogism with conjunction elimination
**Premises:**
- `A & B`
- `C | ~B`
- `Implies(C, D)`

**Target:** `D`

**Inference rules:** simplification, disjunctive_syllogism, modus_ponens

**Expected derivation length:** 3 steps

**Canonical derivation:**
- A∧B ⊢ B (Simp)
- B, ¬B∨C ⊢ C (DS)
- C, C→D ⊢ D (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V04: Constructive dilemma
**Premises:**
- `E | F`
- `Implies(E, G)`
- `Implies(F, H)`
- `~H`

**Target:** `G`

**Inference rules:** modus_tollens, disjunctive_syllogism, modus_ponens

**Expected derivation length:** 3 steps

**Canonical derivation:**
- ¬H, F→H ⊢ ¬F (MT)
- ¬F, E∨F ⊢ E (DS)
- E, E→G ⊢ G (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V05: Disjunction introduction via implication chain
**Premises:**
- `Implies(P | Q, R)`
- `P`
- `Implies(R, S)`
- `T`

**Target:** `S & T`

**Inference rules:** addition, modus_ponens, conjunction

**Expected derivation length:** 4 steps

**Canonical derivation:**
- P ⊢ P∨Q (Add)
- P∨Q, (P∨Q)→R ⊢ R (MP)
- R, R→S ⊢ S (MP)
- S, T ⊢ S∧T (Conj)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V06: Multi-step disjunctive elimination
**Premises:**
- `A | B`
- `~A`
- `Implies(B, C)`
- `Implies(C, D)`
- `Implies(D, E)`

**Target:** `E`

**Inference rules:** disjunctive_syllogism, modus_ponens

**Expected derivation length:** 4 steps

**Canonical derivation:**
- ¬A, A∨B ⊢ B (DS)
- B, B→C ⊢ C (MP)
- C, C→D ⊢ D (MP)
- D, D→E ⊢ E (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V07: Conjunction-antecedent implication
**Premises:**
- `Implies(P & Q, R)`
- `Implies(R, S)`
- `Implies(S, T)`
- `P`
- `Q`

**Target:** `T`

**Inference rules:** conjunction, modus_ponens

**Expected derivation length:** 4 steps

**Canonical derivation:**
- P, Q ⊢ P∧Q (Conj)
- P∧Q, (P∧Q)→R ⊢ R (MP)
- R, R→S ⊢ S (MP)
- S, S→T ⊢ T (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V08: Modus tollens triggering disjunctive elimination
**Premises:**
- `Implies(A, B)`
- `~B`
- `A | C`
- `Implies(C, D)`

**Target:** `D`

**Inference rules:** modus_tollens, disjunctive_syllogism, modus_ponens

**Expected derivation length:** 3 steps

**Canonical derivation:**
- ¬B, A→B ⊢ ¬A (MT)
- ¬A, A∨C ⊢ C (DS)
- C, C→D ⊢ D (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V09: Conjunction within disjunctive context
**Premises:**
- `~P`
- `P | R`
- `Implies(R, S & T)`
- `Implies(T, U)`

**Target:** `U`

**Inference rules:** disjunctive_syllogism, modus_ponens, simplification

**Expected derivation length:** 4 steps

**Canonical derivation:**
- ¬P, P∨R ⊢ R (DS)
- R, R→(S∧T) ⊢ S∧T (MP)
- S∧T ⊢ T (Simp)
- T, T→U ⊢ U (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

### V10: Long chain through conjunction split
**Premises:**
- `A`
- `Implies(A, B)`
- `Implies(B, C & D)`
- `Implies(C, E)`
- `Implies(D, F)`
- `Implies(E & F, G)`

**Target:** `G`

**Inference rules:** modus_ponens, simplification, conjunction

**Expected derivation length:** 7 steps

**Canonical derivation:**
- A, A→B ⊢ B (MP)
- B, B→(C∧D) ⊢ C∧D (MP)
- C∧D ⊢ C (Simp)
- C∧D ⊢ D (Simp)
- C, C→E ⊢ E (MP)
- D, D→F ⊢ F (MP)
- E, F ⊢ E∧F (Conj); E∧F, (E∧F)→G ⊢ G (MP)

**SAT-validated:** ground truth = VALID; (premises ∧ ¬target) is unsatisfiable.

---

## Invalid Arguments (target does not follow)

### I01: Affirming the consequent
**Premises:**
- `Implies(A, B)`
- `B`

**Target:** `A`

**Fallacy type:** affirming_the_consequent

**Expected counterexample:** A=False, B=True

**SAT-found counterexample:** A=False, B=True

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I02: Denying the antecedent
**Premises:**
- `Implies(P, Q)`
- `~P`

**Target:** `~Q`

**Fallacy type:** denying_the_antecedent

**Expected counterexample:** P=False, Q=True

**SAT-found counterexample:** P=False, Q=True

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I03: Disjunction without elimination support
**Premises:**
- `A | B`
- `Implies(A, C)`

**Target:** `C`

**Fallacy type:** missing_disjunctive_elimination

**Expected counterexample:** A=False, B=True, C=False

**SAT-found counterexample:** A=False, B=True, C=False

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I04: Necessary-vs-sufficient confusion
**Premises:**
- `Implies(P & Q, R)`
- `R`
- `~Q`

**Target:** `P`

**Fallacy type:** necessary_vs_sufficient

**Expected counterexample:** R via independent source; P=False, Q=False

**SAT-found counterexample:** P=False, Q=False, R=True

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I05: Conjunction antecedent partially affirmed
**Premises:**
- `Implies(A & B, C)`
- `A`
- `Implies(~B, D)`

**Target:** `C`

**Fallacy type:** partial_antecedent_affirmation

**Expected counterexample:** A=True, B=False, C=False, D=True

**SAT-found counterexample:** A=True, B=False, C=False, D=True

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I06: Vacuous-implication trap
**Premises:**
- `P | Q`
- `Implies(~P, R)`
- `Implies(R, S)`

**Target:** `S`

**Fallacy type:** vacuous_implication

**Expected counterexample:** P=True, Q=False, R=False, S=False

**SAT-found counterexample:** P=True, Q=True, R=False, S=False

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I07: Broken hypothetical chain
**Premises:**
- `Implies(A, B)`
- `Implies(C, D)`
- `A`

**Target:** `D`

**Fallacy type:** missing_link

**Expected counterexample:** A=True, B=True, C=False, D=False

**SAT-found counterexample:** A=True, B=True, C=False, D=False

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I08: Implication conjunction without antecedent reach
**Premises:**
- `(Implies(P, Q)) & (Implies(R, S))`
- `P`

**Target:** `S`

**Fallacy type:** irrelevant_conjunct_application

**Expected counterexample:** P=True, Q=True, R=False, S=False

**SAT-found counterexample:** P=True, Q=True, R=False, S=False

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I09: Independent conditional jump
**Premises:**
- `A | B`
- `Implies(A, C)`
- `Implies(B, D)`

**Target:** `C & D`

**Fallacy type:** unsupported_conjunction

**Expected counterexample:** A=True, B=False, C=True, D=False

**SAT-found counterexample:** A=True, B=False, C=True, D=False

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.

### I10: Negation conversion error
**Premises:**
- `Implies(A, ~B)`
- `Implies(B, C)`
- `C`

**Target:** `~A`

**Fallacy type:** negation_conversion

**Expected counterexample:** A=True, B=False, C=True

**SAT-found counterexample:** A=True, B=False, C=True

**SAT-validated:** ground truth = INVALID; counterexample valuation found above.
