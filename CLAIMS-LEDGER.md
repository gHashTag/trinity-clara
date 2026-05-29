<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# TRINITY CLARA — Single Source of Truth: Claims Ledger

**Purpose.** This ledger is the **single source of truth (SSOT)** for every quantitative or
verifiable claim made anywhere in the TRINITY CLARA submission package. It is modeled on the
claim-status discipline already used in the companion repository
[`trinity-s3ai`](https://github.com/gHashTag/trinity-s3ai) (`claims.yaml`, 5-status vocabulary,
anti-numerology gate). No document in this package may assert a number that is not registered
here with an explicit status and an artifact reference.

**Why this exists.** DARPA-class review rewards epistemic honesty over polish. A reviewer who
finds the *same* metric reported with two different values in two documents will discount the
*entire* package. This ledger eliminates that failure mode by forcing one canonical value per
claim and labeling each with its evidentiary status.

---

## Status vocabulary

| Status | Meaning | Allowed evidence |
|--------|---------|------------------|
| `PROVEN` | Machine-checked formal proof (`Qed.` in Coq/Lean) | Proof file + theorem name |
| `MEASURED` | Empirically measured on real hardware/software | Run log, board, instrument |
| `SIMULATED` | Result of software simulation / RTL testbench, **not** silicon | Testbench, sim script |
| `SYNTHETIC` | Result on a synthetic / generated dataset, not real-world data | Dataset generator + seed |
| `PROJECTED` | Engineering projection / target, not yet observed | Method + assumptions |

Any sentence in any package document that states a number **must** carry the matching status tag
(e.g. "94.2% accuracy `[SYNTHETIC]`") or link back to the row ID below.

---

## A. Formal verification claims

