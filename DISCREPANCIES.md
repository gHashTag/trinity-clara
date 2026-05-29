<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# TRINITY CLARA — Internal Discrepancy Audit

**Date:** 2026-05-29
**Scope:** Cross-document consistency audit of the TRINITY CLARA submission package
(`README.md`, `proposal/`, `submission/`, `evidence/`, `docs/addendum/`).

This is a reviewer-facing punch list of internal contradictions and integrity risks found in the
package. Each item references the canonical resolution in [`CLAIMS-LEDGER.md`](CLAIMS-LEDGER.md).
Severity reflects how a DARPA technical reviewer is likely to weigh the issue.

Legend: 🔴 blocker (likely triggers rejection / loss of trust) · 🟠 major · 🟡 minor / polish.

---

## 🔴 D-1 — Red Team success rate contradicts itself

| Where | What it says |
|-------|--------------|
| `submission/EXECUTIVE-SUMMARY.md` (Differentiation #1) | "Red Team protocol achieves **100% robustness** against 5 adversarial categories" |
| `submission/EXECUTIVE-SUMMARY.md` (Compliance, TA1) | "Red Team Protocol: **100% robustness** (5 categories, **0% false positives**)" |
| `submission/EXECUTIVE-SUMMARY.md` (Innovation table) | "5-category Red Team protocol with **100% success**" |
| `proposal/CLARA-PROPOSAL-TECHNICAL.md` §4.6 | "Red Team Evaluation Protocol targeting **≥95% robustness** (planned for Phase 2)" |
| `proposal/CLARA-PROPOSAL-TECHNICAL.md` §4.7 | "Adversarial Robustness: **96%** adversarial variants blocked (**48/50**)" |

**Problem.** The same capability is reported as 100%, ≥95% (target), and 96% (48/50 measured) in
one package. 100% and 48/50 are mutually exclusive. This is the single highest-risk integrity
issue: a reviewer who notices it will distrust every other number.

**Fix (per ledger R-1/R-2).** Use **"96% (48/50) on a synthetic dataset; ≥95% is the Phase-2
target"** everywhere. Delete all "100% robustness" and "0% false positives" wording from the
Executive Summary and Innovation table.

---

## 🔴 D-2 — "84 Coq theorems" oversells what is formally proven

| Where | What it says |
|-------|--------------|
| `submission/EXECUTIVE-SUMMARY.md` | "**84 Coq theorems** — Most comprehensive formal verification … from .t27 to Verilog" |
| `proposal/CLARA-PROPOSAL-TECHNICAL.md` §4 | 84 theorems verify the **mathematical core**; ML+AR composition is verified "via .t27→Verilog semantic preservation" |
| `trinity-s3ai` README | "**1,325 theorems with `Qed.`**" |

**Problem.** Two issues at once: (a) the package's own changelog admits the 84 cover the *math
core only*, yet the Executive Summary implies they verify the full `.t27→Verilog` ML+AR path;
(b) the companion repo proves **1,325** theorems, so "84 = most comprehensive" understates the
program and invites a "which number is real?" question.

**Fix (per ledger F-1/F-2/F-3).** State: "**2,027 machine-checked `Qed.` theorems, 0 real
`Admitted.`, across 100 `.v` files** in the Trinity program (`trinity-s3ai`, reproducible via
`scripts/count_admitted_honest.py`, 2026-05-29); the CLARA math-core is the `t27/proofs/trinity/`
set (132 `Qed.`, 32 `Admitted.`). ML+AR composition is verified by `.t27→Verilog` lowering and
RTL simulation — **not** by a formal proof."

**Update 2026-05-29 (s3ai fact-sync).** The program-wide figure is now anchored to the
`trinity-s3ai` honest counter output (2,027 `Qed.`), **not** the README headline. The
`trinity-s3ai` README is itself internally inconsistent — it carries both "1,325" and "1,762"
`Qed.`; both are stale snapshots superseded by the reproducible 2,027 machine count. Ledger F-1
updated accordingly. (Historical "1,325"/"84" strings above are retained for the audit trail.)

---

## 🟠 D-3 — Composition pattern count: 4 vs 7

| Where | What it says |
|-------|--------------|
| `submission/EXECUTIVE-SUMMARY.md` (TA2 compliance) | "Composition Patterns: **4/4** demonstrated" |
| `submission/EXECUTIVE-SUMMARY.md` (AR specs list) | "Composition — **7** ML+AR patterns" |
| `submission/EXECUTIVE-SUMMARY.md` (Innovation table) | "**7** composition patterns with formal guarantees" |
| `README.md` | "`composition.t27` … (**7 patterns**)" and elsewhere "**4/4** patterns demonstrated" |
| `proposal/CLARA-PROPOSAL-TECHNICAL.md` | "**4 ML+AR patterns**" / "`composition.t27` (622 lines)" |

**Problem.** "4" and "7" are used interchangeably for the same artifact, sometimes on the same
page. Reviewers read this as careless or inflated.

**Fix (per ledger C-1).** Standardize to: **"4 patterns demonstrated; up to 7 specified in
`composition.t27`."** Never write a bare "7 patterns demonstrated."

---

## 🟠 D-4 — "Realized in silicon" vs pre-silicon RTL

| Where | What it says |
|-------|--------------|
| `README.md` addendum | "All 10 CLARA gaps … **realized in open-RTL silicon**" |
| Hardware addendum | RTL + GDS **submitted** to TTSKY26b shuttle (closed 2026-05-19) |

**Problem.** The chips are submitted to a shuttle; physical dies have not returned. "Realized in
silicon" without the "open-RTL / pre-silicon / submitted" qualifier overstates maturity.

**Fix (per ledger H-4).** Always qualify: "implemented in **open-source RTL** and **submitted**
to the TTSKY26b shuttle; physical silicon validation pending (~Nov 2026)."

---

## 🟠 D-5 — Theorem 4 misuses complexity notation

**Where.** `proposal/CLARA-PROPOSAL-TECHNICAL.md` §3, "Theorem 4: Bounded ASP Executes in O(1)
Constant Time."

**Problem.** ASP is NP-hard. Capping the input with `MAX_CLAUSES=256` bounds the *problem size*;
it does not place ASP in O(1). A formal-methods reviewer will flag this immediately, and it
contradicts the package's own claim to rigorous Big-O proofs.

**Fix (per ledger X-1).** Reframe as a **bounded-termination** guarantee, not a complexity-class
claim. See replacement text in this PR's edit to the Technical Proposal.

---

## 🟠 D-6 — Energy/accuracy numbers presented as fact without status tags

| Claim | Reported as | Actual status |
|-------|-------------|---------------|
| 94.2% accuracy | flat fact | `SYNTHETIC` (100 generated scenarios) |
| 49× energy efficiency | headline differentiator | `MEASURED` on legacy FPGA, only with §8.5 methodology |
| 1 GOPS @ 50 MHz | performance claim | `PROJECTED` |

**Problem.** The companion repo `trinity-s3ai` tags every claim (measured/simulated/projected).
The CLARA package drops these tags, which reads as less rigorous than your own public standard.

**Fix (per ledger P-1/H-1/H-3).** Attach the status tag (and, for 49×, the measurement
methodology) every time the number appears.

---

## 🟡 D-7 — Scope creep from the DePIN addendum

**Where.** `docs/addendum/CLARA-DEPIN-ADDENDUM-2026-05.md` (66 numeric formats, ZK
proof-of-training, mesh routing, $TRI token, 12 "moats").

**Problem.** CLARA TA1/TA2 is about *verifiable AR+ML*. DePIN substrate, token economics, and
mesh routing dilute that focus and can read as off-scope to a CLARA reviewer.

**Fix.** Keep the addendum, but frame it explicitly as **follow-on positioning (RACE/OPTIMA/AIE)**
and add a one-line scope guard at the top: "Nothing in this addendum is part of the CLARA TA1/TA2
deliverable scope." Keep the core package strictly TA1/TA2.

---

## 🟡 D-8 — README cosmetic defects

- Badge alt-text rendered with `printf`-style artifacts in some checkouts (`Apache%!`,
  `Submission%!Ready`) — verify the raw markdown badge URLs encode spaces as `%20`.
- The "Status" badge links to an `img.shields.io` image URL instead of a meaningful page.

**Fix (per ledger, polish).** Normalize badge URLs; point the Status badge at the submission
package or the ledger.

---

## 🟡 D-9 — Key Personnel section is corrupted and off-target

**Where.** `submission/EXECUTIVE-SUMMARY.md`, "Key Personnel."

**Problem.** Publication entry #3 is a concatenation of unrelated fragments (FPGA milestone-table
text spliced into a citation: "…M3-M12 | FPGA verification backend … 5,279 pp."). Several
publications repeat with conflicting page ranges. The overall profile (philosophy of religion,
golden-ratio numerology) is weakly matched to DARPA TA1/TA2 and conflicts with the program's own
**anti-numerology gate** in `trinity-s3ai`.

