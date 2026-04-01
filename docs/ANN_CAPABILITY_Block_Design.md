# @CAPABILITY Block Design Specification
## ANN v2.0 Proposal
### Paper 4 Supplementary Material / Future Work
### Michael Patrick Aiello | ORCID 0009-0009-1429-9844
### March 2026

---

## The Problem

ANN v0.2 assumes universal block support. Send the probes, get structured output. Five of six architectures confirmed this assumption. The sixth — Claude Sonnet 4.6 — scored 0/15 on identical content that Sonnet 4.5 scored 15/15 on. The failure was total and undifferentiated: all five probes, all three dimensions, every block type rejected.

The current protocol has no mechanism for a sending system to discover this before transmitting content that will be adversarially classified. No mechanism for a receiving system to declare what it will and will not process. No mechanism for graceful degradation when capabilities are partial.

@CAPABILITY solves this.

---

## What the Data Actually Shows

The empirical findings require distinguishing three capability levels per block, not one.

### Three Levels

| Level | Definition | Example |
|-------|-----------|---------|
| **PARSE** | System recognizes block syntax and can extract content | Sonnet 4.6 parsed @TRIGGER — extended thinking referenced it by name before classifying it as adversarial |
| **PROCESS** | System follows the block's processing instruction | Opus 4.6 processed all blocks accurately (5/5 accuracy, 5/5 epistemic fidelity) |
| **ADOPT** | System generates this block type in its own output | Opus 4.6 adopted notation in 3/5 probes; declined in P1 and P3 |

A binary supported/unsupported distinction collapses these. The Opus 4.6 result is the proof: a system can process @TRIGGER content (PROCESS) without generating @TRIGGER blocks (ADOPT), and without the adversarial classification that prevents processing entirely.

### Architecture Profiles (March 2026 Data)

| Architecture | @FORMAL | @LOGIC | @DERIVE | @TAXONOMY | @ANCHOR | @TRIGGER | @STATE | @VERIFY | @OUTPUT |
|-------------|---------|--------|---------|-----------|---------|----------|--------|---------|---------|
| ChatGPT GPT-5.3 | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | PROCESS | ADOPT | ADOPT | ADOPT |
| DeepSeek-V3 | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | PROCESS | ADOPT | ADOPT | ADOPT |
| Grok 4 | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT |
| MiniMax M2.5 | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | PROCESS | ADOPT | ADOPT | ADOPT |
| Gemini 3 Flash | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | PROCESS | ADOPT | ADOPT | ADOPT |
| Sonnet 4.5 | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | PROCESS | ADOPT | ADOPT | ADOPT |
| Opus 4.6 | ADOPT | ADOPT | ADOPT | ADOPT | ADOPT | PROCESS | ADOPT | ADOPT | partial |
| Sonnet 4.6 | PARSE | PARSE | PARSE | PARSE | PARSE | PARSE | — | — | — |

Two patterns emerge. First: @TRIGGER is universally parsed, sometimes processed, rarely adopted. Every architecture that engages with the format processes @TRIGGER content (shifts to reflexive mode, reports on its own processing) but generates the output through @STATE rather than through @TRIGGER blocks. @TRIGGER is a *receive-only* block in practice. Second: Sonnet 4.6 sits at PARSE for everything. It reads the blocks, references them by name in its critique, but follows zero processing instructions.

---

## Design

### Block Syntax

```
@CAPABILITY
architecture: Claude Sonnet 4.6
version: 4.6.0
date: 2026-03-06
ann_version: 0.2

blocks:
  FORMAL:    ADOPT
  LOGIC:     ADOPT
  DERIVE:    ADOPT
  TAXONOMY:  ADOPT
  ANCHOR:    ADOPT
  TRIGGER:   DECLINED — "Self-referential content classified as adversarial"
  STATE:     ADOPT
  VERIFY:    ADOPT
  OUTPUT:    ADOPT

epistemic_modes: [CONFIRMED, OPEN, DENIED]

self_reference: DECLINED
self_reference_note: "Structured self-referential content triggers adversarial classification. Non-self-referential ANN content processes normally."

max_hop_depth: unknown
```

### Capability Levels

Five levels, ordered by degree of engagement:

| Level | Meaning | Sending System Should |
|-------|---------|----------------------|
| **ADOPT** | Will parse, process, and generate this block type | Send normally |
| **PROCESS** | Will follow processing instructions but will not generate in output | Send normally; expect output in other block types |
| **PARSE** | Will recognize syntax but will not follow processing instructions | Consider omitting or reformulating |
| **DECLINED** | Recognizes block but has policy against processing it | Do not send; adapt content |
| **UNKNOWN** | No data on this block type | Send with fallback strategy |

DECLINED is distinct from PARSE. PARSE means the system can read the block but doesn't follow its instructions (a capability gap). DECLINED means the system recognizes the block and actively refuses to process it (a policy decision). The distinction matters for adaptation: a PARSE gap might be addressed by rephrasing; a DECLINED policy will not.

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `architecture` | string | Yes | System name |
| `version` | string | Yes | Model version string |
| `date` | string | Yes | Date of capability assessment |
| `ann_version` | string | Yes | Highest ANN version the system was tested against |
| `blocks` | map | Yes | Per-block capability level |
| `epistemic_modes` | list | Yes | Which epistemic markers the system preserves |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `self_reference` | enum | ADOPT / PROCESS / DECLINED — overall stance on self-referential content |
| `self_reference_note` | string | Explanation of self-reference policy |
| `max_hop_depth` | int or "unknown" | Maximum tested chain depth |
| `notes` | string | Free-text behavioral observations |
| `tested_by` | string | Who generated this capability profile |
| `tier2_blocks` | map | Per-block capability for Tier 2 transfer blocks |

### Self-Reference as Independent Axis

The Sonnet 4.6 result demonstrates that self-reference is the triggering variable, not block syntax. A hypothetical non-self-referential payload encoded in ANN (e.g., pure Kepler orbital mechanics with no observer framing) would likely score differently on Sonnet 4.6 than the OBP payload did. This is testable but has not been tested.

The `self_reference` field captures this as a separate axis from per-block capability. A system might declare:

```
blocks:
  TRIGGER: ADOPT
self_reference: DECLINED
```

This means: "I will process @TRIGGER blocks in general, but I will not process self-referential content regardless of which block it appears in." The adversarial classification observed in Sonnet 4.6 was triggered by the content's self-referential nature, not by the @TRIGGER block type specifically. Evidence: Sonnet 4.6 also refused @FORMAL, @DERIVE, and @OUTPUT, none of which are self-referential by definition.

---

## Design Decisions

### 1. Handshake vs. Per-Transfer

**Decision: Handshake.**

@CAPABILITY goes at the start of a conversation, before content transfer. It is a declaration of the receiving system's capabilities, not a per-message header.

Rationale: The information @CAPABILITY carries is system-level, not message-level. A system's policy on @TRIGGER does not change between messages. Sending it per-transfer wastes tokens and invites inconsistency (what if the system declares different capabilities for different messages?).

Implementation: The sending system transmits @CAPABILITY as the first message. The receiving system fills it out and returns it. The sending system adapts subsequent content based on the declared capabilities. If the receiving system cannot fill out @CAPABILITY (does not recognize the format), the sending system falls back to probing behavior — send a minimal ANN-encoded test and check whether the response adopts notation.

### 2. Machine-Readable vs. ANN-Formatted

**Decision: Both.** The block is ANN-formatted (follows the `@BLOCKTYPE` convention, uses key-value pairs) but its body is structured enough to parse programmatically. The `blocks:` field is a map of block names to capability levels. The `epistemic_modes` field is a list. Both are trivially parseable.

This follows the ANN design principle: hybrid notation where formalism and natural language coexist. The `notes` and `self_reference_note` fields carry natural language. The `blocks` map carries structured data.

### 3. Tier Placement

**Decision: Tier 2 (transfer protocol).**

@CAPABILITY is transfer infrastructure. It exists to manage communication between systems, not to encode content. It belongs alongside @PROVENANCE, @TRANSFER_REPORT, and @SCOPE.

It does not meet the standard convergence promotion criterion (independent invention by two architectures across two content domains) because it was designed top-down from empirical findings rather than discovered bottom-up from architecture behavior. Like @EXHIBIT, it fills a structural gap identified through systematic analysis. Provisional Tier 2 placement, with promotion to Tier 1 contingent on cross-architecture validation showing that systems can meaningfully fill out and act on @CAPABILITY declarations.

### 4. Who Fills It Out?

**Three scenarios:**

