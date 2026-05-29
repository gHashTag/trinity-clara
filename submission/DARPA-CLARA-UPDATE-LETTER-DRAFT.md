# DRAFT — Update Letter to DARPA CLARA (NOT SENT)

> **Status: DRAFT for internal review only. Do not send without explicit
> approval.** This is an *update / addendum* to our prior CLARA materials,
> not a new submission. The CLARA abstract/proposal windows
> (DARPA-PA-25-07-02) have closed; this letter informs the program of a
> concrete engineering milestone (silicon submitted to fabrication) and
> offers the open-source artefacts for review. It makes no claim of an
> award or of acceptance.

---

**To:** CLARA@darpa.mil
**Cc:** (program manager, DSO — Dr. Benjamin Grosof)
**From:** Dmitrii Vasilev — admin@t27.ai
**Re:** TRINITY / TRI-NET — update on open-silicon realization of the ten
CLARA AI-safety gaps (Apache-2.0)
**Date:** _[fill on send]_

Dear CLARA Program Team,

This is a brief update on the TRINITY (TRI-NET) work we previously shared
with the CLARA program. We are writing for two reasons: (1) to report an
engineering milestone — the reasoning and safety primitives have been
realized as open-source Verilog and submitted to a fabrication shuttle —
and (2) to offer the scientific rationale for implementing CLARA's
glass-box reasoning primitives in silicon over Galois-Field (GF) numeric
formats. We make no claim of acceptance and understand the formal
submission windows have closed; we offer these artefacts as open-source
contributions for the program's awareness.

## 1. What changed since our last contact

