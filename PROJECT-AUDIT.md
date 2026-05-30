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

**RESOLVED 2026-05-29 (maintainer decision).** The submission uses a **contribution-based
three-person model**, consistent with `README.md`, `submission/CLARA-SUBMISSION-PACKAGE.md`
§Key Personnel, and `proposal/CLARA-COST-PROPOSAL.md` §1.1:

| Person | Role | Contribution |
|--------|------|--------------|
| **Dr. Scott A. Olsen** | Principal Investigator | Golden-mean number-system theory / philosophical-mathematical grounding (per his published book work). |
| **Dmitrii Vasilev** | Co-Investigator / technical lead | His own φ-arithmetic formulas, the Trinity/t27 framework, GF16 formats, and the TRI-NET RTL/silicon. |
| **Dr. Stergios Pellis** | Co-Investigator | Phenomenological physics formulas. |

All "sole author" / "single author" strings across the package have been **retired** (they
contradicted the three-person team and the budgeted cost proposal). "Original work of
D. Vasilev" is retained **only** for the RTL/proof artifacts he authored — a narrower, accurate
statement, not a project-wide authorship claim. Canonical contact email for D. Vasilev is
**`admin@t27.ai`** everywhere (the `bayotkwolpep9c@hotmail.com` address in the DePIN addendum was
a one-off and has been replaced). Recorded as ledger entry **A-1** in `CLAIMS-LEDGER.md`.

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

The 94.2% accuracy and 2.3 ms latency figures originate from a **100-scenario synthetic generator**; the Red Team 100% (50/50) score originates from a different 50-case balanced v1.0 testset (see [`test_vectors/ta2/redteam_tests.json`](test_vectors/ta2/redteam_tests.json)). Both are synthetic. Earlier drafts of this audit cited "96% robustness" from the 100-scenario generator; that figure is retired (the canonical v1.0 testset score is 100% (50/50), and the JSON for the older 100-scenario generator is not present at the pinned commit — see DISCREPANCIES.md D-1 RESOLVED). Per Track-3 (FActScore/HaluEval framing), synthetic results must be labelled and must carry a **falsification path**.

**Fix.** Tag every such number `[SYNTHETIC]` (or `[SYNTHETIC, v1.0 testset]` for the Red Team score); add a one-line falsification path ("would be disconfirmed if accuracy on a *real* COA dataset falls below X").

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
| 7 | A-1 | Authorship reconciliation | ✅ applied 2026-05-29 — three-person contribution model (Olsen PI / Vasilev Co-I / Pellis Co-I); all "sole author" strings retired; single email admin@t27.ai. Ledger A-1. |
| 8 | A-6/A-9 | φ-as-engineering + falsification paths | ✅ doc-level (KEY-PERSONNEL-REWRITE + ledger); full propagation = follow-up |
| 9 | A-8/A-11 | Source GF16 superlatives; badge cleanup | ⏳ follow-up (needs benchmark data) |

Items marked ⏳ require a human decision or data that must not be fabricated — per the rules,
they are flagged here rather than invented.

---

# Wave 3 — Code / Proof / External-Fact Audit (B-series)

**Date:** 2026-05-29
**Method:** Direct inspection of the in-repo `proofs/` tree and the external `gHashTag/t27`
repository (`cd proofs && make` target), byte-level line counts of `.t27` specs, and
external-source verification (Zenodo record, DARPA CLARA solicitation, TinyTapeout shuttle).
This pass moves from prose self-contradiction (A-series) to **claim-vs-artefact** verification:
does the evidence the submission points to actually say what the submission says it says?

Verified external facts (so the package can lean on them):

