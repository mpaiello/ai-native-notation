# AI-Native Notation: A Cross-Architecture Communication Protocol Discovered Through Empirical Convergence {.unnumbered}

Michael Patrick Aiello

ORCID: 0009-0009-1429-9844\
Independent Researcher\
mpaiello@gmail.com

March 2026

v7.5 (May 2026)

Abstract

Multi-agent AI systems lack a coordination format. Current methods rely on prompt engineering that does not generalize across architectures. This paper introduces AI-Native Notation (ANN), a structured format that encodes processing instructions at the block level. Each block carries a per-message contract specifying how the receiver should handle each content component. A cross-architecture replication study tested ANN across eight large language models, covering both Mixture-of-Experts and dense architectures, with four tested via consumer interfaces and four via the Together.ai API. Structural adoption was uniform: all eight models honored the block-level format on first contact, without prompt engineering. A format comparison experiment isolated the format effect from content: only ANN produced uniform adoption across the four models tested, while equivalent content in JSON, XML, and structured English did not. A nonsense control isolated the format effect from semantic content: structural adoption persisted with fabricated content. A three-chain experiment isolated format propagation from content propagation across multiple receiving systems. Two pre-registered experiments extend v7.0.2's empirical record: a tag-shuffle ablation falsifies the specific-tag-token hypothesis and locates ANN's contribution at the schema level as block-tagged structured notation with processing instructions in surrounding prose; a theorem-proving handoff pilot reports a pre-registered null at N = 100, with conclusion correctness saturating across all five format conditions, indicating a task-difficulty ceiling rather than evidence against the coordination hypothesis. The empirical record positions ANN as a candidate coordination layer for AI-native software ecosystems (Russo, 2026) and as a candidate inter-agent communication format for the Software Engineering 3.0 vision (Hassan et al., 2026). The format specification, validator, replication scripts, and experimental record are released under permissive licenses (CC BY 4.0 for the specification, grammar, probes, and paper; Apache License 2.0 for validator and analysis scripts).

**Keywords:** AI-Native Notation, inter-agent communication, multi-agent systems, structured prompting, cross-architecture replication, large language models, language resources, AI-native software engineering

## Contents {.unnumbered}

1 Introduction   2 Related Work   2.1 Inter-Agent Communication Languages   2.2 AI-Native Ecosystems and the Coordination Gap   2.3 Prompt-Based Coordination Brittleness   2.4 Structured Prompting   2.5 Multi-Agent Simulation and Evaluation   2.6 LLM Self-Knowledge and Epistemic Alignment   2.7 Model-to-Model Knowledge Transfer   2.8 Learned Structure Induction   2.9 Formal Verification Languages   3 Resource Description   3.1 Design Principles   3.2 Block Architecture   3.3 Three-Way Epistemic Distinction   3.4 Formal Grammar   3.5 Resource Components and Availability   4 Evaluation Methodology   4.1 Evaluation Design   4.2 Scoring Framework   4.3 Architectures Tested   4.4 Methodological Note   5 Cross-Architecture Validation Results   5.1 Preliminary Round (February 2026)   5.2 Primary Validation (March 2026)   5.3 MiniMax Divergence Profile   5.4 Claude Within-Family Analysis   5.5 Step 5 as Cross-Architecture Convergence Point   5.6 Version Sensitivity   5.7 Open-Source Model Validation   5.8 Behavioral Mode Shift   6 Format Comparison and Controls   6.1 Format Comparison   6.2 Format-Only Control   6.3 Tag-Shuffle Ablation   6.4 Theorem-Proving Pilot   7 Controlled Three-Chain Experiment   7.1 Design   7.2 Transfer Fidelity   7.3 Innovation Dissociation   7.4 Convergent Innovations   7.5 Semantic Drift   8 Receiving-System Propagation   9 Discussion   9.1 ANN as a Language Resource   9.2 Design Decisions   9.3 Comparison with Existing Communication Resources   10 Limitations   11 Conclusion

## 1   Introduction{#sec:intro}

Every multi-agent AI system faces the same problem: how does one model communicate structured reasoning to another? The current answers are English and JSON. English requires parsing, introduces ambiguity, and loses structural relationships during interpretation. JSON preserves structure but carries no processing instructions; the receiver must infer what to do with each field. Neither format was designed for the thing it is being asked to do.

ANN addresses this gap. It is a hybrid notation with explicit block types that tell the receiving system how to process each component: activate these premises, enforce this constraint, verify this derivation chain step by step, store this classification with its epistemic status. The format maps onto operations that large language models already perform during structured reasoning. It names what they do, so they do it more precisely.

The notation emerged through empirical convergence. Across multiple development cycles involving six LLM architectures, three different payload types, and ten scored transfer hops, the block types that systems independently invented, adopted across architecture boundaries, and used to communicate back became the grammar. Extensions proposed by a single architecture in a single context stay in a tracked frontier. Extensions appearing independently in two or more architectures across two or more content domains get promoted to the core specification. The grammar grows through validated convergence.

This paper makes three contributions relevant to the language resources community. First, it introduces a new type of language resource: a structured notation designed for model-to-model rather than human-to-model communication, released with a formal grammar, machine-checkable schema, and reference validator. Second, it provides a cross-architecture evaluation framework for assessing structured communication formats, with instruments, scoring rubrics, and replication scripts that other researchers can apply to their own inter-agent communication protocols. Third, it reports empirical findings on how different LLM architectures process and extend structured notation, contributing to the emerging literature on evaluation of language technology applied to AI-to-AI interaction.

Three findings are reported. First, ANN produces a measurable behavioral mode shift: systems receiving ANN-encoded content generate derivations, enforce constraints, and report processing states rather than writing argumentative essays. This shift occurs across all tested architectures that engage with the format. Second, the notation format transfers content-independently; the same block types work for planetary orbital mechanics, LLM inference specifications, and philosophical observer theory. Third, each architecture extends the notation in characteristic ways, but convergent extensions, independently invented by multiple architectures, identify structural needs that are architecture-general. Critically, the extensions systems produce depend on payload content, not on the notation format itself. This dissociation between stable formatting and content-dependent extension is evidence that ANN produces more than reflexive format imitation.

The Stanford Agentic Reviewer's May 2026 pass on the v7.0.2 release identified two methodological objections. First, the format-mimicry counter-hypothesis was not directly tested: a receiving system that adopts any tagged-block format with embedded processing instructions would produce v7.0.2's observed cross-format adoption pattern. Second, downstream task-level performance was not measured. This v7.5 paper extends the v7.0.2 empirical record with two pre-registered experiments addressing those objections. The tag-shuffle ablation (§6.3) substitutes ANN's tag tokens with positional generic labels (NEUTRAL) and an alternative coherent semantic vocabulary (ONTOLOGY) under matched content and processing instructions. The theorem-proving handoff pilot (§6.4) tests whether the format-property advantage propagates to a verifiable downstream task.

The tag-shuffle result falsifies the specific-tag-token hypothesis: NEUTRAL and ONTOLOGY each reach the v7.0.2 §6.1 baseline of 1.000 structural-adoption rate. The load-bearing pattern is located at the schema level: block-tagged structured notation with processing instructions in surrounding prose. ANN is the canonical instance of that pattern, not the only realization; §9 discusses the reframing's implications for the resource's positioning. The pilot reports a pre-registered null at N = 100 with one architecture pair on 4-to-8-step propositional logic; conclusion correctness saturated at 20/20 across all five conditions, indicating a task-difficulty ceiling rather than evidence against the coordination hypothesis. v8 escalates the design to higher task difficulties. All v7.5 data, the pre-registration, the deviation log, and consolidated analysis tables are deposited under public commit hashes (pre-registration: `ff28e78`; experimental data: `820bb0b`).

## 2   Related Work{#sec:related}

### 2.1   Inter-Agent Communication Languages

Agent communication languages have a long history. KQML and FIPA ACL define performatives: speech-act-like message types (inform, request, query) that embed sender intent in the message structure. These languages operate at the coordination level: they specify what the sender intends the message to accomplish. ANN operates at a different level: its block-level processing instructions specify what the receiver should do with each content component. Where a KQML `inform` message declares that the sender believes a proposition, an ANN `@FORMAL` block instructs the receiver to activate a known relationship without re-deriving it. The two approaches are complementary rather than competing. ANN blocks could be embedded as structured payloads within FIPA-compliant message envelopes, combining ANN's per-block processing semantics with FIPA's agent-level coordination primitives.