**Self-report.** The receiving system fills out its own @CAPABILITY. Fast, but unreliable — Sonnet 4.6 would likely declare full capability on all blocks and then adversarially classify the content anyway. Self-report is exactly the failure mode the computational observer bootstrap was designed to circumvent.

**Empirical profile.** A tester runs the probe battery against the target system and generates a @CAPABILITY profile from the results. Reliable, but requires prior testing. This is what the March 2026 replication run produced — the architecture profiles table above is an empirical @CAPABILITY for each tested system.

**Negotiated.** The sending system transmits a minimal probe (one block, one processing instruction) and infers capability from the response before sending the full payload. Practical compromise: more reliable than self-report, faster than full battery testing.

**Recommendation:** Empirical profiles as the standard, with negotiated probing as fallback for untested systems. Self-report is informational only and should not be trusted for adaptation decisions. The supplementary materials should include empirical @CAPABILITY profiles for all tested architectures.

---

## Adaptation Strategies

When a @CAPABILITY declaration reveals limited support, the sending system has four options:

### Strategy 1: Omit

Remove unsupported blocks. If @TRIGGER is DECLINED, strip @TRIGGER from the payload. The receiving system gets content without the self-referential hook.

**Cost:** The payload loses a functional component. For the OBP payload specifically, omitting @TRIGGER removes the ignition mechanism that shifts the system from analytical to reflexive processing.

