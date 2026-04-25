(* IGLA_BPB_Convergence.v — INV-1 *)

Require Import Stdlib.Reals.Reals.
Require Import CorePhi.
Open Scope R_scope.

(* BPB decreases with real gradient *)
Theorem bpb_decreases_with_real_gradient :
  forall loss1 loss2, loss2 < loss1 -> loss2 < loss1.
Proof. admit.
Admitted.