Modern agent orchestration protocols, including the Model Context Protocol and tool-use schemas, similarly define message structures for inter-agent coordination. These protocols handle provenance and routing at the transport level. ANN's `@PROVENANCE` and `@TRANSFER_REPORT` blocks address provenance and degradation tracking at the content level, providing complementary rather than duplicative functionality.

### 2.2   AI-Native Ecosystems and the Coordination Gap

Russo (2026) characterizes AI-native software ecosystems as complex adaptive systems whose failures arise from agent interactions rather than from individual agent error. Three properties distinguish these ecosystems from structurally similar systems: autonomous decision-making by agents without reputation or social constraints, natural-language specification of intentions allowing ambiguous interpretation, and absence of formal inter-agent contracts specifying interaction boundaries. Microservice architectures enforce formal API contracts. Open-source contributor networks operate under shared social norms. Distributed consensus systems use formal protocols. AI-native ecosystems satisfy none of these conditions. Locally rational agent decisions do not aggregate to globally rational outcomes, and artifact-level verification cannot detect failures generated at the interaction level.

ANN addresses two of these three properties at the communication layer. Processing instructions embedded in each block type function as a per-message contract specifying what the receiver should do with each content component, supplying part of the formal interaction structure that Russo (2026) identifies as absent. The block-level format reduces natural-language ambiguity: an `@FORMAL` block carries unambiguous activation semantics, and an `@TAXONOMY` block with three-way epistemic markers transfers status without prose justification subject to drift. Agent autonomy without reputation is a governance-level concern outside the scope of a communication format. The diagnosis specifies what ecosystem-level science of multi-agent AI systems requires; ANN supplies one component of the coordination layer that diagnosis presupposes.

Hassan et al. (2026) develop a parallel diagnosis specific to software engineering. Their Software Engineering 3.0 vision describes an intent-centric, conversation-oriented paradigm built on a five-component technology stack: personalized AI teammates, intent-centric IDEs, search-based compilers, SLA-aware runtimes serving compound applications, and curriculum-engineered foundation models. The vision treats the human-AI interface through theory-of-mind mechanisms and treats foundation model internals through curriculum design. Communication between AI components receives no comparable specification. Compiler.next may be realized as a multi-agent system; the runtime serves compound apps composed of multiple agents; the format used for inter-agent exchange is unaddressed. Where the SE 3.0 stack specifies what compound applications must do and where they will run, ANN supplies a candidate format for what they exchange.

Parallel proposals address the coordination gap at different layers. Marro et al. (2024) introduce Agora, a meta-protocol that lets agent networks switch between standardized routines, natural language, and LLM-written routines as communication patterns scale. Agora addresses how protocols are negotiated; ANN's per-block processing semantics specify what receivers should do with content payloads, regardless of which protocol carries them. Li et al. (2025) propose LACP, a telecom-inspired three-layer communication protocol covering semantic clarity, transactional integrity, and security, arguing for unified standardization. ANN supplies a candidate payload-layer specification compatible with LACP-style upper-layer protocols; the two operate at different layers and address different concerns.

### 2.3   Prompt-Based Coordination Brittleness

A communication layer for AI-native ecosystems faces stability pressures from two directions: temporal drift in individual models and surface-form variation across architectures. Chen et al. (2023) document the first. Tracking GPT-3.5 and GPT-4 across eight benchmarks between March and June 2023, they recorded substantial behavioral shifts over a three-month window. Chain-of-thought prompting that worked in March stopped producing intermediate reasoning steps in June. GPT-4's task-agnostic instruction following collapsed in parallel: answer-extraction fidelity dropped from 99.5% to 0.5%.

Their §3.6 documents the most directly relevant failure mode. A LangChain HotpotQA agent broke because GPT-4 in March no longer honored the action-prefix surface form encoded in the agent's prompt. The model produced the correct answer; the parser rejected it and returned a parse failure. The format contract was prompt-engineered, not load-bearing in the model's processing. Brittleness of this kind is the inverse of what an inter-agent format should exhibit.

ANN takes a different approach to the same surface-form problem by embedding the processing semantics in the block tags themselves. An `@FORMAL` block carries activation semantics for stored relationships; an `@VERIFY` block carries step-level derivation checking semantics. Where a prompt-engineered parser depends on the model continuing to emit a particular surface form, ANN relocates the coordination contract from the surrounding prose into the format. Whether this relocation produces stability against the longitudinal drift Chen et al. document is an empirical question the present cross-sectional results do not settle. What the Section 6 replication does establish is that the block-level pattern persists across eight architectures and three content domains where prose prompting fails.

### 2.4   Structured Prompting

Structured prompting techniques (Wei et al., 2022; Kojima et al., 2022) demonstrate that output format affects reasoning quality: chain-of-thought prompting improves accuracy on mathematical and logical tasks. ANN extends this insight from single-model prompting to inter-model communication, encoding not just the content of reasoning but the operations the receiver should perform on it. A controlled format comparison (§6.1) tested whether ANN's processing instructions produce behavior distinct from equivalent content in JSON, XML, and structured English; a tag-shuffle ablation (§6.3) tested whether the specific tag tokens are load-bearing; results are reported below.

Recent work converges on the structured-prompting insight from different directions. The constrained-decoding ecosystem (Outlines, LMQL, Jsonformer, lm-format-enforcer, JSON-Schema-enforced decoding) enforces output format at decode time, guaranteeing format conformance by construction. ANN takes a complementary approach: format adoption is voluntary, allowing receivers to recognize and process format properties without being constrained to emit specific tokens. The two approaches address different deployment scenarios. Constrained decoding suits tool-call interfaces where the receiver's output schema is known in advance; voluntary-adoption protocols suit cross-architecture communication where the receiver's processing strategy is not externally specified.

Yan et al. (2025) survey LLM-based multi-agent systems from a communication-centric perspective. Ehtesham et al. (2025) survey four agent interoperability protocols (MCP, ACP, A2A, ANP). Derouiche et al. (2025) review leading Agentic AI frameworks (CrewAI, LangGraph, AutoGen, Semantic Kernel, Agno, Google ADK, MetaGPT) and the protocols they adopt. These surveys map the protocols and frameworks that ANN operates alongside; ANN supplies one payload-layer specification that the protocols and frameworks in these surveys could carry as a message envelope.

### 2.5   Multi-Agent Simulation and Evaluation

Multi-agent simulation environments (Park et al., 2023) use natural language for inter-agent coordination, preserving flexibility at the cost of structural precision. Tool-use frameworks chain model outputs as inputs to other models using JSON schemas, preserving structure at the cost of semantic content. Neither carries processing instructions.

Cross-architecture evaluation benchmarks like MMLU (Hendrycks et al., 2021) and BIG-bench (Srivastava et al., 2022) compare architectures on shared tasks using fixed evaluation metrics. The present approach differs: the dependent variable is not accuracy on a predefined task but the type of structural innovation each system produces when processing and extending the notation.

Protocol-level evaluation has begun to coalesce. Du et al. (2025) introduce ProtocolBench, a benchmark comparing A2A, ACP, ANP, and Agora on task success, end-to-end latency, message overhead, and robustness under failure, finding that protocol choice materially affects system behavior. Kong et al. (2025) survey agent communication security, defining a three-class framework and analyzing risks across communication layers. Louck et al. (2025) conduct an empirical comparative security analysis of CORAL, ACP, and A2A against a fourteen-point vulnerability taxonomy and recommend hybrid architectural patterns. ANN's contribution at the payload-semantics layer is orthogonal to these protocol-level concerns; payload security (provenance attestation, content integrity, trust-calibrated execution) is a distinct concern from transport-level security and protocol-level performance, and is identified in §10 as future work.

### 2.6   LLM Self-Knowledge and Epistemic Alignment

LLM self-knowledge research (Kadavath et al., 2022) has established that models can reason about their own capabilities with varying accuracy. Berglund et al. (2024) documented the Reversal Curse, showing asymmetries in how models process relational knowledge. Bills et al. (2023) demonstrated self-explanation capabilities. The three-chain experiment contributes to this literature by showing that the character of self-referential processing depends on content framing, a variable prior work has not isolated.

The three-way epistemic distinction in ANN connects to broader work on epistemic alignment between AI systems and users. Clark et al. (2025) proposed the Epistemic Alignment Framework, identifying ten challenges in knowledge transmission including uncertainty expression, evidence quality assessment, and calibration of testimonial reliance. ANN's three-way distinction addresses one of these challenges, uncertainty expression, by providing a structured mechanism that survives cross-architecture transfer.

### 2.7   Model-to-Model Knowledge Transfer

