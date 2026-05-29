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
| F-1 | Total machine-checked theorems across the Trinity program | program-wide `Qed.` theorems in `trinity-s3ai` (the often-quoted "1,325" is a program-wide figure; verify before quoting) | `PROVEN where Qed.` | [trinity-s3ai README / `proofs/`](https://github.com/gHashTag/trinity-s3ai) | Never conflate the program-wide figure with the CLARA math-core. Pair any count with its `Admitted` total. See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md). |
| F-2 | CLARA math-core proof base (φ identities, certified bounds) | The **`t27/proofs/trinity/`** set: 13 `.v` files, **110 theorems + 54 lemmas, 132 `Qed.`, 32 `Admitted`** (direct count 2026-05-29). Builds via `opam install coq coq-interval` → `coq_makefile -f _CoqProject` → `make`. | `PROVEN where Qed.` (32 lemmas honestly `Admitted`) | [`t27/proofs/trinity/`](https://github.com/gHashTag/t27), [Zenodo 10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877) | **The bare "84 theorems [PROVEN]" is RETIRED** — it matches no measured count and the project's own Zenodo archive records the VSA witness as "48 statements, 35 Proven, 0 Admitted." Do **not** describe this set as proving "ML+AR composition" (that is F-3, `SIMULATED`). Always disclose `Admitted`. |
| F-3 | ML+AR composition correctness | **Not formally proven** | `SIMULATED` | `.t27 → Verilog` lowering + RTL testbench | Verified by semantic-preservation lowering and simulation, **not** by a Coq proof. Must be stated as such. |
| F-4 | Cross-die anchor `{uio_out,uo_out}=0x47C0` on reset (Theorem 36.1) | Holds on all 3 tiers in simulation | `SIMULATED` | tt-trinity-phi (#198) / -euler (#558) / -gamma (#750) sim | Silicon validation pending shuttle return (est. delivery 2026-12-20 per registry; previously stated "~Nov 2026"). Project IDs verified: see H-5/H-6/H-7. |
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
| H-4 | 10 CLARA gaps in open silicon (Euler, TTSKY26b **#558**) | All 10 → Verilog modules, GDS submitted to TTSKY26b | `SIMULATED` (pre-silicon RTL) → `SUBMITTED` (to fab) | HARDWARE-REALIZATION-TRINET.md; [registry](https://tinytapeout.com/chips/ttsky26b/) | RTL + GDS submitted; **physical silicon not yet returned** (est. delivery 2026-12-20). Say "submitted to shuttle / pre-silicon," not "realized in silicon" without that qualifier. The Euler project ID is **#558**, NOT the retired fabricated "#4915" (see CHIP-PROVENANCE below). |
| H-5 | Φ Phi chip identity on TTSKY26b | Project **#198**, top module `tt_um_trinity_nano`, 1×1 tile | `Verified` (external registry) | [registry](https://tinytapeout.com/chips/ttsky26b/), [tt-trinity-phi](https://github.com/gHashTag/tt-trinity-phi) | Address confirmed against the live shuttle registry by submitter name "Dmitrii Vasilev," 2026-05-29. Retires fabricated "#4913." |
| H-6 | Ε Euler chip identity on TTSKY26b | Project **#558**, top module `tt_um_ghtag_trinity_gf16`, 8×2 tiles | `Verified` (external registry) | [registry](https://tinytapeout.com/chips/ttsky26b/), [tt-gf16-euler](https://github.com/gHashTag/tt-gf16-euler) | Confirmed against live registry 2026-05-29. Retires fabricated "#4915." |
| H-7 | Γ Gamma chip identity on TTSKY26b | Project **#750**, top module `tt_um_trinity_max_true`, 8×4 tiles | `Verified` (external registry) | [registry](https://tinytapeout.com/chips/ttsky26b/), [tt-trinity-gamma](https://github.com/gHashTag/tt-trinity-gamma) | Confirmed against live registry 2026-05-29. Retires fabricated "#4914." |
| H-8 | TTSKY26b shuttle close date | **Closed 2026-05-18 UTC** (= 2026-05-19 06:59 Asia/Bangkok +07); ChipFoundry CI2605, SkyWater 130 nm, 275 designs, est. delivery 2026-12-20 | `Verified` (external registry) | [registry](https://tinytapeout.com/chips/ttsky26b/) | The bare "closed 2026-05-19" (UTC) is RETIRED. Always cite as "2026-05-18 UTC" with the +07 reconciliation when a local date is shown. 275 total designs ⇒ 4-digit project IDs are impossible. |

## E. Composition / coverage claims

| ID | Claim | Canonical value | Status | Authoritative source | Notes / correction |
|----|-------|-----------------|--------|----------------------|--------------------|
| C-1 | ML+AR composition patterns | **4 demonstrated** (CNN+Rules, MLP+Bayesian, Transformer+XAI, RL+Guardrails); up to **7 specified** in `composition.t27` | `SIMULATED` | `specs/ar/composition.t27` | **CONFLICT TO FIX:** "4/4" and "7 patterns" are used interchangeably. Standardize: **"4 demonstrated, 7 specified."** Never write a bare "7 patterns demonstrated." |
| C-2 | AR specification modules | **8/8 complete**; "93 tests / 19 invariants" is **not reproducible from a single in-repo command** (only `examples/05_redteam_test.py` + `test_vectors/ta2/redteam_tests.json` exist as runnable test files) | `SIMULATED` | Evidence package; `find` test inventory 2026-05-29 | Either pin the exact suite that yields 93/19 or stop calling it "test coverage." Until pinned, present as a `[SIMULATED]` design target, not a measured result. |
| C-3 | Numeric format coverage | ~30 at submission → **66** post-submission | `SIMULATED` | NeuronConstant addendum | Scope note: this belongs to the **follow-on** track, not core CLARA TA1/TA2 (see DePIN addendum). |

---

## F. Complexity-claim corrections

| ID | Original wording | Problem | Corrected wording |
|----|------------------|---------|-------------------|
| X-1 | "Theorem 4: Bounded ASP Executes in O(1) Constant Time" | ASP is NP-hard; "O(1)" is not a meaningful complexity class for it. Fixed array bounds do not change the complexity *class* — they cap input size. | "Bounded-ASP termination: TRINITY restricts ASP to a fixed fragment (MAX_CLAUSES=256, MAX_ITERATIONS=1000) that is **guaranteed to terminate in a bounded number of steps**. We make no claim about the asymptotic complexity class of general ASP, which remains NP-hard." |

---

## CHIP-PROVENANCE (external-record verification, 2026-05-29)

The three TRI-NET chips were verified against the **live** TinyTapeout
TTSKY26b registry ([tinytapeout.com/chips/ttsky26b/](https://tinytapeout.com/chips/ttsky26b/))
on 2026-05-29. The registry is the authoritative external source for chip
identity; in-repo prose is a render target and does not override it.

| Chip | Top module | **Verified project ID** | Retired fabricated ID | Repo |
|------|-----------|-------------------------|------------------------|------|
| Φ Phi | `tt_um_trinity_nano` | **#198** | ~~#4913~~ | [tt-trinity-phi](https://github.com/gHashTag/tt-trinity-phi) |
| Ε Euler | `tt_um_ghtag_trinity_gf16` | **#558** | ~~#4915~~ | [tt-gf16-euler](https://github.com/gHashTag/tt-gf16-euler) |
| Γ Gamma | `tt_um_trinity_max_true` | **#750** | ~~#4914~~ | [tt-trinity-gamma](https://github.com/gHashTag/tt-trinity-gamma) |

**Shuttle facts (Verified):** TTSKY26b launched 2026-04-25, **closed
2026-05-18 UTC** (= 2026-05-19 06:59 Asia/Bangkok +07), ChipFoundry
CI2605 on SkyWater 130 nm, **275 designs**, est. delivery **2026-12-20**.

**Why the fabricated IDs were impossible:** the shuttle holds only 275
designs, so any 4-digit project ID (#4913/#4914/#4915) cannot exist on
TTSKY26b. These strings are RETIRED program-wide and banned in CI.

**Status discipline:** all three chips carry registry status "Submitted"
— GDS-II submitted to fab, **dies not yet returned**. No claim of
"realized / committed to silicon" is permitted without the pre-silicon
qualifier until physical dies return (est. 2026-12-20).

---

## Enforcement

1. Every numeric claim in `README.md`, `proposal/`, `submission/`, `evidence/`, and `docs/`
   must map to a row above and carry the matching status tag.
2. CI check: grep for the regex `100% robust` and fail the build — that value is
   retired (see R-1). The CI gate also bans the fabricated chip IDs
   `#4913`/`#4914`/`#4915` and the bare close date `closed 2026-05-19`
   (see CHIP-PROVENANCE; the real IDs are #198/#558/#750 and the close
   date is 2026-05-18 UTC).
3. When a value changes, update **this file first**, then propagate. This file wins all conflicts.

*Last updated: 2026-05-29. Maintained as the SSOT for the TRINITY CLARA submission package.*
