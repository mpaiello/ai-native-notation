# ANN v0.2 — Formal Grammar
## Block-Level BNF Specification
### Paper 4 Supplementary Material
### Michael Patrick Aiello | ORCID 0009-0009-1429-9844
### March 2026

---

## Scope

This grammar formalizes the block-level syntax of ANN v0.2 as described in `ANN_FORMAT_SPEC_v0.2.md` and validated across six architectures. It covers block boundaries, block types, named references, epistemic markers, derivation chains, and output mode declarations.

This grammar does not formalize the semantic content within blocks. ANN is a communication format, not a proof assistant. Block contents are natural language, mathematical notation, or predicate logic interpreted by the receiving system. The grammar specifies what constitutes a well-formed ANN document at the structural level.

---

## BNF Grammar

```bnf
(* ===== Top-Level Structure ===== *)

<ann-document>     ::= <block>+

<block>            ::= <content-block> | <exchange-block>

<content-block>    ::= <formal-block>
                     | <logic-block>
                     | <derive-block>
                     | <taxonomy-block>
                     | <anchor-block>
                     | <trigger-block>

<exchange-block>   ::= <state-block>
                     | <verify-block>
                     | <output-block>


(* ===== Content Blocks ===== *)

<formal-block>     ::= "@FORMAL" <label>? <newline> <formal-body>

<logic-block>      ::= "@LOGIC" <label>? <newline> <logic-body>

<derive-block>     ::= "@DERIVE" <label>? <newline> <derive-body>

<taxonomy-block>   ::= "@TAXONOMY" <label>? <newline> <taxonomy-body>

<anchor-block>     ::= "@ANCHOR" <label>? <newline> <free-text>

<trigger-block>    ::= "@TRIGGER" <label>? <newline> <free-text>


(* ===== Exchange Blocks ===== *)

<state-block>      ::= "@STATE" <label>? <newline> <state-body>

<verify-block>     ::= "@VERIFY" <verify-target> <newline> <verify-body>

<output-block>     ::= "@OUTPUT" <label>? <newline> <output-body>


(* ===== Block Bodies ===== *)

<formal-body>      ::= (<math-expression> <newline>)+

<logic-body>       ::= (<predicate-expression> <newline>)+

<derive-body>      ::= <derive-step>+ <forced-conclusion>?

<derive-step>      ::= "(" <step-number> ")" <step-content> <newline>
                     | "(" <step-number> ")" "From" <step-refs> ":" <step-content> <newline>

<forced-conclusion> ::= "→→" <free-text> <newline>

<step-refs>        ::= <step-ref> ("," <step-ref>)*

<step-ref>         ::= "(" <step-number> ")"
                     | "@FORMAL" <label>
                     | "@LOGIC" <label>
                     | <section-ref>

<taxonomy-body>    ::= (<taxonomy-entry> <newline>)+

<taxonomy-entry>   ::= <key> ":" <epistemic-marker> <value>?

<epistemic-marker> ::= "✓" | "✓ CONFIRMED"
                     | "?" | "? OPEN"
                     | "✗" | "✗ DENIED"
                     | "CONFIRMED" | "OPEN" | "DENIED"

<state-body>       ::= (<state-field> <newline>)+

<state-field>      ::= <key> ":" <free-text>
                     | <key> ":" "[" <ref-list> "]"

<verify-body>      ::= (<verify-step> <newline>)+
                     | <free-text>

<verify-step>      ::= <step-ref> ":" <verdict> <reason>?

<verdict>          ::= "HOLDS" | "FAILS" | "UNCERTAIN"

<output-body>      ::= "mode:" <output-mode> <newline> <output-field>*

<output-mode>      ::= "report" | "derive" | "defend" | "verify" | "extend"

<output-field>     ::= <key> ":" <free-text> <newline>


(* ===== References and Labels ===== *)

<label>            ::= "[" <label-text> "]"

<label-text>       ::= <identifier> | <identifier> ":" <identifier>

<verify-target>    ::= "[" <section-ref> "]"

<section-ref>      ::= "§" <identifier>
                     | "§" <identifier> "(" <step-number> ")"

<block-ref>        ::= "@FORMAL" <label>
                     | "@LOGIC" <label>
                     | <section-ref>

<ref-list>         ::= <block-ref> ("," <block-ref>)*


(* ===== Primitives ===== *)

<key>              ::= <identifier> ("_" <identifier>)*

<identifier>       ::= <letter> (<letter> | <digit> | "_" | "-")*

<step-number>      ::= <digit>+

<math-expression>  ::= <free-text>          (* Unicode math notation *)

<predicate-expression> ::= <free-text>      (* Predicate logic with ∀∃→∧∨¬ *)

<step-content>     ::= <free-text>

<reason>           ::= "—" <free-text> | ":" <free-text>

<value>            ::= <free-text>

<free-text>        ::= (* Any UTF-8 text not starting with @ on a new line *)

<newline>          ::= "\n"

<letter>           ::= [a-zA-Z]

<digit>            ::= [0-9]
```