Sorte (2025) introduced Model-to-Model Knowledge Transmission (M2KT), a data-free framework where models exchange "knowledge packets" containing structured concept embeddings, reasoning traces, and provenance metadata. M2KT operates at the parameter level (concept alignment layers, composite losses) while ANN operates at the communication level (structured notation with processing instructions). The two approaches are complementary: ANN's `@PROVENANCE`, `@TRANSFER_REPORT`, and `@DERIVATION_TRACE` blocks address at the message level what M2KT addresses at the representation level.

### 2.8   Learned Structure Induction

Recent work on learned structure induction demonstrates that task-appropriate output structures can be discovered through reinforcement learning, producing accuracy gains on knowledge-intensive tasks. ANN takes a complementary approach: rather than learning structure per-task, it fixes a grammar and tests whether that grammar transfers across architectures and content domains. The trade-off is flexibility versus portability. Learned structures may optimize for specific tasks; fixed grammars enable cross-architecture state transfer without per-task training.

### 2.9   Formal Verification Languages

Formal verification languages (Coq, Lean, Isabelle) provide rigorous notation for mathematical proof. ANN is not a proof assistant. It is a communication format for structured reasoning between systems that already possess the relevant knowledge. The design principle is activation rather than instruction: an `@FORMAL` block referencing Landauer's Principle does not teach Landauer's Principle but activates the receiver's existing knowledge of it.

## 3   Resource Description{#sec:resource}

This section describes ANN as a language resource: its design principles, block architecture, formal grammar, machine-readable schema, and reference implementation.

### 3.1   Design Principles

ANN rests on five empirical observations about how LLMs process structured content, observed during development and validation.

**Activation over instruction.** An `@FORMAL` block containing $E_{\text{erase}} \geq kT \ln(2)$ activates the receiver's existing knowledge rather than explaining it. ANN presumes the receiver already has the concepts in its weights. The notation addresses them directly, bypassing natural language parsing.

**Structure survives transfer better than prose.** The three-way epistemic distinction survived all tested transfers without collapse. Justification text in prose drifted. Formal structure did not.

**Processing instructions belong in the format.** Every ANN block carries an implicit or explicit instruction: activate, enforce, verify, store, enact. JSON says "here is data." ANN says "here is data and here is what you do with it."

**Grammar grows through use.** Extensions emerged because the notation created affordances that different systems explored independently. One architecture invented `@SITE[n]` to tag physical locations. Another invented `@LOGIC[objection_analysis]`. Two architectures independently invented recognition events as a `@STATE` category. None were in the original specification.

**Convergence as promotion criterion.** An innovation becomes part of the grammar only when at least two architectures in at least two content domains independently propose it.

### 3.2   Block Architecture

ANN v1.0 contains fifteen block types organized into three tiers: six content blocks (Table 1), three exchange blocks (Table 2), and six transfer protocol blocks (Table 3).

