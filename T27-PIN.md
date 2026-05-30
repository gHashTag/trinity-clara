<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0 -->

# TRINITY CLARA — Upstream `t27` Reference Pin

**Date pinned:** 2026-05-30
**Purpose:** Pin the exact `gHashTag/t27` commit that this submission depends on. Future
edits to `t27` MUST NOT silently invalidate the formal-verification, RTL-simulation, or
benchmark claims registered in [`CLAIMS-LEDGER.md`](CLAIMS-LEDGER.md). If `t27` moves
forward, this file is updated together with the ledger entries that cite it.

---

## 1. Pinned commit

| Field | Value |
|-------|-------|
| Repository | https://github.com/gHashTag/t27 |
| Default branch | `master` |
| Pinned commit SHA | `e7a07f15ac0833a0c52f46ed8a646214fbd41357` |
| Pinned short SHA | `e7a07f1` |
| Commit timestamp | 2026-05-30T22:11:17+07:00 |
| License of pinned tree | Apache-2.0 |
| Languages present | Zig, Rust, Python, C, Verilog, TypeScript, Coq/Rocq, F\*, Shell |

**Reproduce the pin locally:**

```bash
git clone https://github.com/gHashTag/t27
cd t27
git checkout e7a07f15ac0833a0c52f46ed8a646214fbd41357
```

---

## 2. Directories in the pinned tree that this submission relies on

These are the only `t27` paths that back claims in this `trinity-clara` package.
Anything not listed here is **not** part of the submission's evidentiary surface.

| Path in pinned `t27` | What it provides | Backs claim |
|----------------------|------------------|-------------|
| `clara-bridge/` | DARPA-facing working code: `run_scenario.py`, four runnable examples (`01_medical_diagnosis.py`, `coa_planning.py`, `04_vsa_analogy.py`), evidence files (`CLARA-EVIDENCE-PACKAGE.md`, `CLARA-RED-TEAM.md`, `CLARA-SCALING.md`, etc.). | C-1 … C-3 (application performance), R-1 … R-3 (Red Team), reference for §Quick Start in this repo. |
| `coq/` (`Kernel/`, `IGLA/`, `Theorems/`) and `proofs/trinity/` | Coq/Rocq proof base. `proofs/trinity/` is the math-core (φ identities, certified bounds) referenced by F-2 in the ledger. | F-1, F-2 (formal-verification counts). Reproduction commands in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md). |
| `conformance/*.json` | 100+ conformance vector sets, including `clara_spec_coverage.json`, `ar_asp_solver.json`, `ar_composition.json`, `ar_explainability.json`, `ar_restraint.json`, `vsa_core.json`. | Test vectors cited from `test_vectors/` in this repo, and `clara_spec_coverage.json` directly maps to TA1 coverage. |
| `specs/` (170+ `.t27` files) | Source specifications for everything that gets lowered to Verilog / Zig / C. | F-3 (ML+AR composition correctness via `.t27 → Verilog` lowering, `SIMULATED`). |
| `gen/verilog/`, `gen/zig/`, `gen/c/` | Generated backends (28 modules, RTL-equivalent for SW; SIM-level for HW). | F-3, F-4 (cross-die anchor, simulation tier). |
| `chips/` (`phi/`, `euler/`, `gamma/`) | TinyTapeout shuttle TTSKY26b RTL for the three Trinity dies. | F-4 (cross-die anchor, sim) and H-5/H-6/H-7 in the ledger. |
| `fpga/` (`vivado/`, `vsa/`) | FPGA build artifacts; `bench/results_v02_real.json` is the throughput measurement template. | Hardware-throughput claims. **See §3 below for the honest gap.** |
| `bootstrap/` (Stage-0 Rust) | The `t27c` compiler that parses `.t27` specs and drives codegen. | F-5 (R-SI-1 invariant CI check), and the precondition for running any of the above. |

---

## 3. Honest open gap in the pinned tree (must remain visible)

`t27/bench/results_v02_real.json` currently records:

```json
{
  "tokens_per_sec_sim": 1193,
  "tokens_per_sec_real": null,
  "bitstream_sha256": "TBD — fill after running: shasum -a 256 fpga/vsa/gf16_heartbeat_top.bit",
  "timestamp": "TBD — fill with ISO 8601 after measurement"
}
```

**Status today:** the 1,193 tokens/s figure is `SIMULATED`. The real on-board measurement
on the QMTECH Wukong V1 (XC7A100T-1FGG676C, DLC-10 programmer) has **not** been recorded.
Any hardware-throughput sentence in this submission that omits `[SIMULATED]` is wrong and
must be corrected. See `DISCREPANCIES.md` for the punch list and `CLAIMS-LEDGER.md` for the
canonical wording.

This is the single largest unmeasured number in the package. We retain it as `SIMULATED`
rather than promote it to `MEASURED` until the bitstream SHA-256 and the UART throughput
log are appended to `t27/bench/results_v02_real.json` and re-pinned here.

---

## 4. When to update this pin

Update **only** when one of the following happens, and update the corresponding ledger row
in the same PR:

1. A new Coq lemma in `proofs/trinity/` flips from `Admitted` → `Qed.` (touch F-2).
2. `bench/results_v02_real.json` receives a real measurement (touch the hardware rows and
   §3 above; move the relevant claim from `SIMULATED` to `MEASURED`).
3. A `clara-bridge/scenarios/*.json` is added or its `run_scenario.py` semantics change
   (touch C-1 … C-3 if any quoted accuracy/latency moves).
4. A new chip taping or silicon return changes F-4's status from `SIMULATED` to `MEASURED`.

Routine documentation churn in `t27` (typos, comment edits, README polish) does **not**
require re-pinning here. The pin is for evidentiary integrity, not bookkeeping.