- **DARPA CLARA is real:** solicitation **DARPA-PA-25-07-02**, *Compositional Learning-And-Reasoning
  for AI Complex Systems Engineering*, announced 2026-02-04/10, Phase 1+2 capped at $2,000,000
  ([darpa.mil/research/programs/clara](https://www.darpa.mil/research/programs/clara),
  [CLARA FAQs PDF](https://www.darpa.mil/sites/default/files/attachment/2026-04/clara-program-darpa-faqs.pdf)).
- **Zenodo DOI 10.5281/zenodo.19227877 is real** — *"Trinity B007: VSA Operations for Ternary
  Computing v5.0"*, Dmitrii Vasilev (ORCID 0009-0008-4294-6159), 2026-05-12
  ([doi.org/10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877)).
- **The external `t27` proof base is real and substantial** (the `proofs/trinity/` set builds via
  `make`).

| ID | Severity | Anomaly | Evidence | Remediation |
|----|----------|---------|----------|-------------|
| **B-1** | 🔴 | **"84 Coq theorems [PROVEN]" is unverifiable as stated and contradicts every authoritative source.** The number 84 appears across README, ARCHITECTURE, FAQ, proposal, submission, evidence, addendum. But: (a) the project's own Zenodo archive states **"48 statements, 35 Proven, 0 Admitted"**; (b) KEY-PERSONNEL prose says **"80+ Coq theorems"**; (c) the in-repo `proofs/` has **45 declarations, 23 Admitted, 7 Axioms**; (d) the external `t27/proofs/trinity/` (the `make` target) has **110 theorems + 54 lemmas but 32 Admitted** — not 0. No single source yields exactly 84-proven-0-admitted. | Zenodo record; `t27/proofs/`; `proofs/igla/`; README:332 | Replace the bare "84 theorems [PROVEN]" with the **verifiable** statement: the `t27/proofs/trinity/` set (13 files) builds under Coq/Rocq with `make`; cite the Zenodo-archived count and **disclose `Admitted` honestly**. Cap composition correctness at `[SIMULATED]`. |
| **B-2** | 🔴 | **"PROVEN" overstates the actual proof state — `Admitted` ≠ proven.** The in-repo IGLA proofs are *honestly* marked `Admitted` (the files themselves cite "R5 honesty: every theorem in this file is honestly `Admitted`"), and the `t27` trinity set carries 32 `Admitted`. A claim tagged `[PROVEN]` must not include `Admitted` lemmas in its count. | `proofs/igla/hybrid_qk_gain.v:39`; `t27/proofs/trinity/*` | Down-grade to **"machine-checked where `Qed.`; remaining lemmas honestly `Admitted` (logged)"**; never fold `Admitted` into a PROVEN count. |
| **B-3** | 🟠 | **Wrong expansion of the CLARA acronym in 5 files.** The submission writes *"DARPA CLARA (Common Learning Repository for AI)"*. The actual program is *"**Compositional Learning-And-Reasoning** for AI Complex Systems Engineering."* Misnaming the program you are applying to is a credibility hit a reviewer will catch instantly. | README:24; EXECUTIVE-SUMMARY:8; CLARA-SUBMISSION-PACKAGE:15; CLARA_TECHNICAL_NARRATIVE:5; CLARA-PREPARATION-PLAN:11 | Replace all 5 with the official name. |
| **B-4** | 🟠 | **`composition.t27` line-count is wrong in 4 docs.** Claimed **622 lines**; actual file is **674 lines**. (A prior draft also said 247.) | `specs/ar/composition.t27` (674 by `wc -l`); proposal:228; 3 evidence docs | Correct to 674, or drop the precise count. |
| **B-5** | 🟠 | **Reproducibility command is imprecise.** Docs say `git clone t27 && cd proofs && make → 13/13 files compile`. The `proofs/` root actually holds **18 `.v` files** across `trinity/` (13), `sacred/` (4), `gravity/` (1); only the **`trinity/` subdir is 13 files**, and `make` requires `coq-interval` + a `coq_makefile` step the docs omit. | `t27/proofs/` (18 .v); `proofs/README.md` build steps | Pin the exact path (`proofs/trinity/`), list the `opam install coq coq-interval` + `coq_makefile -f _CoqProject` prerequisites. See new `REPRODUCIBILITY.md`. |
| **B-6** | 🟡 | **"93 tests, 19 invariants" is unverified in-repo.** Only `examples/05_redteam_test.py` and `test_vectors/ta2/redteam_tests.json` exist as test files; the 93/19 figures are not reproducible from a single command. (Inline `test`/`assert` tokens across `.t27` specs do exist but do not sum to a clean 93.) | `find` test inventory | Either point to the exact suite that yields 93/19 or tag the figure `[SIMULATED]` and stop calling it "test coverage." |
| **B-7** | 🟡 | **`t27/proofs/` README scopes the proofs to a *physics* framework, not CLARA's ML+AR composition.** The proof base verifies the *G2 Alpha S Phi Framework v0.9* (gauge couplings, quark/lepton masses, φ identities) and is cited as `@unpublished`. Presenting it as evidence for "compositional learning-and-reasoning" over-reaches the artefact's own scope. | `t27/proofs/README.md` (`@unpublished{TrinityFramework2026}`) | Frame these theorems as proving the **mathematical/physics core (φ identities, certified bounds)** only — exactly the F-2 ledger guidance — and keep ML+AR composition at `[SIMULATED]`. |

## Wave 3 remediation plan

| Step | Anomaly | Action | Status in this PR |
|------|---------|--------|-------------------|
| 1 | B-1/B-2 | Replace "84 theorems [PROVEN]" with verifiable build-and-archive wording; disclose `Admitted` | ✅ applied |
| 2 | B-3 | Fix CLARA acronym in all 5 files | ✅ applied |
| 3 | B-4 | Correct `composition.t27` to 674 lines | ✅ applied |
| 4 | B-5 | Add `REPRODUCIBILITY.md` with exact verified build steps | ✅ applied |
| 5 | B-6 | Down-tag "93 tests/19 invariants" wording | ✅ applied |
| 6 | B-7 | Reconcile CLAIMS-LEDGER F-2 with Zenodo/t27 facts | ✅ applied |
| 7 | B-1/B-3/B-4 | Extend CI gate with number/acronym consistency checks | ✅ applied |

---

# Wave 4 — External-Record Verification Audit (C-series)

**Date:** 2026-05-29
**Method:** Direct verification of every reviewer-checkable external fact in the
submission against the **live** TinyTapeout TTSKY26b registry
([tinytapeout.com/chips/ttsky26b/](https://tinytapeout.com/chips/ttsky26b/)),
cross-checked by submitter name "Dmitrii Vasilev" and against the companion
GitHub repos (`tt-trinity-phi`, `tt-trinity-euler`, `tt-trinity-gamma`). This pass
moves from *claim-vs-artefact* (B-series) to **claim-vs-external-record**: do the
facts a DARPA reviewer could independently confirm in a public registry actually
match what the submission asserts? This is the most dangerous anomaly class
because a single registry lookup by a reviewer falsifies a fabricated fact
instantly.

Verified external facts (authoritative — the package must match these exactly):

- **TTSKY26b is real:** launched 2026-04-25, **closed 2026-05-18 UTC**, ChipFoundry
  CI2605 on SkyWater 130 nm, **275 designs total**, est. delivery **2026-12-20**
  ([registry](https://tinytapeout.com/chips/ttsky26b/)).
- **Verified Trinity project IDs:** Φ Phi **#198** (`tt_um_trinity_nano`), Ε Euler
  **#558** (`tt_um_ghtag_trinity_gf16`), Γ Gamma **#750** (`tt_um_trinity_max_true`).
- 275 total designs ⇒ **no 4-digit project ID can exist** on this shuttle.

| ID | Severity | Anomaly | Evidence | Remediation |
|----|----------|---------|----------|-------------|
| **C-1** | 🔴 | **Chip project IDs #4913 / #4914 / #4915 are FABRICATED.** The submission tagged Phi/Gamma/Euler with 4-digit TinyTapeout IDs. The TTSKY26b shuttle holds only **275 designs**, so a 4-digit ID is structurally impossible. The real, registry-confirmed addresses are **#198 (Phi), #558 (Euler), #750 (Gamma)**. A reviewer who opens the registry sees the contradiction in one click. | Live [TTSKY26b registry](https://tinytapeout.com/chips/ttsky26b/) (275 designs; names "Dmitrii Vasilev") | Replace all #4913→#198(Phi)/#4915→#558(Euler)/#4914→#750(Gamma). Add CHIP-PROVENANCE block to CLAIMS-LEDGER. Ban the fabricated strings in CI. |
| **C-2** | 🔴 | **Shuttle close date stated as "closed 2026-05-19" is wrong.** The registry records the close as **2026-05-18 UTC**. The repo's local-time intuition (Asia/Bangkok +07) explains the off-by-one: 2026-05-18 23:59 UTC = 2026-05-19 06:59 +07. Stated bare as a UTC date, "2026-05-19" contradicts the registry. | [registry](https://tinytapeout.com/chips/ttsky26b/) | Standardize to **"closed 2026-05-18 UTC (= 2026-05-19 06:59 +07)"** with the registry link. Ban the bare "closed 2026-05-19" in CI. |
| **C-3** | 🔴 | **"Committed to silicon" / "not simulated" overclaims contradict the pre-silicon reality.** Three statements (`HARDWARE-REALIZATION-TRINET.md` §1 "the safety lattice is not simulated — it is committed to silicon" and §Gap-2 "k3_alu is not simulated"; `CLARA-PROPOSAL-TECHNICAL.md` "complete and committed to silicon") assert a present-tense silicon fact. Per H-4, all three chips carry registry status **"Submitted"**; dies are **not yet returned** (est. delivery 2026-12-20). Calling a pre-silicon GDS submission "committed to silicon / not simulated" is a High-risk overclaim. | H-4 ledger; [registry](https://tinytapeout.com/chips/ttsky26b/) status "Submitted" | Reword to "synthesizable gate-level RTL with passing `gds` CI; GDS-II **submitted to fab** (status Submitted; dies not yet returned)" + `[MEASURED in simulation / SUBMITTED to fab]` tag. Done across both files. |
| **C-4** | 🟠 | **Three "world's first / first known" superlatives are unverifiable.** No exhaustive prior-art survey exists, so "world's first hardware implementation of all 10 CLARA gaps" cannot be asserted as fact. Also "strongest possible evidence." | EXECUTIVE-SUMMARY:14; HARDWARE-REALIZATION:16; CLARA-PROPOSAL:175 | Soften to "to the authors' knowledge, the first **published** open-silicon implementation" + `[Open conjecture]` with a written `falsification_path` (any earlier published open-silicon CLARA-gap chip refutes it). Done. |
| **C-5** | 🟡 | **Wrong registry URL path `tinytapeout.com/runs/ttsky26b`.** The canonical chip page is `tinytapeout.com/chips/ttsky26b/`. A dead/incorrect link in the submission's external-evidence section reads as carelessness. | HARDWARE-REALIZATION-TRINET:208 | Corrected to `https://tinytapeout.com/chips/ttsky26b/`. Done. |

## Wave 4 remediation plan

| Step | Anomaly | Action | Status in this PR |
|------|---------|--------|-------------------|
| 1 | C-1 | Replace fabricated #4913/#4914/#4915 with verified #198/#558/#750 across all non-meta docs | ✅ applied |
| 2 | C-2 | Standardize close date to 2026-05-18 UTC (+07 reconciliation) with registry link | ✅ applied |
| 3 | C-3 | Reword "committed to silicon"/"not simulated" to pre-silicon SUBMITTED framing + claim-status tags | ✅ applied |
| 4 | C-4 | Soften "world's first" superlatives to Open conjecture + falsification path | ✅ applied |
| 5 | C-5 | Fix registry URL `/runs/` → `/chips/` | ✅ applied |
| 6 | C-1/C-2 | Add CHIP-PROVENANCE block + H-5…H-8 rows to CLAIMS-LEDGER; reconcile H-4/F-4 | ✅ applied |
| 7 | C-1/C-2 | Extend CI gate to ban fabricated IDs + bare wrong close date | ✅ applied |

*Audit maintained alongside [`CLAIMS-LEDGER.md`](CLAIMS-LEDGER.md) (SSOT),
[`DISCREPANCIES.md`](DISCREPANCIES.md), and [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).*
