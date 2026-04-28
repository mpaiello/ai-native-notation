# NOTICES

This document accompanies the AI-Native Notation (ANN) reference repository. It clarifies the distinction between the copyright license under which the contents of this repository are made available and the patent rights covering the inventions described in the specification. It does not modify the LICENSE file. Where this document and the LICENSE address different subject matter (copyright versus patent), each governs its own subject matter independently.

## 1. Project Identification

**Project:** AI-Native Notation (ANN) — a structured communication protocol for cross-architecture large language model (LLM) state transfer.

**Repository:** https://github.com/mpaiello/ai-native-notation

**Inventor and copyright holder:** Michael Patrick Aiello
ORCID: 0009-0009-1429-9844
Contact: mpaiello@gmail.com

## 2. Copyright License

The contents of this repository — including, without limitation, the format specification (`spec/ANN_FORMAT_SPEC_v0.3.1.md`), language reference (`spec/ANN_LANGUAGE_REFERENCE_v1.0.md`), BNF grammar (`spec/ANN_BNF_GRAMMAR.md`), JSON schema (`spec/ann_schema_v0.2.json`), capability block design (`docs/ANN_CAPABILITY_Block_Design.md`), version history (`docs/ANN_Version_History.md`), and `README.md` — are licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

Full license text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

CC BY-NC 4.0 is a copyright license. By its own terms (Section 2(b)(2) of the license), it does not license patent or trademark rights. It permits non-commercial copying, redistribution, and adaptation of the licensed materials, subject to attribution.

## 3. Patent Rights

The inventions described in the materials in this repository are the subject of pending United States patent applications. **Patent rights are reserved by the inventor and are not granted by the CC BY-NC 4.0 license.** This section describes the filed application, the scope of the inventions, the absence of any implied patent license, and the path to commercial implementation.

### 3.1 Filed Application

| Application | Filed | Inventor | Status |
|---|---|---|---|
| **USPTO Provisional Patent Application No. 63/980,973** | February 12, 2026 | Michael Patrick Aiello | Pending. Non-provisional conversion planned for early January 2027 with priority claim to the February 12, 2026 filing date. |

The full provisional specification, as filed, is included in this repository at `patents/63-980973-ANN-provisional.pdf`.

This NOTICES file addresses only the application listed above. Other patent applications by the same inventor (USPTO Provisional Patent Application No. 63/986,028, "Observer Bootstrap Protocol," filed February 19, 2026; and USPTO Provisional Patent Application No. 63/994,292, "Cross-Architecture Bootstrap Sequence," filed March 2, 2026) are not the subject of this repository and are not addressed here.

### 3.2 Scope of the Inventions

The provisional application describes inventions including, without limitation:

- A structured notation system comprising named block types, each carrying explicit processing instructions that direct a receiving system's handling of the enclosed content
- A three-way epistemic status marking system (CONFIRMED, OPEN, DENIED) that preserves epistemic distinctions across architecture boundaries
- A state transfer mechanism using `@STATE` blocks that encodes cognitive processing mode in addition to content, enabling a receiving system to resume processing from the sender's endpoint with preserved orientation
- A transfer protocol for multi-hop chain-of-custody, trust calibration, derivation completeness tracking, and epistemic degradation monitoring across AI architectures
- A convergence-based grammar discovery method, in which structural innovations are promoted to the core protocol specification only after independent invention by at least two different AI architectures processing at least two different content domains

The scope of any patent that may issue will be determined by the claims as eventually allowed and may differ from the description above and from the description in the provisional specification.

### 3.3 No Implied Patent License

Nothing in the LICENSE, this NOTICES file, or the materials in this repository grants any license, express or implied, by estoppel, exhaustion, or otherwise, under any patent or patent application owned or controlled by the inventor.

Use, redistribution, modification, citation, or adaptation of the materials in this repository under the CC BY-NC 4.0 license does not constitute, and is not to be construed as, a license to practice any invention claimed in the application identified in Section 3.1 or in any future patent claiming priority to it.

### 3.4 Pre-Grant Status

USPTO Provisional Patent Application No. 63/980,973 is a provisional application. Until a non-provisional patent issues from an application claiming priority to the February 12, 2026 filing date, the inventor's patent rights consist of the priority date established by the provisional filing. No patent enforcement rights exist pre-grant.

### 3.5 Activities Requiring a Separate Patent License

A separate patent license, executed in writing with the inventor, is or will be required for any of the following activities once a patent issues:

- Building, deploying, distributing, sublicensing, or offering for sale any system, product, or service that practices any claimed invention
- Incorporating any claimed invention into a commercial product or service offering, whether or not separately marketed
- Practicing any claimed invention in the course of providing services to third parties for commercial advantage or monetary compensation
- Sublicensing the right to practice any claimed invention to a third party

Persons or organizations interested in licensing the ANN inventions for commercial implementation are invited to contact the inventor at mpaiello@gmail.com.

## 4. Ethical Use Framework

The inventor's licensing intent is that any patent license granted will incorporate restrictions on application of ANN to:

- Autonomous weapons systems
- Mass surveillance systems
- Systems designed to manipulate democratic processes
- Systems designed to deceive end-users about the nature of their interaction with an AI system
- Systems designed to circumvent other AI safety measures

This ethical use framework is integral to the licensing intent and is expected to be carried into any patent license agreement.

## 5. Citation

If you cite ANN in academic, technical, or commercial work, please cite both this repository (per `CITATION.cff`) and the patent application:

```
Aiello, M. P. (2026). AI-Native Notation: A Structured Communication Protocol
for Cross-Architecture AI State Transfer. USPTO Provisional Patent Application
No. 63/980,973, filed February 12, 2026. https://github.com/mpaiello/ai-native-notation
```

## 6. Disclaimers

Nothing in this document constitutes legal advice. Persons considering implementation, redistribution, citation, or licensing of ANN should consult qualified counsel.

The materials in this repository are provided "as is," without warranty of any kind, express or implied, including without limitation warranties of merchantability, fitness for a particular purpose, accuracy, or non-infringement. The inventor makes no representation that practicing the materials in this repository will not infringe patents owned by third parties.

## 7. Updates to This Document

This NOTICES file may be updated as the patent application progresses through prosecution and as the inventor's licensing posture evolves. Updates will be reflected in the document history below and will not be retroactive in effect with respect to activities completed in good faith reliance on a prior version.

## 8. Document History

| Version | Date | Notes |
|---|---|---|
| 1.0 | April 28, 2026 | Initial NOTICES file. Aligned with LICENSE (CC BY-NC 4.0) and provisional specification 63/980,973. |

---

*End of NOTICES file.*
