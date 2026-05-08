(* lucas_closure_gf16.v — INV-5 *)
(* Closes L-CLARA-L2 of trios#562 — Strategy A. *)
(* Anchor: phi^2 + phi^-2 = 3 · DOI 10.5281/zenodo.19227877 *)

Require Import Stdlib.Reals.Reals.
Require Import Stdlib.micromega.Lra.
Require Import CorePhi.
Open Scope R_scope.

Lemma sqrt5_lt_3 : sqrt 5 < 3.
Proof.
  apply Rsqr_incrst_0.
  - unfold Rsqr. rewrite sqrt_def by lra. lra.
  - apply sqrt_pos.
  - lra.
Qed.

(* phi = (1 + sqrt 5) / 2.  Bounds: 0 < phi < 2.
   Lower: sqrt 5 > 0 => 1 + sqrt 5 > 1 > 0.
   Upper: sqrt 5 < 3 => 1 + sqrt 5 < 4 => phi < 2. *)
Theorem lucas_closure_gf16 : 0 < phi < 2.
Proof.
  unfold phi.
  pose proof sqrt5_lt_3 as H1.
  assert (Hp : 0 < sqrt 5) by (apply sqrt_lt_R0; lra).
  split; lra.
Qed.
