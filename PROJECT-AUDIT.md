<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# TRINITY CLARA — Project Anomaly Audit (Wave 2)

**Date:** 2026-05-29
**Auditor scope:** Whole submission package + cross-references to companion repos
(`t27`, `trinity-s3ai`, `NeuronConstant`, `tt-trinity-*`).
**Standard applied:** TRIOS operating rules — claim-status framing (Verified / Empirical fit /
Open conjecture / High-risk / Retracted), anti-numerology gate, no prize/absolute claims as
deliverables, English-only public artefacts, and the Track-1 finding that **no peer-reviewed
publication exists under TRINITY / S³AI / GOLDEN BRIDGE as of 2026-05-29** — therefore every
algorithmic/empirical claim without an external DOI is **capped at "Open conjecture."**

This is the adversarial "what would a hostile reviewer attack?" pass. Items are ordered by how
fast they would sink the proposal. Resolution of D-1..D-9 is tracked in
[`DISCREPANCIES.md`](DISCREPANCIES.md); this file adds the deeper structural anomalies A-1..A-12.

Severity: 🔴 fatal (kills credibility) · 🟠 major · 🟡 minor.

---

## 🔴 A-1 — Authorship is internally contradictory (THREE incompatible models)

The package simultaneously asserts three mutually exclusive authorship stories:

| Source | Claim |
|--------|-------|
| `proposal/CLARA-PROPOSAL-TECHNICAL.md` L196 | "**Sole author:** Dmitrii Vasilev <admin@t27.ai>" |
| `submission/HARDWARE-REALIZATION-TRINET.md` | "**Sole Author:** Dmitrii Vasilev" (×3) |
| `submission/EXECUTIVE-SUMMARY.md` L166 | "**Principal Investigator:** Scott A. Olsen, Ph.D." |
| `README.md` L326 / `submission/CLARA-SUBMISSION-PACKAGE.md` L44 | "**Co-Investigator** — Dmitrii Vasilev" |

A reviewer cannot tell who the PI is. "Sole author" and "Co-Investigator under a different PI"
cannot both be true. **This is the single most damaging anomaly** — it undermines the cost
proposal (which budgets 2 PIs + 4 researchers), the personnel section, and basic trust.

**Plus:** two different contact emails for the same person — `admin@t27.ai`
(proposal/hardware) vs `bayotkwolpep9c@hotmail.com` (DePIN addendum L239).

**Fix.** Decide one authorship model and propagate it everywhere. Recommended: a single named
PI with a clearly-labelled, *staffed-at-award* team (the cost proposal already implies this).
Pick **one** canonical contact email. See `submission/KEY-PERSONNEL-REWRITE.md`.

---

## 🔴 A-2 — Fabricated / swapped bibliography citations

`proposal/CLARA-PROPOSAL-TECHNICAL.md` Bibliography:

