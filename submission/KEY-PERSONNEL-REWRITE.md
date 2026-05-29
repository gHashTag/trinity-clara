<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# Key Personnel (replacement for EXECUTIVE-SUMMARY.md § "Key Personnel")

> **Why this rewrite.** The previous Key Personnel section contained a corrupted publication
> entry (FPGA milestone-table text spliced into a citation), duplicated publications with
> conflicting page ranges, and a profile weighted toward golden-ratio metaphysics — which
> conflicts with the program's own anti-numerology gate in `trinity-s3ai`. This version presents
> a clean, defensible team description aligned to DARPA TA1/TA2 (Argumentation & Reasoning /
> Composition). **Bracketed fields are placeholders — fill with verified facts before
> submission.** Do not ship any unverifiable claim.

---

## Principal Investigator

**Name:** Dmitrii Vasilev
**Role:** Principal Investigator / Lead Architect, TRINITY S³AI
**Affiliation:** [organization / independent researcher]
**Contact:** admin@t27.ai

**Relevance to CLARA.** Sole author and maintainer of the open-source TRINITY stack that
constitutes the technical substance of this proposal, including:

- The `.t27` specification language and its lowering path to synthesizable Verilog
  ([`t27`](https://github.com/gHashTag/t27)).
- The formal-verification corpus — **1,325 machine-checked `Qed.` theorems** across the program
  ([`trinity-s3ai`](https://github.com/gHashTag/trinity-s3ai)), of which 84 constitute the CLARA
  math-core, developed under an explicit **anti-numerology / claim-status discipline**.
- The three open-silicon RTL designs (Φ/Ε/Γ) submitted to the TinyTapeout TTSKY26b shuttle,
  with the Euler tier implementing all 10 CLARA safety gaps as Verilog modules
  (DOI [10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877), Apache-2.0).

This is direct, demonstrable, reproducible evidence of the exact engineering capability the
CLARA TA1/TA2 effort requires: formal AR specs → verified composition → open hardware.

---

## Proposed Team Structure (to be staffed under award)

The cost proposal budgets a team; the following roles map personnel to CLARA deliverables. Named
hires are to be confirmed at award; the PI covers all roles in the current prototype.

| Role | CLARA responsibility | Required expertise |
|------|----------------------|--------------------|
| PI / Lead Architect | Overall direction, `.t27→Verilog` semantics, DARPA coordination | Formal methods, ternary/neuro-symbolic systems |
| AR / Logic Researcher (×2) | Datalog/ASP/K3 engines, Coq proofs, composition formalization | Automated reasoning, Coq/Lean, Horn-clause semantics |
| ML / Neural Researcher (×2) | Neural + Bayesian + RL components, polynomial-bound analysis | Neuro-symbolic ML, complexity analysis, benchmarking |
| Systems Engineer (×1) | FPGA prototype, RTL CI, reproducibility kit | RTL/FPGA toolchains, CI, open-silicon flow |

---

## Theoretical grounding (stated as engineering, not metaphysics)

TRINITY's use of the constant φ is an **engineering numeric-format decision**, not a metaphysical
claim. The GF16 (DLFloat-6:9) format exploits the algebraic identity **φ² + φ⁻² = 3** to obtain a
well-conditioned ternary-friendly encoding with a wide dynamic range. The benefit is quantified
and falsifiable: format error, dynamic range, and accuracy-vs-float are reported as benchmarks
with explicit status tags (see `CLAIMS-LEDGER.md`). No claim is made that φ "explains" any
physical phenomenon; the companion repository `trinity-s3ai` enforces this boundary with an
automated **anti-numerology gate** and a 5-status claim ledger.

This framing is deliberate: it aligns the personnel narrative with the same epistemic standard
the codebase already enforces, and removes the single most attackable element of the prior draft.

---

## Selected supporting artifacts (in lieu of unverifiable publication list)

Rather than a publication list, the strongest credential for this proposal is the **reproducible
artifact trail**, which a reviewer can independently verify:

1. `git clone https://github.com/gHashTag/t27 && cd proofs && make` → 13/13 files compile, 84
   math-core theorems `[PROVEN]`.
2. [`trinity-s3ai`](https://github.com/gHashTag/trinity-s3ai) — 1,325 `Qed.` theorems, honest
   claim ledger, documented boundary theorems (BT-1..BT-4) and refutations `[PROVEN]`.
3. Euler RTL (TinyTapeout #558) — 10 CLARA gaps as Verilog modules, green `gds` CI
   `[SIMULATED]`, submitted to TTSKY26b shuttle.
4. DOI [10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877) — archived RTL
   snapshots and gate-level netlists, Apache-2.0.

> **Action before submission:** if a co-PI or named academic collaborator will be on the award,
> add their verified CV here (degrees, affiliation, peer-reviewed publications with correct,
> non-duplicated citations). Remove any entry that cannot be independently verified.
