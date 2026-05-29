<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# TRINITY PhD & Upstream Provenance — DARPA CLARA PA-25-07-02

**Purpose.** This appendix gives an honest, auditable account of where the
artefacts referenced in the TRINITY CLARA submission come from. It is meant to
be read alongside `README.md`, `proposal/CLARA-PROPOSAL-TECHNICAL.md`, and
`submission/CLARA-SUBMISSION-PACKAGE.md`. Nothing in this document expands
TRINITY's claims; it constrains and clarifies them.

**Scope.** TRINITY CLARA (this repository) is a *submission slice*: a focused
package built on top of upstream Trinity research. It is **not** the full
proof base, and we do not represent it as such.

Audit cutoff for upstream counts in this document: **2026-05-12**.

---

## 1. Repository topology

| Repository | Role | Relationship to TRINITY CLARA |
|---|---|---|
| [`gHashTag/trinity-clara`](https://github.com/gHashTag/trinity-clara) | **This repo.** DARPA CLARA PA-25-07-02 submission package. | Source of truth for the submission. |
| [`gHashTag/t27`](https://github.com/gHashTag/t27) | Upstream Trinity codebase: `.t27` compiler, Coq proof base, Verilog backends. | Provides the broader Coq library that the CLARA submission references. |
| [`gHashTag/trios`](https://github.com/gHashTag/trios) | PhD-grade research harness: `docs/phd` (thesis chapters), `crates/trios-phd` (Rust audit harness), invariant contracts. | Provides PhD-level provenance, audit tooling, and runtime invariant contracts that bind to `proofs/igla/*.v`. |

The submission is therefore a **proof subset**, not a full re-export of
upstream Trinity. Claims about "TRINITY's proof base" in CLARA documents
should be read against the counts in §2 and §3, not against the broader
upstream library.

---

## 2. Proof status — `proofs/igla/` (this repository)

The IGLA proof package shipped in this submission is the canonical six-INV
bundle plus three additional files added during the IGLA L-H4 / L-CLARA-FREEZE
work. Honest, auditable counts:

| Class | Count | Notes |
|---|---|---|
| `.v` files in `proofs/igla/` | 8 | Six INV files + `lr_convergence.v` + `hybrid_qk_gain.v` (the latter still landing). `CorePhi.v` ships separately as a small core shim. |
| `Qed` (canonical IGLA bundle, per `_metadata.json`) | 47 | Across the 6 INV files: `igla_asha_bound` (6), `gf16_precision` (5), `nca_entropy_band` (6), `lr_phi_optimality` (6), `lucas_closure_gf16` (13), `igla_found_criterion` (11 of which 5 are `Example` refutations). |
| `Admitted` (IGLA budget) | 4 | Tracked in `_metadata.json → admitted_budget`. Each `Admitted` is named, has a stated reason, and a `close_with:` recipe (typically `Coq.Interval`-backed). |
| Honest `Qed` placeholders | 1 | `welch_ttest_alpha_001_rejects_baseline` in `igla_found_criterion.v` is `Qed`-closed but its statement currently reduces to `True`; the *real* invariant is enforced at runtime in `trios:crates/trios-igla-race/src/victory.rs::stat_strength` until the Coq.Interval-backed Welch t-test bound lands. |
| `Axiom` | 1 | `phi_pow_to_lucas` (Binet formula for `R^nat`) in `lucas_closure_gf16.v`. Standard practice when anchoring `f64` PHI to `lucas_even:Z` without a real-analysis library. |
| Falsification witnesses | 10 | One `*_falsification_is_contradiction` per INV file, plus five `refutation_*` examples in `igla_found_criterion.v`. Each one proves that violating the invariant implies `False` or contradicts `victory_acceptable`. |

**What this means.** The IGLA proof package is **not** fully proven. It is
*honestly partial*: 47 closed obligations, 4 declared open obligations with
stated closure paths, 1 placeholder that defers to a runtime guard, and 1
axiom. Calling it "fully proven" would be wrong. Calling it "vapour" would
also be wrong.

Authoritative source: [`proofs/igla/_metadata.json`](../proofs/igla/_metadata.json).
Runtime binding for the placeholder: [trios `victory.rs`](https://github.com/gHashTag/trios/blob/main/crates/trios-igla-race/src/victory.rs).

---

## 3. Upstream proof status — `gHashTag/t27` (audit 2026-05-12)

The upstream `t27` Coq proof base is the broader library that CLARA documents
sometimes refer to. As of the **2026-05-12 audit**, it reports:

| Metric | Count |
|---|---|
| Audited `.v` files | 28 |
| Stated `Theorem` / `Lemma` | 218 |
| `Qed` (closed proofs) | 162 |
| `Admitted` | 32 |
| `Abort` | 2 |

This is the number to cite when discussing the upstream proof base. The
phrase **"84 Coq theorems"** that appears in some older CLARA narrative was
a snapshot from v1.1 of the technical proposal and is no longer the right
figure to cite; where it survives, it should be read as a historical
v1.1 milestone, not a current count. Newer documents in this submission
prefer either:

- "47 closed obligations + 4 Admitted in the IGLA proof bundle" (for the
  CLARA-scoped IGLA subset shipped here), or
- "162 Qed / 32 Admitted / 2 Abort across 28 .v files in upstream `t27`
  (audit 2026-05-12)" (for the broader upstream library).

---

## 4. PhD provenance — `gHashTag/trios`

The Trinity S³AI architecture has a documented PhD-thesis backbone that lives
in the `trios` repository. CLARA reviewers who want to verify provenance
should consult, in this order:

| Artefact | Path | What it gives you |
|---|---|---|
| Thesis source | `docs/phd/` in [`gHashTag/trios`](https://github.com/gHashTag/trios) | Chapter-level write-up of the φ-structured number system, L1–L7 derivation hierarchy, and CLARA-relevant arguments. |
| Audit harness | `crates/trios-phd` in [`gHashTag/trios`](https://github.com/gHashTag/trios) | Rust harness that re-runs the audit and produces the `.v` counts cited in §3. |
| Runtime invariant contract | [`assertions/igla_assertions.json`](../assertions/igla_assertions.json) (this repo, mirrored from `trios`) | Machine-readable contract binding `proofs/igla/*.v` to runtime checks (`L-R14`). |
| Issue threads | [trios#372](https://github.com/gHashTag/trios/issues/372), [trios#264](https://github.com/gHashTag/trios/issues/264) | Review threads that motivated several of the L-CLARA-FREEZE proof closures. |

**CLARA-relevant PhD chapters and appendices.** The PhD covers a wider scope
than CLARA; the chapters that are load-bearing for the CLARA submission are,
by topic: Ch. 22 (proof discipline / invariant contracts), Ch. 24 (φ-structured
arithmetic and GF16), Ch. 28 (compositional reasoning and L1–L7), Ch. 34
(IGLA / RACE), and the appendices App. B / F / G / H / I / M / N (formal
appendices, falsification protocol, runtime audits). **Reviewers should treat
these chapter numbers as *pointers into `trios:docs/phd/`*** — if a file name
differs in the published thesis, the canonical path is whatever is checked
in to `trios:docs/phd/` at the audit cutoff above; we do not duplicate the
PhD source tree here.

---

## 5. Zenodo software/provenance DOIs

Three canonical Zenodo records carry the **software and provenance artefacts**
behind TRINITY. These DOIs are **provenance and citation handles** for the
software releases — they are *not* a proof source. The proof source is
`proofs/igla/*.v` (this repo) and the upstream `t27` Coq base.

| DOI | Subject |
|---|---|
| [10.5281/zenodo.19227879](https://doi.org/10.5281/zenodo.19227879) | TRINITY framework (umbrella software release) |
| [10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877) | φ / VSA components |
| [10.5281/zenodo.18947017](https://doi.org/10.5281/zenodo.18947017) | FPGA / hardware backend |

**Citation hygiene.** When citing these DOIs in CLARA documents, use the form
"Zenodo software record" or "provenance DOI". Do not phrase them as "proves"
or "verifies".

---

## 6. Team & author provenance

### 6.1 Principal Investigator

**Dr. Scott A. Olsen** (Wisdom Traditions Center, LLC / College of Central
Florida). PhD (Philosophy, University of Florida, 1983), J.D. (Levin College
of Law, 1977). Full bio and publications: see
[`submission/EXECUTIVE-SUMMARY.md § Key Personnel`](../submission/EXECUTIVE-SUMMARY.md).
This appendix does not introduce new PI claims; it only points back to the
content already in the executive summary.

### 6.2 Co-Investigator — Dmitrii Vasilev (Trinity S³AI Research Group)

- ORCID: [0009-0008-4294-6159](https://orcid.org/0009-0008-4294-6159)
- Primary architect of the t27 compiler, GoldenFloat formats, IGLA RACE
  proof base, and `trios-phd` audit harness.
- Author context for upstream artefacts cited in this submission:
  [`gHashTag/t27`](https://github.com/gHashTag/t27),
  [`gHashTag/trios`](https://github.com/gHashTag/trios),
  [`gHashTag/trinity-clara`](https://github.com/gHashTag/trinity-clara).

### 6.3 Co-Investigator — Dr. Stergios Pellis (Physics & Applied Mathematics)

- Contributes mathematical-physics expertise, statistical validation
  methodology, and benchmark/ablation design.
- **TODO (pre-submission):** confirm institutional affiliation and ORCID.
  These are not yet recorded in this repository and must be filled in before
  the final submission package is sealed. We deliberately do not invent
  either field.

---

## 7. Language discipline

CLARA-facing documents in this submission use the following technical
phrasing and **do not** use mystical or unbounded-capability language:

- **Use:** "verifiable distributed cognition", "formal proof-backed cognitive
  substrate", "φ-structured arithmetic", "ternary K3 reasoning with bounded
  rationality", "L1–L7 derivation hierarchy".
- **Do not use:** "AGI", "superintelligence", "sentient", "consciousness
  engine", "sacred geometry" as a load-bearing claim. Where φ-related
  language appears (`φ² + φ⁻² = 3`, GF16, Lucas-closure), it is algebraic and
  hardware-relevant, not mystical.

---

## 8. Where to look next

| If you want to verify… | Read |
|---|---|
| The actual IGLA proof obligations and their closure status | [`proofs/igla/_metadata.json`](../proofs/igla/_metadata.json), [`proofs/igla/*.v`](../proofs/igla/) |
| The runtime invariant contract | [`assertions/igla_assertions.json`](../assertions/igla_assertions.json) |
| The upstream proof count (162 Qed / 32 Admitted / 2 Abort, 2026-05-12) | `gHashTag/trios:crates/trios-phd/` |
| The Red Team protocol and the 100% / 50-of-50 figure | [`evidence/CLARA-RED-TEAM.md`](../evidence/CLARA-RED-TEAM.md) |
| The PI / Co-I bios | [`submission/EXECUTIVE-SUMMARY.md`](../submission/EXECUTIVE-SUMMARY.md), [`submission/CLARA-SUBMISSION-PACKAGE.md`](../submission/CLARA-SUBMISSION-PACKAGE.md) |
| Software provenance DOIs | [10.5281/zenodo.19227879](https://doi.org/10.5281/zenodo.19227879), [10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877), [10.5281/zenodo.18947017](https://doi.org/10.5281/zenodo.18947017) |

---

**Document version:** 1.0 — 2026-05-13
**Author of record:** Trinity S³AI Research Group
**License:** Apache-2.0