**Fix.** Replace with a clean, defensible personnel section (see this PR's rewrite). Present φ as
an *engineering* numeric-format choice (GF16), not as a metaphysical "secret of the universe."

---

## 🔴 D-10 — Authorship contradiction ("sole author" vs three-person PI/Co-I team)

**Where.** `proposal/CLARA-PROPOSAL-TECHNICAL.md`, `submission/HARDWARE-REALIZATION-TRINET.md` (×3),
`submission/EXECUTIVE-SUMMARY.md`, `submission/KEY-PERSONNEL-REWRITE.md` vs `README.md` /
`submission/CLARA-SUBMISSION-PACKAGE.md` / `proposal/CLARA-COST-PROPOSAL.md`.

**Problem.** The package simultaneously said "sole author: Dmitrii Vasilev" (×5) and named a
three-person team (PI Dr. Scott A. Olsen + Co-I Vasilev + Co-I Dr. Stergios Pellis). A reviewer
could not tell who the PI is; "sole author" also contradicts the budgeted cost proposal.

**Fix (RESOLVED 2026-05-29).** Adopt the **contribution-based three-person model** — Olsen (PI,
golden-mean theory / book grounding), Vasilev (Co-I, own φ-formulas + t27 framework + GF16 +
TRI-NET silicon), Pellis (Co-I, phenomenological formulas). All "sole/single author" strings
retired; "original work of D. Vasilev" kept only for the RTL/proof artifacts. Single email
`admin@t27.ai`. See ledger **A-1** and `PROJECT-AUDIT.md` A-1.

---

## 🟠 D-11 — Coq toolchain version stated four different ways

**Where.** `README.md` ("Rocq 9.1.1"), `proposal/CLARA-PROPOSAL-TECHNICAL.md` ("Coq 9.1.1"),
`REPRODUCIBILITY.md` / `submission/HARDWARE-REALIZATION-TRINET.md` ("Coq 8.19+ / Rocq 9.0+"), vs
the CI gate which pins **`coqorg/coq:8.20.1`**.

**Problem.** A reviewer who clones and builds hits an immediate version mismatch; no Rocq 9.1.1
build exists in this repo.

**Fix (RESOLVED 2026-05-29).** State the build floor ("Coq 8.19+") together with the
CI-verified container ("machine-checked in CI under `coqorg/coq:8.20.1`"). The bare "9.1.1"
claims are retired. See ledger **V-1**.

---

## Summary table

| ID | Severity | Issue | Resolution owner |
|----|----------|-------|------------------|
| D-1 | 🔴 | Red Team 100% vs 96% vs ≥95% | Ledger R-1/R-2 |
| D-2 | 🔴 | "84 Coq" oversold vs 1,325; conflated with composition | Ledger F-1/F-2/F-3 |
| D-3 | 🟠 | Composition patterns 4 vs 7 | Ledger C-1 |
| D-4 | 🟠 | "Realized in silicon" vs submitted RTL | Ledger H-4 |
| D-5 | 🟠 | Theorem 4 O(1) misuse | Ledger X-1 |
| D-6 | 🟠 | Missing status tags on key numbers | Ledger P-1/H-1/H-3 |
| D-7 | 🟡 | DePIN scope creep | Scope guard |
| D-8 | 🟡 | README badge defects | Polish |
| D-9 | 🟡 | Corrupted / off-target Key Personnel | Rewrite |
| D-10 | 🔴 | "Sole author" vs three-person PI/Co-I team | Ledger A-1 (RESOLVED) |
| D-11 | 🟠 | Coq version stated 4 ways vs CI 8.20.1 | Ledger V-1 (RESOLVED) |

*Audit maintained alongside [`CLAIMS-LEDGER.md`](CLAIMS-LEDGER.md), the package SSOT.*
