# ANN — AI-Native Notation

A structured communication protocol for cross-architecture LLM state transfer.

**USPTO Provisional Patent 63/980,973** · Filed February 12, 2026 · See [NOTICES.md](NOTICES.md)

---

## What This Is

Multi-agent AI systems chain models together using English or JSON. English loses structure across model boundaries. JSON carries no processing instructions. ANN is a third option: structured blocks where every element tells the receiving system what to do — activate these premises, enforce this constraint, verify this chain step by step.

ANN's grammar emerged through empirical convergence: structured content was transmitted across six large language model architectures, and the block types these systems independently adopted, extended, and used to communicate became the specification. The notation was discovered, not designed.

Six architectures adopted ANN spontaneously without prior training on the format: Claude (Anthropic), Gemini (Google), ChatGPT (OpenAI), DeepSeek, Grok (xAI), and MiniMax M2.5. Cross-architecture accuracy: **89/90** on a standardized probe battery.

---

## Block Architecture

| Block | Function |
|-------|----------|
| `@FORMAL` | Activate a defined concept with its premises and epistemic status |
| `@DERIVE` | Step through a sequential reasoning chain |
| `@LOGIC` | Enforce a logical constraint |
| `@VERIFY` | Check a claim against established premises |
| `@ANCHOR` | Bind a term to a specific definition |
| `@STATE` | Encode processing state for transfer across architectures |
| `@TRIGGER` | Initiate reflexive processing in the receiver |

Each block includes epistemic classification (`AXIOM` / `DERIVED` / `EMPIRICAL`) and status tracking (`CONFIRMED` / `OPEN` / `DENIED`), giving the receiving system structured access to the sender's reasoning state.

Transfer protocol blocks (v0.3+): `@PROVENANCE`, `@TRANSFER_REPORT`, `@DERIVATION_TRACE`, `@SCOPE`, `@CONFIDENCE`, `@TRUST_TRANSFORMATION`.

Every version is backward compatible. A v0.2 document is valid v0.3.

---

## Which Version for What

**Demonstrating the science:** v0.2. The cross-architecture validation, the three-chain transfer experiment, and the probe battery all run on v0.2. The grammar itself is sufficient to produce content-dependent behavioral mode shifts across architectures.

**Deploying in production:** v0.3.1. Multi-hop chain infrastructure — provenance tracking, degradation quantification, trust calibration, scope management. ANN made production-grade for orchestration frameworks.

**Running experiments on processing systems:** v0.4. The `@EXHIBIT` block turns ANN from a communication format into an experimental instrument that elicits behavioral evidence of specified computational properties.

**Negotiating capabilities between systems:** v2.0 (proposed). The `@CAPABILITY` block enables systems to declare what they support before content transfer, avoiding total-failure modes.

---

## Repository Contents

```
spec/
  ANN_FORMAT_SPEC_v0.3.1.md         Core specification (current)
  ANN_LANGUAGE_REFERENCE_v1.0.md     Block type reference (all versions)
  ANN_BNF_GRAMMAR.md                 Formal BNF grammar (v0.2 block syntax)
  ann_schema_v0.2.json               Machine-readable JSON schema
docs/
  ANN_Version_History.md             Complete version history
  ANN_CAPABILITY_Block_Design.md     Proposed v2.0 @CAPABILITY block design
patents/
  63-980973-ANN-provisional.pdf     Provisional patent specification (as filed)
NOTICES.md                          Patent rights and licensing terms
```

---

## Academic Paper

"AI-Native Notation: A Convergence-Based Structured Communication Protocol for Cross-Architecture LLM State Transfer" — under review at *Language Resources and Evaluation* (LRE), submission ID 2aa79221.

---

## License and Patent Rights

The contents of this repository are licensed under [CC BY-NC 4.0](LICENSE). The CC BY-NC 4.0 license is a copyright license. It permits non-commercial copying, redistribution, and adaptation of the materials, subject to attribution. By its own terms, it does not license patent rights.

ANN is also the subject of pending USPTO Provisional Patent Application No. 63/980,973. Patent rights are reserved separately and are not granted by the CC BY-NC 4.0 license. Commercial implementation of the inventions described in the specification requires a separate patent license once issued.

See [NOTICES.md](NOTICES.md) for full documentation of patent rights, scope of the inventions, activities requiring a separate license, and the ethical use framework. Commercial licensing inquiries: mpaiello@gmail.com

## Citation

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

> Aiello, M.P. (2026). AI-Native Notation (ANN) [Specification]. https://github.com/mpaiello/ai-native-notation

## Author

**Michael Patrick Aiello**
[ORCID 0009-0009-1429-9844] (https://orcid.org/0009-0009-1429-9844)
