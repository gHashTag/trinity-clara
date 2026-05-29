<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# TRINITY CLARA — Reproducibility & Proof-State Disclosure

**Date:** 2026-05-29
**Purpose:** Give a reviewer the *exact*, verified commands to reproduce the formal-verification
claims, and an honest disclosure of the proof state (`Qed.` vs `Admitted`). This file is the
single source of truth for "how do I check the math myself?" Numbers here were obtained by
direct inspection of the repositories on 2026-05-29 and supersede any looser figure elsewhere
in the package (see `CLAIMS-LEDGER.md` F-1/F-2 and `PROJECT-AUDIT.md` B-1…B-7).

---

## 1. What is actually formally verified

The formal-verification claim rests on the **`gHashTag/t27`** Coq/Rocq proof base, specifically
the `proofs/trinity/` set. This proves the **mathematical/physics core** of the Trinity
framework — golden-ratio (φ) algebraic identities and certified numerical bounds for the
*G2 Alpha S Phi Framework v0.9* — **not** the ML+AR composition. Composition correctness is
established by `.t27 → Verilog` lowering and RTL **simulation** `[SIMULATED]`, never by a
machine-checked proof.

> **Claim status (per TRIOS rules):** the φ identities and certified bounds are `[PROVEN]` to
> the extent their `.v` files end in `Qed.`. Any lemma ending in `Admitted` is **not** proven and
> is disclosed as such below. The framework itself is published only as an `@unpublished` Zenodo
> stub — **no peer-reviewed publication exists** — so all *algorithmic/empirical* claims built on
> top of it are capped at **Open conjecture** until externally validated.

---

## 2. Exact reproduction steps (verified 2026-05-29)

```bash
# 1. Clone the proof base
git clone https://github.com/gHashTag/t27.git
cd t27/proofs

# 2. Install the Coq toolchain (the bounds proofs need coq-interval)
opam install coq coq-interval          # Coq 8.19+ / Rocq 9.0+, coq-interval >= 4.8.0

# 3. Generate the makefile and build
coq_makefile -f _CoqProject -o CoqMakefile
make -f CoqMakefile
# Expected: "0 errors, 0 warnings" for the trinity/ set
```

**Correction vs earlier wording.** Earlier docs wrote `cd proofs && make → 13/13 files compile`.
That is imprecise:

- `t27/proofs/` contains **18 `.v` files** total: `trinity/` (13), `sacred/` (4), `gravity/` (1).
- The **13-file figure refers to `proofs/trinity/` only** — the φ-identity + certified-bounds set.
- `make` is **not** bare: it requires `coq-interval` and the `coq_makefile -f _CoqProject` step.

---

## 3. Honest proof-state ledger (direct counts, 2026-05-29)

| Source tree | Theorems | Lemmas | `Qed.` | `Admitted` | Axioms | Notes |
|-------------|---------:|-------:|-------:|-----------:|-------:|-------|
| `t27/proofs/trinity/` (the `make` target, 13 files) | 110 | 54 | 132 | **32** | 0 | φ identities + certified physics bounds |
| `t27/proofs/` (all 18 `.v`) | 116 | 54 | 138 | 32 | 0 | adds `sacred/`, `gravity/` |
| `t27/` (whole repo, all `.v`) | 146 | 572 | 684 | 41 | — | program-wide incl. Physics/IGLA/Kernel |
| this repo `proofs/igla/` | 28 | 17 | 40 | **23** | 7 | IGLA lemmas, *honestly* `Admitted` per R5 |

**Reading these honestly:**

- The often-quoted **"84 Coq theorems [PROVEN]"** does **not** correspond to any single
  measured count above. Use the verifiable figures instead, and always pair a count with its
  `Admitted` total.
- The project's **Zenodo archive** (DOI [10.5281/zenodo.19227877](https://doi.org/10.5281/zenodo.19227877),
  audit 2026-05-12) records the VSA witness as **"48 statements, 35 Proven, 0 Admitted."** That is
  a *different, narrower* witness than the `proofs/trinity/` set above — cite it for the VSA
  operations specifically, not as the global theorem count.
- The in-repo `proofs/igla/` lemmas are deliberately `Admitted`; the files themselves state
  *"R5 honesty: every theorem in this file is honestly `Admitted`."* They are scaffolding, not
  evidence of proof, and must never be folded into a `[PROVEN]` count.

---

## 4. Program facts a reviewer can independently confirm

- **DARPA CLARA solicitation:** `DARPA-PA-25-07-02`, *Compositional Learning-And-Reasoning for AI
  Complex Systems Engineering*
  ([darpa.mil/research/programs/clara](https://www.darpa.mil/research/programs/clara)).
- **Zenodo archive:** *Trinity B007: VSA Operations for Ternary Computing v5.0*, Dmitrii Vasilev,
  ORCID 0009-0008-4294-6159, 2026-05-12 (Apache-2.0).
- **TinyTapeout shuttle:** SKY130A multi-project shuttle (see TinyTapeout chip registry for the
  specific run and chip IDs; cross-check the IDs in `submission/HARDWARE-REALIZATION-TRINET.md`
  against [tinytapeout.com/chips](https://tinytapeout.com/chips/) before final submission).

---

## 5. What is NOT proven (explicit non-claims)

- ML+AR **composition correctness** — `[SIMULATED]` (RTL simulation), not proven.
- Any **performance multiplier** (energy ×, GF16 speedups) — measurement/simulation, never a Coq
  theorem.
- "**Test coverage: 93 tests / 19 invariants**" — not reproducible from a single in-repo command;
  treat as `[SIMULATED]` until a runnable suite is pinned.

*Maintained alongside [`CLAIMS-LEDGER.md`](CLAIMS-LEDGER.md) (SSOT), [`PROJECT-AUDIT.md`](PROJECT-AUDIT.md),
and [`DISCREPANCIES.md`](DISCREPANCIES.md).*