| ID | Claim | Canonical value | Status | Authoritative source | Notes / correction |
|----|-------|-----------------|--------|----------------------|--------------------|
| F-1 | Total machine-checked theorems across the Trinity program | **1,325 `Qed.` theorems** (in `trinity-s3ai`) | `PROVEN` | [trinity-s3ai README / `proofs/`](https://github.com/gHashTag/trinity-s3ai) | The "84 Coq theorems" figure used in the proposal refers **only** to the CLARA math-core subset (φ identities, physics constants). State both numbers, never conflate them. |
| F-2 | CLARA math-core theorems (φ identities, constants) | **84 theorems**, 13/13 files compile | `PROVEN` | `t27` proofs, `proofs/igla/` | Do **not** describe these 84 as proving "ML+AR composition." They prove the mathematical core only. |
| F-3 | ML+AR composition correctness | **Not formally proven** | `SIMULATED` | `.t27 → Verilog` lowering + RTL testbench | Verified by semantic-preservation lowering and simulation, **not** by a Coq proof. Must be stated as such. |
| F-4 | Cross-die anchor `{uio_out,uo_out}=0x47C0` on reset (Theorem 36.1) | Holds on all 3 tiers in simulation | `SIMULATED` | tt-trinity-phi/euler/gamma sim | Silicon validation pending shuttle return (~Nov 2026). |
| F-5 | R-SI-1 invariant (zero standalone `*` in synthesis RTL) | Passes on every commit | `MEASURED` (CI) | CI workflow `R-SI-1 no-star check` | CI is real and measurable; keep. |

## B. Adversarial robustness / Red Team claims

| ID | Claim | Canonical value | Status | Authoritative source | Notes / correction |
|----|-------|-----------------|--------|----------------------|--------------------|
| R-1 | Adversarial variants blocked (Red Team) | **96% (48/50)**, recovery 7.2 ms avg | `SYNTHETIC` | `examples/05_redteam_test.py`, 100-scenario synthetic set | **CONFLICT TO FIX:** Executive Summary currently says "100% robustness, 0% false positives." That is inconsistent with the 48/50 empirical result. Adopt **96% (48/50)** everywhere; drop all "100%" robustness wording. |
| R-2 | Red Team target | **≥95% (planned target)** | `PROJECTED` | Technical Proposal §4.6 | Keep as a *target*, clearly separated from the 96% observed value. |
| R-3 | Attack categories covered | **5** (fuel deception, action exhaustion, timeline, resource poisoning, proof-trace) | `SYNTHETIC` | `CLARA-RED-TEAM.md` | Category count is fine; only the success rate is in conflict. |

## C. Application-performance claims

| ID | Claim | Canonical value | Status | Authoritative source | Notes / correction |
|----|-------|-----------------|--------|----------------------|--------------------|
| P-1 | COA-planning decision accuracy | **94.2% (94/100)** | `SYNTHETIC` | Technical Proposal §4.7, synthetic COA dataset | Must be tagged `[SYNTHETIC]`; it is **not** a real-world or fielded result. |
| P-2 | Decision latency | avg 2.3 ms, max 4.7 ms | `SIMULATED` | §4.7 | Tag as simulation result. |
| P-3 | Explanation length | 7.2 steps avg (all ≤10) | `SYNTHETIC` | §4.7 | CLARA ≤10-step constraint satisfied. |

## D. Hardware / energy claims

| ID | Claim | Canonical value | Status | Authoritative source | Notes / correction |
|----|-------|-----------------|--------|----------------------|--------------------|
| H-1 | Energy efficiency vs GPU | **49×** on legacy FPGA (XC7A100T @ 92 MHz vs Jetson Orin baseline) | `MEASURED` (prototype) | §8.5 methodology | Keep the *methodology* sentence attached every time the number appears; never quote "49×" bare. |
| H-2 | Throughput | 63 tok/s @ 1.2 W (19 mJ/token) | `MEASURED` (prototype) | §8.5 | OK with board + clock stated. |
| H-3 | Euler ternary core performance | ~1 GOPS @ ~50 MHz @ ~1 W | `PROJECTED` | Hardware addendum | Already labeled "projected" in README; enforce that label in all docs. |
| H-4 | 10 CLARA gaps in open silicon (Euler #4915) | All 10 → Verilog modules, submitted TTSKY26b | `SIMULATED` (pre-silicon RTL) | HARDWARE-REALIZATION-TRINET.md | RTL + GDS submitted; **physical silicon not yet returned**. Say "submitted to shuttle / pre-silicon," not "realized in silicon" without that qualifier. |

## E. Composition / coverage claims

| ID | Claim | Canonical value | Status | Authoritative source | Notes / correction |
|----|-------|-----------------|--------|----------------------|--------------------|
| C-1 | ML+AR composition patterns | **4 demonstrated** (CNN+Rules, MLP+Bayesian, Transformer+XAI, RL+Guardrails); up to **7 specified** in `composition.t27` | `SIMULATED` | `specs/ar/composition.t27` | **CONFLICT TO FIX:** "4/4" and "7 patterns" are used interchangeably. Standardize: **"4 demonstrated, 7 specified."** Never write a bare "7 patterns demonstrated." |
| C-2 | AR specification modules | **8/8 complete**, 93 tests, 19 invariants | `SIMULATED` | Evidence package | OK; keep test/invariant counts consistent. |
| C-3 | Numeric format coverage | ~30 at submission → **66** post-submission | `SIMULATED` | NeuronConstant addendum | Scope note: this belongs to the **follow-on** track, not core CLARA TA1/TA2 (see DePIN addendum). |

---

## F. Complexity-claim corrections

| ID | Original wording | Problem | Corrected wording |
|----|------------------|---------|-------------------|
| X-1 | "Theorem 4: Bounded ASP Executes in O(1) Constant Time" | ASP is NP-hard; "O(1)" is not a meaningful complexity class for it. Fixed array bounds do not change the complexity *class* — they cap input size. | "Bounded-ASP termination: TRINITY restricts ASP to a fixed fragment (MAX_CLAUSES=256, MAX_ITERATIONS=1000) that is **guaranteed to terminate in a bounded number of steps**. We make no claim about the asymptotic complexity class of general ASP, which remains NP-hard." |

---

## Enforcement

1. Every numeric claim in `README.md`, `proposal/`, `submission/`, `evidence/`, and `docs/`
   must map to a row above and carry the matching status tag.
2. CI check (recommended): grep for the regex `100% robust` and fail the build — that value is
   retired (see R-1).
3. When a value changes, update **this file first**, then propagate. This file wins all conflicts.

*Last updated: 2026-05-29. Maintained as the SSOT for the TRINITY CLARA submission package.*