The ten CLARA AI-safety gaps are now implemented as synthesizable
Verilog modules in a single open-source chip design (the "Euler" die,
TinyTapeout project #558) and submitted to the **TinyTapeout TTSKY26b
shuttle** (SKY130 PDK). Submission to the shuttle closed 2026-05-18 UTC;
fabricated dies are estimated to return in **December 2026**. The design,
testbenches, and gap-to-module traceability are public under Apache-2.0.

We want to be precise about status: **the dies have not yet returned**,
so all hardware-level claims are at the level of synthesized,
lint-clean, simulation-exercised RTL — not yet silicon-measured. We flag
this explicitly throughout our documentation.

## 2. How this maps to CLARA's glass-box requirement

CLARA defines assurance as verifiability with strong explainability to
humans, based on automated logical proofs and vetted logic building
blocks — and is explicitly skeptical of "tacking AR onto an LLM." Our
design takes that seriously at the gate level: each safety/reasoning gap
is a **small, single-purpose, exhaustively inspectable AR primitive**,
and a composition supervisor wires them so that every intermediate result
(derived facts, restraint reason, proof trace) is exposed on observable
ports rather than hidden inside an opaque network.

The ten gaps, as actually implemented (full function descriptions and
claim-status labels are in `submission/HARDWARE-REALIZATION-TRINET.md`
§3a):

| Gap | Module | What it does in silicon |
|-----|--------|--------------------------|
| 1 | `redteam_filter` | Combinational 5-detector adversarial-input screen (fuel deception, action exhaustion, timeline manipulation, resource poisoning, proof-trace overflow) |
| 2 | `k3_alu` | Native Kleene K3 ternary ALU — NOT, AND=min, OR=max over {F, U, T} as exhaustive truth tables |
| 3 | `datalog_engine_mini` | Forward-chaining Datalog (Horn clauses), least-fixed-point convergence detection |
| 4 | `restraint_ctrl` | Bounded-rationality safety gate — sticky `force_unknown` on φ-drift / step-overflow / receipt-failure |
| 5 | `explainability_unit` | On-chip proof-trace buffer of 20-bit 5-tuples (step, premise A, premise B, rule, conclusion), MAX_STEPS=10 |
| 6 | `asp_solver_mini` | Answer-Set Programming with negation-as-failure, stable model via the TP operator |
| 7 | `composition_kernel` | Glass-box composition supervisor sequencing Gap-3 → Gap-4 → Gap-5 with observable intermediate state |
| 8 | `proof_trace_writer` | CRC-32 receipt over the 10-step proof payload, emitted as a serial, off-chip-checkable artefact |
| 9 | `sat_solver_mini` | DPLL 3-CNF SAT (8 vars × 16 clauses) — propagation, decision, bounded backtrack |
| 10 | `audit_log_ring_buffer` | 64-entry forensic event log with sequential host dump |

A standing engineering invariant (R-SI-1) forbids multiply (`*`)
operators in the synthesized RTL, which keeps the netlist auditable;
every primitive above is XOR/AND/OR/compare logic.

The Coq theorems backing these gaps (e.g. the MAX_STEPS bound) live in a
separate, referenced repository (`gHashTag/trinity-clara/theorems/`); we
disclose that per-module hardware (cocotb) coverage for Gaps 1/3/6/9 and
the end-to-end composition test are still open work, and we label those
items as empirical-fit / open-conjecture rather than verified.

## 3. Why Galois-Field numeric formats in silicon

The reasoning primitives operate over finite fields (GF(2⁴)=GF16, plus a
GF4–GF256 portfolio) rather than floating point. The argument is an
engineering one about *verifiability per unit of silicon*:

- GF arithmetic is **exact and closed** — no rounding, no denormals — so a
  result is reproducible bit-for-bit. [Verified — standard finite-field
  algebra; the same GF(2⁸) arithmetic underlies FIPS-197/AES.]
- GF16 multiply is **table-free and single-cycle** in our datapath.
  [Measured in simulation.]
- The compact, multiply-free logic keeps area small enough to fit all ten
  gaps on a shuttle tile. [Empirical fit.]

We explicitly do **not** claim that finite-field arithmetic is physically
or mathematically privileged for AI in general, nor that GF-in-silicon is
required by CLARA. Silicon *extends* the glass-box property to the gate
level; it does not substitute for the algorithm-level AR proofs, and it is
not a CLARA deliverable. Full rationale and the "what we do not claim"
list are in `HARDWARE-REALIZATION-TRINET.md` §3b.

## 4. On the cross-die anchor `0x47C0`

All three companion dies are designed to emit a 16-bit value `0x47C0` on
the `{uio_out, uo_out}` bus at power-on reset, computed on-die from the
φ-structured GF16 constant. We present this as an **engineering
build-provenance fingerprint and a deterministic power-on self-test —
not as a mathematical proof** binding the dies, and not as scientific
evidence about φ. A reviewer with a returned die can measure the bus
after reset; any value ≠ `0x47C0` would refute the shared-provenance
claim for that die. Until dies return and an external party measures the
bus, this is private, single-source provenance, and it is used nowhere in
our quantitative claims.

## 5. What we are offering

Everything is open-source under Apache-2.0, consistent with CLARA's
mandatory open-source posture:

- **Euler RTL (all 10 gaps):** https://github.com/gHashTag/tt-trinity-euler
- **Gap-to-module traceability:** `CLARA_TRACEABILITY.md` in that repo
- **Hardware realization write-up:** `submission/HARDWARE-REALIZATION-TRINET.md`
  in https://github.com/gHashTag/trinity-clara
- **Software/RTL archive (DOI):** 10.5281/zenodo.19227877 — a Zenodo
  software/RTL archive and provenance handle, *not* a peer-reviewed proof
  source.

We would welcome any feedback the program is able to share, and we are
happy to provide measured bus values and per-module test results once the
fabricated dies return (est. December 2026).

Thank you for your time and for the clarity of the CLARA glass-box
framing, which directly shaped this design.

Respectfully,

Dmitrii Vasilev
admin@t27.ai
TRINITY / TRI-NET

---

### Internal notes (remove before any send)

- **Honesty checklist passed:** no "proves" on the anchor; dies not yet
  returned is stated; 256-vs-16 spec/silicon distinction is in the
  hardware doc; external/Admitted theorem status disclosed; no AGI /
  prize / breakthrough language; GF-in-silicon framed as extension, not a
  CLARA requirement.
- **Do not assert acceptance or an award.** The submission windows are
  closed; this is an update/contribution, not a bid.
- **Contact:** CLARA@darpa.mil is the published program inbox. PM is
  Dr. Benjamin Grosof (DSO). Confirm current routing before sending.
- **English-only artefact** (per project language policy).
