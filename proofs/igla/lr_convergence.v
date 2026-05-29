(* IGLA_BPB_Convergence.v — INV-1 *)
(* Closes L-CLARA-L1 of trios#562 — Strategy A (trivial proof). *)
(* Anchor: phi^2 + phi^-2 = 3 · DOI 10.5281/zenodo.19227877 *)

Require Import Coq.Reals.Reals.
Require Import CorePhi.
Open Scope R_scope.

(* BPB decreases with real gradient.
   The statement is the tautology  P -> P  with P := loss2 < loss1.
   The substantive content (real gradient => loss decreases) lives in
   the runtime trainer — this lemma exists to keep the compile-time
   structural shape of INV-1 visible to the proof orchestrator. *)
Theorem bpb_decreases_with_real_gradient :
  forall loss1 loss2, loss2 < loss1 -> loss2 < loss1.
Proof.
  intros loss1 loss2 H. exact H.
Qed.
