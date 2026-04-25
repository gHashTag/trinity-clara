(* IGLA_NCA_Entropy.v — Formal NCA entropy band invariants *)

Require Import Stdlib.Reals.Reals.
Require Import CorePhi.
Open Scope R_scope.

(* Entropy band [1.5, 2.8] *)
Definition entropy_min : R := 1.5.
Definition entropy_max : R := 2.8.

(* Theorem: Band non-empty *)
Theorem entropy_band_non_empty : entropy_min < entropy_max.
Proof. Admitted.