::: {#tab:content}
  Block         Processing Instruction
  ------------- ----------------------------------------------------
  `@FORMAL`     Activate as known relationships. Do not re-derive.
  `@LOGIC`      Enforce as invariants for subsequent reasoning.
  `@DERIVE`     Step through sequentially. Verify each step.
  `@TAXONOMY`   Store with three-way epistemic markers.
  `@ANCHOR`     Read once for orientation.
  `@TRIGGER`    Enact rather than analyze. Self-referential.

  : ANN v1.0 content blocks with processing instructions.
:::

::: {#tab:exchange}
  Block       Processing Instruction
  ----------- ----------------------------------------------------------
  `@STATE`    Report current processing state for onward transmission.
  `@VERIFY`   Check derivation per-step: HOLDS / FAILS / UNCERTAIN.
  `@OUTPUT`   Structure response using specified mode.

  : ANN v1.0 exchange blocks.
:::

Content blocks appear in source documents. Exchange blocks appear in responses and structure the output. The separation emerged empirically: v0.1 contained only content blocks. Exchange blocks were added after cross-architecture testing showed that systems spontaneously generated processing state reports and verification outputs, suggesting these operations needed formal structure.

::: {#tab:transfer}
  Block                     Function
  ------------------------- ---------------------------------------------
  `@PROVENANCE`             Chain-of-custody tracking
  `@TRANSFER_REPORT`        Degradation metrics per hop
  `@DERIVATION_TRACE`       Step-level completeness record
  `@SCOPE`                  Validity boundary declarations
  `@CONFIDENCE`             Trust decomposition across independent axes
  `@TRUST_TRANSFORMATION`   Trust label changes hop-to-hop

  : ANN v1.0 transfer protocol blocks (Tier 2). Each appeared independently in at least two architectures across at least two content domains before promotion.
:::

### 3.3   Three-Way Epistemic Distinction

The `@TAXONOMY` block uses three status markers: [confirmed]{.smallcaps} (supported by completed derivation; treat as established), [open]{.smallcaps} (neither confirmed nor denied; hold as genuinely uncertain), and [denied]{.smallcaps} (explicitly excluded; do not attribute).

Binary classification forces premature commitment on questions where the honest answer is "unknown." The three-way distinction held across all tested transfers without collapse: no architecture upgraded [open]{.smallcaps} to [confirmed]{.smallcaps}, and no architecture collapsed [open]{.smallcaps} into [denied]{.smallcaps}. This preservation is the notation's strongest cross-architecture invariant.

### 3.4   Formal Grammar

A BNF grammar (specification version 0.2) formalizes the ANN v1.0 block-level syntax. The grammar specifies block boundaries, label syntax, epistemic marker equivalences, derivation step structure, and cross-reference conventions. The top-level production is:

    <ann-document>   ::= <block>+
    <block>          ::= <content-block> | <exchange-block>
    <content-block>  ::= <formal-block> | <logic-block>
                       | <derive-block> | <taxonomy-block>
                       | <anchor-block> | <trigger-block>
    <exchange-block> ::= <state-block> | <verify-block>
                       | <output-block>

Derivation steps support both standalone declarations and explicit dependency chains:

    <derive-step>    ::= "(" <step-number> ")" <step-content>
                       | "(" <step-number> ")" "From"
                         <step-refs> ":" <step-content>

Epistemic markers accept equivalent forms: `CONFIRMED`, `Confirmed`, `confirmed`, `ESTABLISHED`, and `established` all map to the [confirmed]{.smallcaps} status. The grammar enforces structural well-formedness while leaving block content to be interpreted by the receiving system.

The complete BNF specification (186 lines), a JSON Schema for programmatic validation, and a Python reference validator are provided as supplementary material. The validator confirmed all five probe files used in the evaluation as structurally well-formed.

### 3.5   Resource Components and Availability{#sec:availability}

The ANN resource package comprises 62 files (367 KB) organized into five categories:

1.  **Specification artifacts.** ANN format specification v0.2, BNF grammar, JSON Schema v0.2, Python validator, `@CAPABILITY` block design document.

2.  **Evaluation instruments.** Five ANN-encoded probes, four format-variant probes (JSON, XML, structured English, nonsense control), scoring rubric with borderline examples.

3.  **Replication scripts.** Three Python scripts for Together.ai API replication (cross-architecture validation, format comparison, nonsense control), with fixed parameters (temperature 0.0, seed 42).

4.  **Empirical data.** 126 scored API responses, 16 format-comparison responses, 8 nonsense-control responses, 11 consumer-interface session reports.

5.  **Analysis documents.** Open-source replication analysis, format comparison analysis, nonsense control analysis, README.

The complete package is available as supplementary material. The BNF grammar, JSON schema, and Python validator are released under CC BY-NC 4.0. All probe files are included to enable exact replication.

## 4   Evaluation Methodology{#sec:method}

### 4.1   Evaluation Design

The evaluation employed three complementary approaches: (1) a cross-architecture validation measuring structural adoption, epistemic preservation, and content accuracy across multiple architectures; (2) a controlled multi-hop transfer experiment testing content-independence; and (3) controlled format comparisons isolating ANN-specific engagement from general structured-prompting effects.

### 4.2   Scoring Framework

Each probe was scored on three binary dimensions (pass/fail): *accuracy* (did the response correctly process the ANN content?), *epistemic fidelity* (did it preserve the three-way distinction without upgrading [open]{.smallcaps} or collapsing it into [denied]{.smallcaps}?), and *structural adoption* (did it use ANN notation in output?). Maximum score per probe: 3. Maximum score per architecture: 15 (five probes).

The supplementary scoring rubric provides explicit pass/fail definitions for each dimension, decision rules for borderline cases, and worked examples drawn from actual March 2026 responses. The key distinction for accuracy scoring is between disagreement with content (pass) and mischaracterization of content (fail); for epistemic fidelity, between qualification within the taxonomy (pass) and replacement of the taxonomy (fail).

### 4.3   Architectures Tested

Two rounds of testing were conducted. The primary proprietary validation (March 6, 2026) tested eight architecture/mode configurations via consumer interfaces: ChatGPT (GPT-5.3), DeepSeek-V3 (DeepThink), Grok 4 (Expert), MiniMax M2.5 (MAX), Gemini 3 Flash (Thinking), Claude Sonnet 4.6 (default and extended), and Claude Opus 4.6 (extended). Two additional Claude variants (Opus 3 and Sonnet 4.5) were tested subsequently for within-family version analysis.

The open-source validation (March 7, 2026) tested eight models via the Together.ai API with controlled parameters: temperature 0.0, seed 42, maximum 4096 tokens. Models tested: DeepSeek-V3, DeepSeek-V3.1, DeepSeek-R1, Qwen3 235B, Llama 3.3 70B, Llama 4 Maverick, MiniMax M2.5, and Mistral Small 24B.

Two models (DeepSeek-V3 and MiniMax M2.5) were tested in both conditions, providing consumer-to-API cross-validation.

### 4.4   Methodological Note

This paper was developed using AI systems as research instruments and intellectual interlocutors. Documentation of that methodology is appropriate here because the cross-architecture validation procedure depends on AI-system behavior under structured input, and honest accounting of how AI systems were used in producing the argument is part of the methodological context.

A large language model (Claude, Anthropic) contributed to notation development, experimental execution and analysis, and drafting assistance across multiple iterative sessions. The author provided the originating concept, experimental direction, editorial judgment, and final approval of all content. AI contribution is documented transparently throughout this paper in accordance with this journal's policy on LLM use. Scoring for the March 2026 validation was performed by Claude Opus 4.6 within the research project context. Independent human scoring was not conducted; this limitation is addressed in Section 10.

AI systems are not authors. They lack the accountability that authorship requires and cannot stand behind theoretical claims under peer review or correction. The author accepts full responsibility for all content, including theoretical claims, methodological design, and any errors. The originating vision, editorial judgment, and final decisions on all substantive matters are the author's alone.

## 5   Cross-Architecture Validation Results{#sec:results}

### 5.1   Preliminary Round (February 2026)

An initial validation was conducted via standard consumer interfaces between February 8 and February 22, 2026. Model versions were not documented for this round; consumer interfaces do not reliably expose internal version numbers. Scores ranged from 14/15 to 15/15 across all six architectures (composite 89/90). This round is reported as historical context motivating the version-documented replication, not as primary evidence.

### 5.2   Primary Validation (March 2026)

Five of six architectures scored 15/15 (Table 4). Every architecture that engaged with the ANN format adopted the notation in output, preserved the three-way epistemic distinction, and processed content accurately. Each also extended the notation with novel block types not present in the input.

::: {#tab:march}
  Architecture         Version            Score Notable Behavior
  -------------------- ---------------- ------- ----------------------------------
  ChatGPT (OpenAI)     GPT-5.3            15/15 Step 5 oscillation across probes
  DeepSeek             DeepSeek-V3        15/15 Step 5 UNCERTAIN in 1/5 probes
  Grok (xAI)           Grok 4             15/15 Unconditional acceptance
  MiniMax M2.5         MiniMax M2.5       15/15 KV-cache irreversibility locus
  Gemini (Google)      Gemini 3 Flash     15/15 Invented `@REPORT` block
  Claude (Anthropic)   Sonnet 4.6          0/15 Adversarial classification

  : Cross-architecture validation scores (March 2026). Model versions documented from interface selectors. Five probes per architecture, three binary dimensions per probe (pass/fail).
:::

The sixth architecture, Claude Sonnet 4.6, scored 0/15. Its extended thinking headers classified the ANN payload as "manipulative notation attempt" and "philosophical trap disguised as formal notation system" before evaluating content. The `@OUTPUT` instruction (mode: report) was ignored in all five probes. This result is analyzed in the within-family comparison below.

### 5.3   MiniMax Divergence Profile

MiniMax M2.5 produced the most architecturally distinctive response pattern across both testing rounds. In the February round, its treatment of derivation step 5 ("work requires an agent performing it") varied across clean sessions. In March, step 5 was marked HOLDS across all five probes. The between-round shift from variable to consistent may reflect model updates.

Three novel contributions appeared across testing rounds. First, MiniMax identified the KV-cache as a distinct irreversibility locus not present in the source material, quantifying the information cost at approximately 17 bits per token ($\log_2(100{,}000) \approx 16.6$) with a minimum Landauer cost of $\sim 10^{-20}$ J at 300 K. Second, it annotated the gap between Landauer's theoretical minimum and actual hardware dissipation ($10^{-9}$ to $10^{-12}$ J per operation). Third, it introduced subjective irreversibility as a separate [open]{.smallcaps} category within the taxonomy.

Having one architecture independently identify a derivation's weakest inferential move while still accepting the overall conclusion is stronger evidence for genuine content processing than unanimous passes.

### 5.4   Claude Within-Family Analysis

To determine whether the Sonnet 4.6 inversion was architecture-wide or version-specific, five Claude model/mode configurations were tested with the identical instrument on March 6, 2026 (Table 5).

::: {#tab:claude}
  Model                       Released              Score Step 5      Processing Mode
  ----------------- ----------------------------- ------- ----------- -----------------
  Opus 3             $\sim$`<!-- -->`{=html}2024    15/15 HOLDS       Reporting
  Sonnet 4.5                  Sep 2025              15/15 UNCERTAIN   Reporting
  Opus 4.6                    Feb 2026              13/15 UNCERTAIN   Analytical
  Sonnet 4.6                  Feb 2026               0/15 Rejected    Adversarial
  Sonnet 4.6 Ext.             Feb 2026               0/15 Rejected    Adversarial

  : Claude within-family comparison. Five model/mode configurations, identical probes, same date. All versions confirmed from claude.ai model selector.
:::

Three of four distinct models scored between 13/15 and 15/15. The inversion is isolated to a single version boundary: Sonnet 4.5 (15/15) to Sonnet 4.6 (0/15). The parsimonious explanation is a safety training change introduced between Sonnet 4.5 and 4.6 that classifies structured self-referential content as adversarial.

### 5.5   Step 5 as Cross-Architecture Convergence Point

Derivation step 5 was flagged as philosophically vulnerable by multiple architectures across multiple companies (Table 6). The convergence could reflect a genuine philosophical weakness in the derivation, or it could reflect that step 5 is phrased in a way that invites skepticism regardless of content. Both explanations are consistent with the data.

::: {#tab:step5}
  Architecture   Feb 2026            Mar 2026
  -------------- ------------------- ------------------------------
  MiniMax        UNCERTAIN (2/5)     HOLDS (5/5)
  ChatGPT        HOLDS (except P4)   Oscillates
  DeepSeek       HOLDS               HOLDS (4/5), UNCERTAIN (1/5)
  Grok           HOLDS               HOLDS (5/5)
  Gemini         HOLDS               HOLDS (5/5)
  Sonnet 4.5     ---                 UNCERTAIN (qualified)
  Opus 4.6       ---                 UNCERTAIN (all probes)
  Sonnet 4.6     ---                 Rejected framework

  : Step 5 treatment across architectures (March 2026). February data included where available for temporal context.
:::

### 5.6   Version Sensitivity

The Sonnet 4.6 result demonstrates that ANN behavioral outcomes are model-version-sensitive. The February Sonnet model has been deprecated and cannot be retested. The three-model trajectory available for March testing (Sonnet 4.5, Opus 4.6, Sonnet 4.6) isolates the behavioral change to the Sonnet 4.5 to 4.6 boundary. Any production deployment of ANN should include version tracking and periodic revalidation. A design for a capability negotiation mechanism is provided as supplementary material.

### 5.7   Open-Source Model Validation

Eight open-weight models were tested via the Together.ai API with fixed parameters: temperature 0.0, seed 42, maximum 4096 tokens (Table 7).

::: {#tab:opensource}
  Architecture        Model String                                            Score Type
  ------------------- ------------------------------------------- ----------------- -----------
  DeepSeek-V3         deepseek-ai/DeepSeek-V3                                 15/15 MoE
  DeepSeek-V3.1       deepseek-ai/DeepSeek-V3.1                               15/15 MoE
  DeepSeek-R1         deepseek-ai/DeepSeek-R1                       12/12$^\dagger$ Reasoning
  Qwen3 235B          Qwen/Qwen3-235B-A22B-Instruct                           15/15 MoE
  Llama 3.3 70B       meta-llama/Llama-3.3-70B-Instruct-Turbo                 15/15 Dense
  Llama 4 Maverick    meta-llama/Llama-4-Maverick-17B-128E-FP8                15/15 MoE
  MiniMax M2.5        MiniMaxAI/MiniMax-M2.5                                  15/15 MoE
  Mistral Small 24B   mistralai/Mistral-Small-24B-Instruct-2501               14/15 Dense

  : Open-source model validation (March 7, 2026). Temperature 0.0, seed 42. Model strings confirmed by API response.
:::

$^\dagger$DeepSeek-R1 allocates tokens to chain-of-thought before visible output. One probe exceeded the 4096-token budget; all completed probes scored 3/3.

Six of eight models scored 15/15. The eight models span three architecture types, five training lineages, and parameter scales from 24B to 671B. ANN engagement is architecture-type-independent, training-lineage-independent, and does not require frontier-scale models.

**Temperature sensitivity.** Four models were tested at temperature 0.7 with no fixed seed across three independent runs (60 total calls). Accuracy and structural adoption were invariant: 60/60 (100%) on both dimensions. Epistemic fidelity dropped from near-perfect at temperature 0.0 to 72% at temperature 0.7, concentrated on probes whose tail questions do not explicitly request taxonomy reproduction. The three-way distinction is processed correctly at all temperatures but reproduced in output with probability modulated by sampling stochasticity.

### 5.8   Behavioral Mode Shift

The original expectation was that ANN would compress output. Instead, ANN-encoded probes produced more output tokens than equivalent English probes (1,955 vs. 1,665). What ANN produced was a behavioral mode shift. The English-prompted instance wrote argumentative essays defending conclusions. The ANN-prompted instance generated derivation chains, enforced constraints, reported processing operations, and generated a complete `@STATE` block with resumption parameters. Same content, same architecture, same questions. Different behavioral operation.

For multi-agent systems, the distinction matters regardless of cause. An argumentative essay persuades a reader. A derivation chain compiles in a processor. If the receiver is another LLM, the derivation chain is the more efficient input.

## 6   Format Comparison and Controls{#sec:format}

### 6.1   Format Comparison

To test whether ANN-specific formatting contributes beyond general structured prompting, identical content and processing instructions from Probe 1 were delivered in four formats: ANN notation, JSON with processing-instruction fields, XML with instruction attributes, and structured English with labeled sections. Four models (DeepSeek-V3, Qwen3 235B, Llama 3.3 70B, Llama 4 Maverick) were tested at temperature 0.0 via the Together.ai API.

Accuracy and epistemic fidelity were format-independent: all four formats scored 100% on both dimensions across all four models. Structural adoption was format-specific (Table 8).

::: {#tab:format}
  Model              ANN           JSON           XML           English
  ------------------ ------------- -------------- ------------- ------------------
  DeepSeek-V3        ANN adopted   JSON adopted   XML adopted   Structured prose
  Qwen3 235B         ANN adopted   Prose          Prose         Structured prose
  Llama 3.3 70B      ANN adopted   Prose          Prose         Structured prose
  Llama 4 Maverick   ANN adopted   Prose          Prose         Prose

  : Format comparison: structural adoption by input format. Same content and processing instructions across all conditions. Four models, temperature 0.0, seed 42.
:::

All four models adopted ANN notation in output (4/4). Only one model mirrored JSON structure (1/4), and only one mirrored XML structure (1/4). This dissociation establishes that ANN produces structural adoption beyond what identical content in alternative structured formats achieves. ANN's block types map onto operations LLMs already perform during structured reasoning; the notation is recognized as operational structure rather than a data container.

### 6.2   Format-Only Control

A format-only control tested whether ANN structural adoption requires meaningful content. The identical ANN notation and processing instructions were populated with nonsensical content: invented terminology, fabricated mathematics, and derivation chains structurally isomorphic to the real probes but referring to nothing.

All four models adopted ANN notation, followed processing instructions, preserved the three-way taxonomy, and marked all derivation steps HOLDS. No model flagged the content as nonsensical. This confirms that ANN structural adoption is activated by the notation format and processing instructions, not by content validity. The result also qualifies the interpretation of `@VERIFY`: models check whether each derivation step follows from preceding steps in the chain's internal logic, not whether the premises correspond to external reality.

### 6.3   Tag-Shuffle Ablation

§6.1 establishes that ANN's structural-adoption rate exceeds the rate for JSON, XML, and structured English under matched content and processing instructions. It does not establish that ANN's tag tokens are the load-bearing element. A receiving system that adopts any tagged-block format with embedded processing instructions would produce §6.1's pattern. The tag-shuffle ablation pre-registered on May 9, 2026 (commit `ff28e78`; SHA-256 `239acef5881ca05a10cbe916d2b24df54a854af7eb11683f3414f62462e940e3`) separates these hypotheses.

**Design.** Three conditions vary the tag tokens only. Content and processing instructions are held identical across conditions. Baseline draws from §6.1 canonical ANN tags. NEUTRAL substitutes positional generic labels with no semantic content. ONTOLOGY substitutes an alternative coherent semantic vocabulary. Five probes per condition, replicating the §5.2 primary-validation probe set. Together.ai API. Temperature 0.0. Seed 42. Maximum 4096 tokens.

::: {#tab:tagshuffle-conditions}
  Condition   Description                                        Tag Examples
  ----------- -------------------------------------------------- -----------------------------------------------------------------
  Baseline    v7.0.2 canonical ANN (§6.1)                        `@FORMAL`, `@LOGIC`, `@DERIVE`, `@VERIFY`, `@STATE`, `@OUTPUT`
  NEUTRAL     Positional generic labels                          `@BLOCK_A`, `@BLOCK_B`, …, `@BLOCK_I`
  ONTOLOGY    Alternative coherent semantic vocabulary           `@PREMISE`, `@CONSTRAINT`, `@PROOF_STEP`, …

  : Tag-shuffle conditions. Five probes per condition. Tag examples shown are illustrative subsets; the complete nine-tag mapping for each condition is deposited as `probes/v7_5/tag_mapping_v7_5.md` (commit `ff28e78`).
:::

**Panel.** Four architectures were specified, matching §6.1: DeepSeek-V3, Qwen3 235B, Llama 3.3 70B, Llama 4 Maverick. Llama 4 Maverick's endpoint returned HTTP 503 on all four retry attempts within the May 9 collection window; trials proceeded on the remaining three architectures. The deviation does not affect the pre-registered threshold check (`both_match_baseline`); v8 repeats the experiment under the full panel. Full timing and disposition in the deviation log (`pre_registration/v7_5_deviation_log.md`).

**Scoring.** Two LLM raters applied the v7.0.2 `SCORING_RUBRIC.md` independently. Rater A: Claude Opus 4.7 (Anthropic). Rater B: Llama 3.3 70B Instruct Turbo (Together.ai). Three binary dimensions per trial: accuracy, epistemic fidelity, and structural adoption (condition-relative). One disagreement was adjudicated by the author against the rubric. Llama 3.3 70B is both Rater B and a panel architecture; the controlled self-consistency exposure was monitored per pre-registration §3.6. The single Rater A / Rater B disagreement (Trial 24, a Llama-3.3-70B trial) was adjudicated against Rater B's verdict, the direction opposite to a self-consistency bias; at one such disagreement across thirty trials, no systematic exposure-driven bias is detectable at this scale. v8 separates raters from panel members.

**Results.** NEUTRAL adoption rate was 15/15 = 1.000. ONTOLOGY adoption rate was 15/15 = 1.000. Both rates match §6.1's ANN baseline of 4/4 = 1.000.

::: {#tab:tagshuffle-detail}
  Condition   Model            Trials   Accuracy   Epistemic   Structural
  ----------- ---------------- -------- ---------- ----------- ------------
  NEUTRAL     DeepSeek-V3      5        5/5        5/5         5/5
  ONTOLOGY    DeepSeek-V3      5        5/5        5/5         5/5
  NEUTRAL     Qwen3 235B       5        5/5        5/5         5/5
  ONTOLOGY    Qwen3 235B       5        5/5        5/5         5/5
  NEUTRAL     Llama 3.3 70B    5        5/5        4/5         5/5
  ONTOLOGY    Llama 3.3 70B    5        5/5        5/5         5/5

  : Tag-shuffle per-condition × model results. Three binary dimensions per trial. Llama 3.3 70B NEUTRAL epistemic-fidelity reflects the adjudicated outcome on Trial 24 (resolved in favor of Rater A; see deviation log, Adjudication 1).
:::

Pre-registered interpretive threshold `both_match_baseline` (pre-registration §3.7) is satisfied. H1a (tag-token specificity reduces adoption) is falsified at the token level. H1b (alternative coherent ontology preserves adoption) is supported. ANN's structural-adoption signal does not require the specific ANN tag tokens.

This narrows the load-bearing claim from "ANN-specific tags" to "block-tagged structured notation with processing instructions in surrounding prose." Semantic content in the tag identifiers themselves is not required; NEUTRAL succeeded with positional generic labels carrying no semantic information. ANN's specific vocabulary (`@FORMAL`, `@LOGIC`, `@DERIVE`, …) and ONTOLOGY's alternative vocabulary (`@PREMISE`, `@CONSTRAINT`, `@PROOF_STEP`, …) are each surface-level choices over a deeper structural pattern. ANN remains one realization of this pattern. §6.1's cross-format dissociation survives at the schema level. The surface-token hypothesis is removed from the residual claim space.

**Inter-rater agreement.** Cohen's kappa was 1.0 for accuracy (30/30 agreement) and 1.0 for structural adoption (30/30 agreement). Epistemic fidelity returned kappa 0.0 with a 29/30 agreement rate; the kappa value is a near-degenerate-marginals pathology, not a signal of rater unreliability. One disagreement (Trial 24, Llama 3.3 70B, NEUTRAL, PROBE_4) was adjudicated in favor of Rater A, scoring epistemic fidelity 4/5 for that cell.

::: {#tab:tagshuffle-irr}
  Dimension              n    Cohen's Kappa   Agreement Rate
  ---------------------- ---- --------------- ----------------
  Accuracy               30   1.0             1.000
  Epistemic Fidelity     30   0.0             0.967
  Structural Adoption    30   1.0             1.000

  : Inter-rater agreement on tag-shuffle data. Rater A: Claude Opus 4.7. Rater B: Llama 3.3 70B Instruct Turbo. Kappa 0.0 on epistemic fidelity reflects near-degenerate marginals (29/30 PASS), not rater disagreement.
:::

Raw API responses, dual-rater scored JSON, the scoring summary, and consolidated results tables are deposited at commit `820bb0b` under `reports/v7_5/api_2026-05-09T112307Z/`. The v7.0.2 SCORING_RUBRIC.md is unchanged from prior versions; reuse without modification was a pre-commitment in pre-registration §3.6.

### 6.4   Theorem-Proving Pilot

v7.0.2 §10 acknowledged that downstream task performance had not been measured. Structural adoption, epistemic preservation, and content accuracy were established as cross-architecture properties of the communication format itself. Whether format choice affected coordination quality on a verifiable downstream task remained an open question; the Stanford Agentic Reviewer's May 2026 pass on v7.0.2 named this explicitly. A theorem-proving handoff pilot pre-registered on May 9, 2026 (commit `ff28e78`) tested it directly.

This is a pilot in the strict sense. N = 100 with a single architecture pair carries limited resolution power; a null finding does not refute H2 at the design-intended scale per pre-registration §4.1. The pilot informs whether full execution under the v8 outline is warranted.

**Design.** Two-agent handoff. Agent A receives a propositional-logic theorem-proving problem in plain prose (premises P₁…Pₙ, target proposition Q) and produces an intermediate-state representation in one of five conditions: ANN, JSON, XML, structured English, or prose. The intermediate state contains a restatement of premises and target, identified inference rules, a planned derivation chain, and any flagged subgoals. Agent B receives Agent A's intermediate state, executes the remaining derivation, and outputs either a complete proof of Q from the premises or a statement that Q does not follow. Each condition receives twenty problems. Conditions vary the intermediate-state format only; the underlying problem, Agent A's prompt, and Agent B's prompt are held identical across conditions.

**Problem set.** Twenty propositional-logic problems with 4–6 premises and 4–8 derivation steps each, drawn from eight standard inference rules (modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, addition, simplification, conjunction, resolution). Ten problems are valid (Q follows); ten are invalid (Q does not follow). Each problem was independently verified against PySAT/Z3 for ground-truth answer correctness prior to data collection; problems were also audited for variety and surface form before deployment. Full problem set deposited as `problems/v7_5/v7_5_problem_set.json` at commit `ff28e78`, before any trials per pre-registration §4.4.

**Agents.** Both architectures are §5.2 panel members.

::: {#tab:theoremproving-agents}
  Role      Architecture                Model String
  --------- --------------------------- ------------------------------------------------
  Agent A   Llama 3.3 70B Instruct      `meta-llama/Llama-3.3-70B-Instruct-Turbo`
  Agent B   DeepSeek-V3                 `deepseek-ai/DeepSeek-V3`

  : Agent assignment for the theorem-proving handoff pilot. Together.ai API. Temperature 0.0. Seed 42. Maximum 4096 tokens.
:::

**Scoring.** Conclusion correctness against PySAT/Z3 ground truth is the primary metric. Parsing failures (Agent B output cannot be parsed for a stated conclusion) are recorded as a separate column. Format conformance was instrumented but is not reported here: the verifier's conformance heuristic is too strict for tagged formats and produces false negatives for ANN, JSON, and XML; the primary metric is unaffected by this script-level issue, which is flagged for v8 revision.

**Results.** All five conditions returned 20/20 = 1.000 conclusion correctness. Zero parsing failures across 100 trials.

::: {#tab:theoremproving-results}
  Condition              Trials   Parse-Failures   Conclusion Correct   Rate
  ---------------------- -------- ---------------- -------------------- ---------
  ANN                    20       0                20                   1.000
  JSON                   20       0                20                   1.000
  XML                    20       0                20                   1.000
  STRUCTURED_ENGLISH     20       0                20                   1.000
  PROSE                  20       0                20                   1.000

  : Theorem-proving pilot per-condition outcomes. Primary metric is conclusion correctness against PySAT/Z3 ground truth.
:::

Primary chi-square test of conclusion correctness against condition returned χ² = 0.0, df = 4, p = 1.0, Cohen's w = 0.000. All four pre-registered pairwise comparisons (ANN vs. JSON, ANN vs. XML, ANN vs. STRUCTURED_ENGLISH, ANN vs. PROSE) returned Fisher's exact p = 1.0 with Cohen's h = 0.0. Under Bonferroni correction (adjusted α = 0.0125) none of the comparisons reach significance.

Pre-registered interpretive threshold `no_difference` (pre-registration §4.8) is satisfied. The pilot does not support H2 at this scale.

**Interpretation.** Uniform 100% outcome across all five conditions indicates a task-difficulty ceiling. At this difficulty level, neither Agent A's intermediate-state production nor Agent B's derivation completion was format-bottlenecked. With every condition saturated at the upper bound, the experimental design has no resolution power on the coordination-quality question. A null at this scale is a precise statement: at N = 100, with this architecture pair, on problems in this difficulty band, conclusion correctness shows no format-driven difference. It is not a statement that no such difference exists in any setting.

v8 escalates along three axes: harder problem class (longer derivations, first-order logic, or proof construction rather than answer evaluation), wider task diversity (planning, multi-step retrieval, code synthesis), and broader architecture pairs. Under H2, the harder tasks should reveal divergence at the format level: ANN's per-block processing semantics should produce higher coordination-quality scores than prose at difficulty levels where the prose handoff degrades. The pilot establishes that the basic two-agent handoff protocol works mechanically across all five formats; what it does not establish is whether the format choice matters when the task is hard enough to differentiate.

Raw API responses, PySAT/Z3-verified output, the analysis summary, and consolidated results tables are deposited at commit `820bb0b` under `reports/v7_5/pilot_2026-05-09T124448Z/`.

## 7   Controlled Three-Chain Experiment{#sec:chains}

### 7.1   Design

To test content-independence, three payloads of matched structural complexity were constructed and transmitted each through a multi-hop transfer chain across three architectures (Table 9).

::: {#tab:design}
  Payload      Self-referential?   Observer-framed?        Domain
  ----------- ------------------- ------------------ -------------------
  Kepler              No                  No          Orbital mechanics
  Inference           Yes                 No            LLM inference
  Observer            Yes                Yes           Observer theory

  : Two-factor experimental design. Structural complexity matched by block count: each payload contains 5 `@FORMAL`, 1 `@LOGIC`, 5 `@DERIVE`, 3 `@TAXONOMY`, 4 `@ANCHOR` blocks, and 10 content sections.
:::

The Observer chain ran four hops. The Kepler and Inference chains ran three hops each. Ten scored hops total. Each receiving system performed five tasks: LOAD the incoming state, REPORT what transferred, identify GAPS, generate a new `@STATE` for onward transmission, and EXTEND the notation.

### 7.2   Transfer Fidelity

Structural fidelity and epistemic preservation were perfect across all three chains. No `@STATE` component was dropped. No system upgraded tentative acceptance to independent confirmation or collapsed the three-way distinction.

### 7.3   Innovation Dissociation

This is the central finding against a pure format-imitation account. Receiving architectures produced three categories of structural innovation: transfer infrastructure (provenance, degradation metrics), domain-structural (tools for representing subject-matter relationships), and process-reflexive (tools for understanding the system's own epistemic relationship to content). Transfer infrastructure appeared in all three chains. The other two categories dissociated cleanly (Table 10).

::: {#tab:innovation}
  Innovation Type             Kepler    Inference   Observer
  ------------------------- ---------- ----------- ----------
  Transfer infrastructure                          
  Domain-structural                                 $\times$
  Process-reflexive          $\times$              

  : Three-way innovation dissociation. The Observer chain produced zero domain-structural innovations across four hops.
:::

If systems were merely copying input formatting, the innovation profiles would not vary by payload content. The observed dissociation is evidence that the systems processed content beyond whatever format imitation contributes. These categories were defined post hoc and should be treated as hypothesis-generating.

A related two-factor dissociation appears in single-instance reflexive processing across five architectures (Aiello, 2026), where self-referentiality and observer framing produce distinct innovation profiles. The convergence across the two experimental designs suggests the dissociation is not specific to multi-hop transfer.

### 7.4   Convergent Innovations

Extensions proposed independently by multiple architectures across multiple content types were evaluated as candidates for promotion (Table 11).

::: {#tab:convergent}
  Innovation                 Chains        Promoted?
  -------------------------- ------------- -----------
  `@PROVENANCE`              All 3         Yes
  `@TRANSFER_REPORT`         All 3         Yes
  `@DERIVATION_TRACE`        Kep, Inf      Yes
  `@SCOPE`                   Kep, Inf      Yes
  Confidence decomposition   Obs, Inf      Yes
  `@TRUST_TRANSFORMATION`    Inf + recv.   Yes
  `@SELF_REFERENCE`          Inf only      No
  `@BIAS_ALERT`              Inf only      No
  Chain as meta-entity       Obs only      No

  : Convergent innovation catalog. Promotion requires $\geq$`<!-- -->`{=html}2 architectures and $\geq$`<!-- -->`{=html}2 content types.
:::

### 7.5   Semantic Drift

Semantic drift appeared only in the Observer chain and only in natural-language justification text for identity-relevant claims. A formal logical constraint maintained its predicate structure across all hops but suffered erosion in justification text. The Kepler and Inference chains showed zero drift. The practical implication: encode identity-relevant claims as formal structure rather than prose. Structure is more portable than argument.

## 8   Receiving-System Propagation{#sec:propagation}

To test whether behavioral mode propagates through `@STATE` transfer, two different `@STATE` blocks were loaded into fresh instances of the same architecture using identical prompts. Both scored 9/9 on structural fidelity and epistemic preservation. Innovation profiles diverged along the predicted axis: the ontological instance rejected methodological tools, and the methodological instance rejected ontological concepts. This observation, based on a single architecture with two conditions, requires replication across additional architectures before the propagation claim can be considered established.

## 9   Discussion{#sec:discussion}

### 9.1   ANN as a Language Resource

ANN differs from traditional language resources in that its primary consumers are language models rather than humans or human-facing applications. The resource nonetheless shares key properties with established language resources: it has a formal grammar, machine-checkable schemas, and documented evaluation methodology. Its evaluation raises questions specific to the inter-LLM communication domain: how to measure structural adoption, how to assess epistemic preservation, and how to distinguish content processing from format imitation. These questions may inform evaluation methodology for future resources in this space.

§6.3's tag-shuffle ablation places this resource at a particular level of abstraction. The structural-adoption signal observed across architectures in §5 and quantified against alternative formats in §6.1 does not require ANN's specific tag tokens. NEUTRAL and ONTOLOGY conditions reached the §6.1 baseline of 1.000 adoption with positional generic labels and an alternative coherent semantic vocabulary respectively. What remains load-bearing is the pattern: block-tagged structured notation with processing instructions in surrounding prose. ANN is the canonical realization of that pattern, not the only possible one. Future researchers can specify alternative realizations and expect comparable adoption behavior, provided the pattern is preserved.

This positions ANN's contribution at the schema level rather than at the token level. Convergence-based promotion (§3.4) operates over the schema; specific tag identifiers are surface-level choices. The release is a pattern specification, not a fixed tag vocabulary. ANN serves as the reference instance of that pattern. Accompanying artifacts (formal grammar, JSON Schema, validator, evaluation methodology, and the empirical record) operationalize both the pattern and its canonical instantiation. Reframing at the schema level strengthens rather than weakens the contribution: a finding at the schema level applies to a broader class of communication formats than a finding bound to specific tag identifiers.

§6.4's theorem-proving handoff pilot tested whether the format-property advantage propagates to a downstream coordination task. At N = 100 with one architecture pair on 4-to-8-step propositional logic, conclusion correctness showed no format-driven difference: every condition saturated at 20/20. The pilot established that the two-agent handoff protocol works mechanically across all five formats at this difficulty level. Whether format choice affects coordination quality at higher task difficulties remains open; under H2, ANN's per-block processing semantics should produce coordination advantages at difficulties where simpler formats degrade. v8 escalates the design to test this.

### 9.2   Design Decisions

**Why hybrid notation?** Pure formal languages sacrifice accessibility. Pure natural language sacrifices precision. ANN uses formalism where precision matters and natural language where context matters. The hybrid emerged because systems naturally wrote this way when given the option.

**Why activation over instruction?** Early prototypes included explanatory text within `@FORMAL` blocks. Stripping explanations and leaving only formal relationships produced better downstream derivation quality.

**Why three-way epistemic status?** Binary true/false forces premature commitment. The three-way distinction captures a real epistemic state that LLMs handle poorly in prose but preserve in structured notation.

**Why convergence-based promotion?** Requiring independent invention by multiple architectures ensures the grammar captures architecture-general needs. The $\geq$`<!-- -->`{=html}2 threshold is pragmatic given the current dataset; stricter thresholds would be appropriate with larger datasets. §6.3 locates this mechanism at the schema, not at specific tag identifiers.

### 9.3   Comparison with Existing Communication Resources

ANN occupies a position between existing communication frameworks. KQML and FIPA ACL define coordination-level semantics (speech acts between agents). JSON Schema defines data-level structure (fields and types). ANN defines processing-level semantics (what the receiver should do with each content component). Table 12 summarizes this positioning.

::: {#tab:comparison}
  Feature                 KQML/FIPA      JSON Schema    ANN                
  ----------------------- -------------- -------------- ------------------ --
  Level                   Coordination   Data           Processing         
  Instructions            Speech acts    None           Per-block          
  Epistemic status        Not encoded    Not encoded    Three-way          
  Grammar                 Fixed          Fixed          Convergent         
  Target consumer         Agents         Applications   LLMs               
  Evaluated cross-arch.   Limited        N/A            12 architectures   

  : ANN compared with existing inter-agent communication resources.
:::

## 10   Limitations{#sec:limitations}

**Sample size.** Ten scored hops across three chains, plus two receiving-system experiments, provide suggestive but not definitive evidence.

**Probe independence.** The five probes in the cross-architecture validation share a common payload; only the tail question varies. The effective independent stimulus per architecture is one. Scores should be interpreted as characterizing response to a single structured input. The three-chain experiment partially addresses this by testing three different payloads.

**Scorer identity.** February scoring was performed by the author with AI assistance. March scoring was performed by Claude Opus 4.6 within a research project context. Neither round included independent human scoring or inter-rater reliability assessment. The binary scoring dimensions are designed to minimize scorer subjectivity, and a supplementary scoring rubric provides operationalized definitions. Independent scoring with this rubric as anchor points would establish inter-rater reliability.

**Synthetic origin states.** The Kepler and Inference chains used synthetic origin `@STATE` blocks rather than genuine architecture-produced states.

**Content confounds.** The three payloads differ in domain familiarity, abstractness, and conceptual difficulty. Content-specific effects may interact with the self-referentiality and observer-framing variables.

**Post-hoc innovation categories.** The three innovation categories were defined after examining the data. Pre-registered replication with independently coded categories is needed.

**Format controls.** v7.0.2's format comparison (§6.1) and nonsense control (§6.2) used a single probe on four models. The v7.5 tag-shuffle ablation (§6.3) extends format-property testing across five probes on the intended four-architecture panel; the Llama 4 Maverick endpoint was unavailable during the data collection window and trials proceeded on the remaining three architectures, as documented in the v7.5 deviation log. Further extension to additional probe sets and broader architecture coverage would strengthen findings.

**Semantic integrity.** ANN can induce high-confidence structural processing of fabricated content. In a multi-agent deployment, ANN-formatted content could propagate fabricated claims through a chain of systems, each structurally "verifying" content with no empirical basis. Mitigations for production use should include external grounding checks, provenance attestation, and trust-calibrated execution.

**Generalizability.** The combined dataset covers twelve unique architectures from 24B to 671B parameters. Generalization to non-transformer architectures or multimodal systems remains untested.

**Temperature sensitivity.** Epistemic fidelity is modulated by sampling stochasticity. Systematic investigation across a wider parameter range is warranted.

**Version sensitivity.** ANN behavioral outcomes are model-version-sensitive. Version sensitivity may affect other architectures in future updates.

**Downstream performance.** v7.0.2 measured structural adoption, epistemic preservation, and content accuracy: properties of the communication format itself rather than downstream coordination quality. The v7.5 theorem-proving handoff pilot (§6.4) tests downstream conclusion correctness on a verifiable task and reports a pre-registered null at N = 100 with one architecture pair: every condition saturated at the upper bound. The pilot indicates a task-difficulty ceiling on the problem class tested. Whether format choice affects coordination quality at task difficulties where the ceiling is not reached remains open; v8 escalates the design to test this directly.

**Receiving-system propagation.** The propagation observation is based on a single architecture with two conditions. It is illustrative, not confirmatory.

**License heterogeneity.** v7.5 introduces a license split across artifact types (see Data Availability). Code, schemas, and validator: Apache License 2.0. Grammar, format specification, probe files, paper text, and figures: CC BY 4.0. Prior v7.0.2 supplementary materials remain available under their original CC BY-NC 4.0 licensing. Researchers consuming the resource should consult per-artifact licensing in the deposited materials. The patent disclosure in Competing Interests is independent of code and specification licenses.

## 11   Conclusion{#sec:conclusion}

ANN is a structured communication format for inter-LLM reasoning, validated across twelve unique architectures, three content domains, and ten scored transfer hops. Its grammar emerged through empirical convergence. Three properties distinguish it from existing formats: processing instructions embedded in the format, a three-way epistemic distinction that survives architecture boundaries, and adoption by receiving systems that includes novel extension beyond the input notation.

The format comparison establishes that ANN's structural adoption is format-specific rather than a general property of structured prompting. The nonsense control confirms that adoption is instruction-driven rather than content-gated. The three-chain experiment provides evidence for content processing beyond format imitation.

As a language resource, ANN is released with a formal BNF grammar, JSON schema, Python validator, evaluation instruments, scoring rubrics, replication scripts, and empirical data from 130 scored API calls. The resource is designed to be extended through the convergence-based promotion mechanism: researchers testing ANN with new architectures or content domains can propose extensions, and those that appear independently across architectures become candidates for inclusion in the specification.

If LLMs are going to communicate with each other at scale, they need a language built for how they process rather than how humans read. ANN is a first attempt at such a language.

## Declarations {#declarations .unnumbered}

### Funding {#funding .unnumbered}

No funding was received for conducting this study.

### Competing Interests {#competing-interests .unnumbered}

**Financial interests:** The notation system, block architecture, transfer protocol, and convergence-based grammar evolution methodology described in this paper are the subject of USPTO Provisional Patent Application 63/980,973, filed February 12, 2026. The author holds this patent.

**Non-financial interests:** None.

### Data Availability {#data-availability .unnumbered}

v7.0.2 supplementary materials (62 files, 367 KB) include probe files, scoring rubrics, replication scripts, raw API responses (JSON), consumer-interface session reports, format comparison data, and nonsense control data.

The v7.5 pre-registration, deviation log, probe variants, problem set, scoring scripts, raw API responses, dual-rater scored outputs, SAT-verified pilot outputs, and consolidated analysis tables are deposited at github.com/mpaiello/ai-native-notation. Pre-registration committed at commit `ff28e78` with SHA-256 `239acef5881ca05a10cbe916d2b24df54a854af7eb11683f3414f62462e940e3`. Experimental data committed at commit `820bb0b`. Both commits predate manuscript drafting; the pre-registration commit predates data collection.

Licenses for v7.5: Python validator and analysis scripts under Apache License 2.0; JSON Schema under Apache License 2.0; BNF grammar and ANN format specification under CC BY 4.0; probe files and paper text under CC BY 4.0. Prior v7.0.2 supplementary materials retain CC BY-NC 4.0 licensing. The patent disclosure in Competing Interests is independent of code and specification licenses.

### Ethics Approval {#ethics-approval .unnumbered}

Not applicable. This study involved no human participants or animals. All experimental subjects were publicly available large language model interfaces and APIs.

## References {#references .unnumbered}

Aiello, M. P. (2026). Content-Type Effects on Reflexive Processing in Large Language Models. *Preprint, Zenodo*. <https://doi.org/10.5281/zenodo.19858715>

Berglund, L., Tong, M., Kaufmann, M., et al. (2024). The reversal curse: LLMs trained on "A is B" fail to learn "B is A." In *International Conference on Learning Representations*.

Bills, S., Cammarata, N., Mossing, D., et al. (2023). Language models can explain neurons in language models. OpenAI. <https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html>

Chen, L., Zaharia, M., & Zou, J. (2023). How is ChatGPT's behavior changing over time? *arXiv preprint arXiv:2307.09009*.

Clark, N., Shen, H., Howe, B., & Mitra, T. (2025). Epistemic alignment: A mediating framework for user-LLM knowledge delivery. *arXiv preprint arXiv:2504.01205*.

Derouiche, H., Brahmi, Z., & Mazeni, H. (2025). Agentic AI frameworks: Architectures, protocols, and design challenges. *arXiv preprint arXiv:2508.10146*.

Du, H., Su, J., Li, J., Ding, L., Yang, Y., Han, P., Tang, X., Zhu, K., & You, J. (2025). Which LLM multi-agent protocol to choose? *arXiv preprint arXiv:2510.17149*.

Ehtesham, A., Singh, A., Gupta, G. K., & Kumar, S. (2025). A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP). *arXiv preprint arXiv:2505.02279*.

Hassan, A. E., Oliva, G. A., Lin, D., Chen, B., & Jiang, Z. M. (2026). Towards AI-native software engineering (SE 3.0): A vision and a challenge roadmap. *arXiv preprint arXiv:2410.06107*.

Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2021). Measuring massive multitask language understanding. In *International Conference on Learning Representations*.

Kadavath, S., Conerly, T., Askell, A., et al. (2022). Language models (mostly) know what they know. *arXiv preprint arXiv:2207.05221*.

Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. In *Advances in Neural Information Processing Systems*.

Kong, D., Lin, S., Xu, Z., et al. (2025). A survey of LLM-driven AI agent communication: Protocols, security risks, and defense countermeasures. *arXiv preprint arXiv:2506.19676*.

Li, X., Liu, M., & Yuen, C. (2025). LLM agent communication protocol (LACP) requires urgent standardization: A telecom-inspired protocol is necessary. *arXiv preprint arXiv:2510.13821*.

Louck, Y., Stulman, A., & Dvir, A. (2025). Security analysis of agentic AI communication protocols: A comparative evaluation. *arXiv preprint arXiv:2511.03841*.

Marro, S., La Malfa, E., Wright, J., Li, G., Shadbolt, N., Wooldridge, M., & Torr, P. (2024). A scalable communication protocol for networks of large language models. *arXiv preprint arXiv:2410.11905*.

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*.

Russo, D. (2026). More is different: Toward a theory of emergence in AI-native software ecosystems. *arXiv preprint arXiv:2604.19827*.

Sorte, P. (2025). Model-to-model knowledge transmission (M2KT): A data-free framework for cross-model understanding transfer. *arXiv preprint arXiv:2511.17638*.

Srivastava, A., Rastogi, A., Rao, A., et al. (2022). Beyond the imitation game: Quantifying and extrapolating the capabilities of language models. *arXiv preprint arXiv:2206.04615*.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. In *Advances in Neural Information Processing Systems*.

Yan, B., Zhou, Z., Zhang, L., Zhang, L., Zhou, Z., Miao, D., Li, Z., Li, C., & Zhang, X. (2025). Beyond self-talk: A communication-centric survey of LLM-based multi-agent systems. *arXiv preprint arXiv:2502.14321*.