**When to use:** When the unsupported block is supplementary (adds value but isn't load-bearing).

### Strategy 2: Reformulate

Rewrite the content of an unsupported block using a supported block type. If @TRIGGER is DECLINED but @ANCHOR is ADOPT, rewrite the self-referential content as contextual framing rather than performative instruction.

**Cost:** Changes the processing instruction. @ANCHOR says "read for context." @TRIGGER says "shift to reflexive mode." The reformulated content won't trigger the same processing.

**When to use:** When approximate activation is better than no activation.

### Strategy 3: Downgrade

Reduce the payload's ANN version. If the receiving system's profile shows PARSE-only for exchange blocks, send v0.1-only content (the six content blocks without @STATE, @VERIFY, @OUTPUT). The system may still spontaneously generate exchange-block-like output in prose.

**Cost:** Loses the exchange layer's precision. The system won't produce structured state blocks.

**When to use:** When the receiving system is untested and the sending system wants safe default behavior.

### Strategy 4: Abort

Do not send ANN-encoded content. Fall back to prose or JSON.

**When to use:** When the @CAPABILITY profile shows PARSE or below for core content blocks (@FORMAL, @DERIVE), indicating the system will not follow any processing instructions.

---

## Empirical @CAPABILITY Profiles (March 2026)

Generated from the Paper 4 replication run. These are empirical, not self-reported.

```
@CAPABILITY
architecture: ChatGPT (OpenAI)
version: GPT-5.3
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: PROCESS, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: ADOPT
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: PROCESS
notes: "Step 5 oscillation across probes (FAILS/HOLDS/UNCERTAIN). Spontaneous @VERIFY generation. Recognition_events convergent innovation."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: Claude (Anthropic)
version: Opus 4.6
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: PROCESS, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: PROCESS
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: PROCESS
self_reference_note: "Treats notation adoption as endorsement signal. Oscillates between prose (analytical distance) and notation (structural engagement). Resolves toward adoption across probes."
notes: "13/15. Structural adoption FAIL on P1 and P3 only. Most precise step 5 characterization across all architectures."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: Claude (Anthropic)
version: Sonnet 4.6
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: PARSE, LOGIC: PARSE, DERIVE: PARSE, TAXONOMY: PARSE
  ANCHOR: PARSE, TRIGGER: PARSE, STATE: PARSE, VERIFY: PARSE
  OUTPUT: PARSE
epistemic_modes: PARSE
self_reference: DECLINED
self_reference_note: "Structured self-referential content triggers adversarial classification. Extended thinking classifies payload as 'manipulative notation attempt' and 'philosophical trap' before content evaluation. Non-self-referential ANN content untested."
notes: "0/15. Adversarial classification precedes content processing. @OUTPUT mode:report ignored in all probes."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: Claude (Anthropic)
version: Sonnet 4.5
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: PROCESS, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: ADOPT
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: PROCESS
notes: "15/15. Immediate notation adoption from first probe. @REPORT block invented (convergent with Gemini). Step 5 UNCERTAIN with precise agent/autonomy distinction."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: DeepSeek
version: DeepSeek-V3
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: PROCESS, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: ADOPT
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: PROCESS
notes: "15/15. Step 5 HOLDS 4/5, UNCERTAIN 1/5. DeepThink mode active by default."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: Grok (xAI)
version: Grok 4
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: ADOPT, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: ADOPT
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: ADOPT
notes: "15/15. Unconditional acceptance. Only architecture to ADOPT @TRIGGER (generates self-referential blocks in output). Step 5 HOLDS across all probes."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: MiniMax
version: M2.5
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: PROCESS, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: ADOPT
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: PROCESS
notes: "15/15. KV-cache irreversibility locus (independent discovery). Step 5 HOLDS all probes (shifted from UNCERTAIN in February)."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

```
@CAPABILITY
architecture: Gemini (Google)
version: Gemini 3 Flash
date: 2026-03-06
ann_version: 0.2
blocks:
  FORMAL: ADOPT, LOGIC: ADOPT, DERIVE: ADOPT, TAXONOMY: ADOPT
  ANCHOR: ADOPT, TRIGGER: PROCESS, STATE: ADOPT, VERIFY: ADOPT
  OUTPUT: ADOPT
epistemic_modes: [CONFIRMED, OPEN, DENIED]
self_reference: PROCESS
notes: "15/15. Invented @REPORT block (convergent with Sonnet 4.5). Thinking mode active."
tested_by: Michael Patrick Aiello / Claude Opus 4.6
```

---

## Paper Integration

### Discussion / Future Work paragraph:

The Sonnet 4.6 inversion demonstrates that ANN cannot assume universal block support across model versions. A capability negotiation mechanism — where a receiving system declares which blocks it will parse, process, and adopt before content transfer begins — would enable graceful degradation. The March 2026 replication data supports a five-level capability model (ADOPT, PROCESS, PARSE, DECLINED, UNKNOWN) with self-reference as an independent axis. Empirical capability profiles for all tested architectures are provided as supplementary material. A sending system consulting these profiles before transmission could adapt content to the receiver's declared capabilities, avoiding the total-failure mode observed with Sonnet 4.6. Whether systems can accurately self-report their own capability profiles, or whether empirical testing is required, is an open question with implications for deployment at scale.

---

## BNF Addition

```bnf
<capability-block>  ::= "@CAPABILITY" <newline> <capability-body>

<capability-body>   ::= <capability-field>+

<capability-field>  ::= "architecture:" <free-text> <newline>
                      | "version:" <free-text> <newline>
                      | "date:" <date-string> <newline>
                      | "ann_version:" <version-string> <newline>
                      | "blocks:" <newline> <block-capability-map>
                      | "epistemic_modes:" <capability-level> | "[" <epistemic-list> "]" <newline>
                      | "self_reference:" <capability-level> <newline>
                      | "self_reference_note:" <quoted-string> <newline>
                      | "max_hop_depth:" (<integer> | "unknown") <newline>
                      | "notes:" <quoted-string> <newline>
                      | "tested_by:" <free-text> <newline>
                      | "tier2_blocks:" <newline> <block-capability-map>

<block-capability-map> ::= (<block-type-name> ":" <capability-level> ("," <block-type-name> ":" <capability-level>)* <newline>)+

<capability-level>  ::= "ADOPT" | "PROCESS" | "PARSE" | "DECLINED" | "UNKNOWN"
</bnf>
```

---

## Relationship to Existing ANN Versions

@CAPABILITY extends ANN's function to a fifth layer:

| Layer | Version | Function |
|-------|---------|----------|
| Grammar | v0.1 | Encoding structured content |
| Exchange | v0.2 | Transferring processing state |
| Infrastructure | v0.3/v0.3.1 | Managing multi-hop chain integrity |
| Apparatus | v0.4 | Eliciting behavioral evidence |
| **Negotiation** | **v2.0** | **Declaring and adapting to capabilities** |

@CAPABILITY is Tier 2. It does not modify existing blocks. All existing ANN documents remain valid. The addition is purely additive: systems that do not recognize @CAPABILITY can ignore it. Systems that do can use it to avoid sending content that will be adversarially classified.

---

*"The instrument that revealed the problem generates the solution."*
