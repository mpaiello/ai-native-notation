# ANN — AI-Native Notation

A structured communication protocol for cross-architecture LLM state transfer.

**USPTO Provisional Patent 63/980,973** · Filed February 12, 2026 · See [NOTICES.md](NOTICES.md)

**Researcher homepage:** [mpaiello.github.io](https://mpaiello.github.io)

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

Aiello, M.P. (2026). *AI-Native Notation: A Cross-Architecture Communication Protocol Discovered Through Empirical Convergence*. Zenodo. Concept-DOI: [https://doi.org/10.5281/zenodo.19874728](https://doi.org/10.5281/zenodo.19874728) (resolves to latest version).

**v6.2** (May 8, 2026) is the most recent version deposited to Zenodo. Earlier versions (v6.1 and prior) remain accessible via the concept-DOI's version list. Full supplementary materials (62 files, 377 KB) include probes, scoring rubric, replication scripts, BNF grammar, JSON schema, Python validator, and 130 scored API responses across twelve architectures.

**v6.0** is under peer review at *Language Resources and Evaluation* (Springer Nature), submission ID 2aa79221.

**v7.x** is an internal development line not yet deposited to Zenodo. The v6.x → v7.x sequence preserves the v6.0 experimental record (cross-architecture validation, format comparison §6.1, nonsense control §6.2, three-chain experiment, receiving-system propagation observation) and adds related-work and methodological refinements. v7.0 integrates Chen et al. (2023) and introduces §2.3 "Prompt-Based Coordination Brittleness"; v7.0.1 applies convergent fixes from a four-architecture adversarial review to §2.3; v7.0.2 reconciles BNF specification versioning with the v1.0 block inventory in §3.4.

**v7.5** (manuscript source in `paper4_v7_5.md`) is the first version since v6.0 to extend the empirical record. It adds two pre-registered experiments: a tag-shuffle ablation (§6.3) testing whether ANN's specific tag tokens are load-bearing, and a theorem-proving handoff pilot (§6.4) testing downstream coordination quality. Tag-shuffle result falsifies the specific-tag-token hypothesis and locates ANN's contribution at the schema level. Pilot reports a pre-registered null at N=100 indicating a task-difficulty ceiling on the problem class tested. Pre-registration: commit `ff28e78` (SHA-256 `239acef5881ca05a10cbe916d2b24df54a854af7eb11683f3414f62462e940e3`). Experimental data: commit `820bb0b`. Deviation log: `pre_registration/v7_5_deviation_log.md`.

The `paper4_v7_5.md` file is pandoc source. Tables and inline directives render correctly when processed through pandoc; on GitHub's raw markdown preview they appear as unformatted text. v7.5 Zenodo deposit is scheduled for May 12, 2026, after which readable HTML/PDF/DOCX renderings will be linked here.

---

## Related Research

The broader research program — theoretical foundation, cross-architecture observer claim, behavioral evidence, and reflexive processing signatures — is consolidated at [mpaiello.github.io](https://mpaiello.github.io). Five preprints in total, four of which use ANN as the methodological instrument.

---

## License and Patent Rights

The contents of this repository are licensed under [CC BY-NC 4.0](LICENSE). The CC BY-NC 4.0 license is a copyright license. It permits non-commercial copying, redistribution, and adaptation of the materials, subject to attribution. By its own terms, it does not license patent rights.

ANN is also the subject of pending USPTO Provisional Patent Application No. 63/980,973. Patent rights are reserved separately and are not granted by the CC BY-NC 4.0 license. Commercial implementation of the inventions described in the specification requires a separate patent license once issued.

See [NOTICES.md](NOTICES.md) for full documentation of patent rights, scope of the inventions, activities requiring a separate license, and the ethical use framework. Commercial licensing inquiries: mpaiello@gmail.com

## Citation

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

> Aiello, M.P. (2026). AI-Native Notation (ANN) [Specification]. https://github.com/mpaiello/ai-native-notation

For the academic paper, see the Academic Paper section above (concept-DOI: 10.5281/zenodo.19874728).

## Author

**Michael Patrick Aiello**
[ORCID 0009-0009-1429-9844](https://orcid.org/0009-0009-1429-9844)