| Ref | As printed | Reality (verified) |
|-----|-----------|--------------------|
| [4] | "Manhaeve, R. et al. (2018). *CTSketch: Deep Compositional Reasoning.* NeurIPS 2018." | **CTSketch** = Choi, Solko-Breslin, Alur, Wong, *Compositional Tensor Sketching for Scalable Neurosymbolic Learning*, **NeurIPS 2025** ([arXiv:2503.24123](https://arxiv.org/abs/2503.24123)). Not Manhaeve, not 2018, not that title. |
| [5] | "Liang, P. et al. (2018). *DeepProbLog: Simple Differentiable Logic.* NeurIPS 2018." | **DeepProbLog** = Manhaeve, Dumančić, Kimmig, Demeester, De Raedt, *Neural Probabilistic Logic Programming*, **NeurIPS 2018** ([proceedings](https://proceedings.neurips.cc/paper_files/paper/2018/hash/dc5d637ed5e62c36ecb73b654b05ba2a-Abstract.html)). Wrong author (Liang), wrong title. |
| [6] | "REASON Team (2026). … arXiv:2601.20784." | Unverifiable — no such arXiv ID resolves. Anonymous "Team" author. |

**Why fatal.** A DARPA technical reviewer is a domain expert. Citing DeepProbLog with the wrong
author and inventing a CTSketch attribution is the kind of error that triggers an integrity
review. The 94.2% accuracy comparison "vs DeepProbLog (95.1%)" also has **no citation for the
95.1% figure** — it appears to be invented.

**Fix.** Correct [4] and [5] to the verified citations above; remove or replace [6] with a real
source; either cite a real DeepProbLog benchmark number or delete the "95.1%" comparison.

---

## 🔴 A-3 — Absolute claims forbidden by the project's own rules

The TRIOS claim-status rule bans hype and absolute guarantees as deliverables. The package is
saturated with them:

- "**100%** Red Team success" / "**100%** robustness, **0% false positives**" (already in D-1).
- "**Most comprehensive** formal verification" (README, Exec Summary) — unprovable superlative.
- "**Unique among SOA systems**" / "**NONE** provide … robustness" — absolute negative claim
  about all competitors, undefendable.
- "**Guaranteed** Polynomial Bounds" + "**formal correctness guarantees**" for ML+AR — but
  composition is `[SIMULATED]`, not proven (F-3). Per Track-1, no external DOI ⇒ **Open
  conjecture**, so "guarantee" is disallowed.
- "**World's first** hardware implementation of all 10 CLARA gaps" — defensible *only* with the
  "open-RTL, submitted to shuttle, pre-silicon" qualifier (A-7).

**Fix.** Replace superlatives with claim-status-tagged, falsifiable statements. Example:
"Among the 10 neuro-symbolic systems we surveyed (table X), none documented a formal adversarial
guardrail [Empirical fit, survey-bounded]" instead of "unique among SOA systems / none provide."

---

## 🟠 A-4 — Energy figure: 42× vs 49× used interchangeably

`42×` appears in `evidence/CLARA-SCALING.md`, `CLARA-IMPROVEMENTS-SUMMARY.md`, and as the
"target" in §8.5; `49×` appears in 14+ other places as the "measured" value — including **twice
in the same §8.5 paragraph** ("target: 42×" then "= 49× improvement"). A reviewer reading the
methodology section sees the proposal contradict itself within one paragraph.

**Fix.** State once: "**target 42×; measured 49×** on legacy XC7A100T @ 92 MHz vs Jetson Orin
baseline [MEASURED, prototype]." Use that exact phrasing everywhere (ledger H-1).

---

## 🟠 A-5 — "84 theorems verify … compositional integrity" overreaches (links to D-2)

§4 L130: "84 Coq theorems verify mathematical core … ML+AR composition verified via .t27→Verilog
… **where 84 theorems establish foundational mathematical correctness and compilation ensures
compositional integrity**." Compilation success is **not** verification of compositional
correctness — it only means the files type-check. This conflates "compiles" with "proven."

**Fix.** "13/13 files compile [MEASURED]; 84 theorems prove the math core [PROVEN]; composition
correctness is checked by simulation, not proof [SIMULATED]."

---

## 🟠 A-6 — φ presented as metaphysics, not engineering (anti-numerology violation)

The Key Personnel and "Basis for Confidence" sections lean on golden-ratio metaphysics ("Nature's
Greatest Secret", "Divine Proportion", "Grand Unification … Consciousness"). The companion repo
`trinity-s3ai` runs an **anti-numerology gate** precisely to keep this out of public artefacts.
Shipping numerology in a DARPA proposal while your own CI rejects it is an exploitable
inconsistency.

**Fix.** Reframe φ strictly as the GF16 numeric-format design choice with the algebraic identity
φ²+φ⁻²=3; report range/precision as benchmarks with status tags (handled in
`KEY-PERSONNEL-REWRITE.md`).

---

## 🟠 A-7 — "Realized in silicon" vs submitted RTL (also D-4)

README addendum: "all 10 … gaps … **realized in open-RTL silicon**." The chips were **submitted**
to the TTSKY26b shuttle; dies have not returned (~Nov 2026). Without the "pre-silicon / submitted"
qualifier this overstates TRL.

**Fix.** Always: "implemented in open-source RTL and submitted to TTSKY26b; physical-silicon
validation pending [SIMULATED→pending]."

---

## 🟠 A-8 — "65,000× wider dynamic range" / "1.8× more accurate" unsourced

These GF16 superlatives (README, API_REFERENCE, ARCHITECTURE) appear with no benchmark methodology
or comparison baseline in the public docs. "65,000×" against *what* float configuration? "1.8×
more accurate" on *what* task?

**Fix.** Either attach the benchmark (format, baseline, dataset, metric) with a `[MEASURED]` /
`[SIMULATED]` tag, or downgrade to a bounded, defensible statement.

---

## 🟠 A-9 — Empirical results are synthetic but read as fielded (also D-6)

94.2% accuracy, 96% robustness, 2.3 ms latency all come from a **100-scenario synthetic
generator**. They are presented in compliance tables ("TA1 — 100%") as if validated. Per Track-3
(FActScore/HaluEval framing), synthetic results must be labelled and must carry a
**falsification path**.

**Fix.** Tag every such number `[SYNTHETIC]`; add a one-line falsification path ("would be
disconfirmed if accuracy on a *real* COA dataset falls below X").

---

## 🟡 A-10 — Compliance sections claim "100%" coverage

"TA1 — 100%", "TA2 — 100%" headers assert complete compliance for a Phase-1 proposal whose own
schedule defers most ML+AR integration to Months 7–18. Claiming 100% now contradicts the roadmap.

**Fix.** Replace "TA1 — 100%" with "TA1 — Phase-1 requirements met; Phase-2 items scheduled
(M7–M18)."

---

## 🟡 A-11 — README cosmetic + count drift (also D-3, D-8)

- Badge alt-text artefacts (`Apache%!`, `Submission%!Ready`) in some renders.
- "7 patterns" vs "4/4 demonstrated" within the same README.
- Status badge links to a shields.io image instead of a meaningful page.

---

## 🟡 A-12 — No machine-checkable claim gate

There is currently nothing stopping a future edit from reintroducing "100% robustness" or an
untagged number. The companion repo enforces this in CI; this package does not.

**Fix.** Add `.github/workflows/claim-integrity.yml` (this PR) that fails the build on retired
strings and unsourced superlatives.

---

## Decomposed remediation plan

| Step | Anomaly | Action | Status in this PR |
|------|---------|--------|-------------------|
| 1 | A-2 | Fix bibliography [4]/[5]/[6]; remove invented 95.1% | ✅ applied |
| 2 | A-4 | Unify 42×/49× wording in §8.5 | ✅ applied |
| 3 | A-5 | Soften "compilation ensures compositional integrity" | ✅ applied |
| 4 | A-3/A-10 | Retire "100%/most comprehensive/unique" in README | ✅ applied |
| 5 | A-12 | Add claim-integrity CI gate | ✅ applied |
| 6 | D-7 | Scope-guard banner on DePIN addendum | ✅ applied |
| 7 | A-1 | Authorship reconciliation | ⏳ needs human decision (one PI + email) — flagged, not silently chosen |
| 8 | A-6/A-9 | φ-as-engineering + falsification paths | ✅ doc-level (KEY-PERSONNEL-REWRITE + ledger); full propagation = follow-up |
| 9 | A-8/A-11 | Source GF16 superlatives; badge cleanup | ⏳ follow-up (needs benchmark data) |

Items marked ⏳ require a human decision or data that must not be fabricated — per the rules,
they are flagged here rather than invented.

*Audit maintained alongside [`CLAIMS-LEDGER.md`](CLAIMS-LEDGER.md) (SSOT) and
[`DISCREPANCIES.md`](DISCREPANCIES.md).*