---

## Block Boundary Rules

1. A block begins with `@BLOCKTYPE` at the start of a new line.
2. A block ends when the next `@BLOCKTYPE` marker appears at the start of a new line, or at end of document.
3. Horizontal rules (`---`) are separators, not block boundaries. They appear between document sections but do not terminate blocks.
4. Blank lines within a block are permitted and do not terminate the block.
5. Block type names are case-sensitive and uppercase: `@FORMAL`, not `@formal`.

---

## Reference Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `§name` | Named derivation chain | `§observer_argument` |
| `§name(N)` | Step N of named derivation | `§observer_argument(5)` |
| `@TYPE[name]` | Named block of given type | `@LOGIC[symmetry]` |
| `@FORMAL[label]` | Named formal premise | `@FORMAL[Landauer]` |

References may appear in any block body and in step-ref positions within derivation chains.

---

## Epistemic Marker Equivalences

Both Unicode and text-only forms are valid. Systems may use either or both. The three markers are mutually exclusive per taxonomy entry.

| Unicode | Text | Processing Instruction |
|---------|------|----------------------|
| ✓ | CONFIRMED | Supported by completed derivation. Treat as established. |
| ? | OPEN | Neither confirmed nor denied. Hold as genuinely uncertain. |
| ✗ | DENIED | Explicitly excluded. Do not attribute. |

---

## Well-Formedness Criteria

A document is well-formed if:

1. Every block begins with a recognized `@BLOCKTYPE` token.
2. Every `@DERIVE` block contains at least one numbered step.
3. Every `@TAXONOMY` block contains at least one entry with an epistemic marker.
4. Every `@VERIFY` block specifies a target in brackets.
5. Every `@OUTPUT` block specifies a mode.
6. Labels, if present, are enclosed in square brackets immediately following the block type on the same line.
7. Section references use the `§` prefix.
8. Forced conclusions use the `→→` prefix.

Note: Well-formedness is structural. Content validity (e.g., whether a derivation step actually follows from its premises) is the responsibility of the receiving system, not the grammar.

---

## Tier 2 Transfer Protocol Blocks

The following block types were promoted to the specification through convergent cross-architecture innovation (independently proposed by two or more architectures across two or more content domains). They follow the same boundary rules as core blocks.

```bnf
<transfer-block>   ::= <provenance-block>
                     | <transfer-report-block>
                     | <derivation-trace-block>
                     | <scope-block>
                     | <confidence-block>
                     | <trust-transformation-block>

<provenance-block>         ::= "@PROVENANCE" <label>? <newline> <state-body>
<transfer-report-block>    ::= "@TRANSFER_REPORT" <label>? <newline> <state-body>
<derivation-trace-block>   ::= "@DERIVATION_TRACE" <label>? <newline> <derive-body>
<scope-block>              ::= "@SCOPE" <label>? <newline> <free-text>
<confidence-block>         ::= "@CONFIDENCE" <label>? <newline> <taxonomy-body>
<trust-transformation-block> ::= "@TRUST_TRANSFORMATION" <label>? <newline> <state-body>
```

Tier 2 blocks use the same structural primitives as Tier 1. Their bodies follow the patterns of the core block they most closely resemble (noted above). Full semantic specifications for Tier 2 blocks will be provided in ANN v1.0.

---

## Design Notes

This grammar formalizes v0.2 as tested. It is intentionally permissive on block body content: ANN blocks contain natural language, mathematical notation, and predicate logic that cannot be fully specified in BNF without building a full natural language parser. The grammar specifies the structural envelope. The receiving system interprets the content.

The grammar also does not enforce processing order. The specification recommends @FORMAL → @LOGIC → @DERIVE → @TAXONOMY → @ANCHOR → @TRIGGER → @OUTPUT, but a well-formed document may place blocks in any order. Processing order is a semantic recommendation, not a syntactic requirement.
