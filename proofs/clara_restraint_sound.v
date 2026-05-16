(** * CLARA Gap-4: Restraint Control Soundness — Theorem 86

    Repository : gHashTag/trinity-clara
    Path       : proofs/clara_restraint_sound.v
    Issue      : CLARA Gap-4 (restraint_ctrl force_unknown spec)
    Date       : 2026-05-17
    Author     : Trinity S³AI Research Group

    Anchor     : φ² + φ⁻² = 3  (Trinity Identity)
    DOI        : 10.5281/zenodo.19227877

    ---------------------------------------------------------------
    Informal statement
    ---------------------------------------------------------------
    The restraint_ctrl module maintains a state [s : state] and
    processes inputs [i : input] containing three fields:
      - phi_drift   : nat  — φ-drift sensor reading
      - step_count  : nat  — step counter
      - receipt_ok  : bool — receipt validity flag

    A single-step transition [step_restraint s i] computes a new
    state [s'].  The output bit [force_unknown s'] satisfies:

    (A) Soundness: for any state [s] and input [i],
          force_unknown s'
          = (phi_drift i >? 164) || (step_count i >? 10) || (¬ receipt_ok i)
        OR the output was already tripped:
          force_unknown s = true ∧ force_unknown s' = true.

    (B) Sticky: once [force_unknown s = true], every subsequent
        transition keeps [force_unknown] = true.

    (C) Reason one-hot: when [force_unknown s' = true], the
        [reason] bitvector stored in [s'] has popcount ≤ 1
        (at most one causal bit is set).

    All three are proved below with zero uses of [Admitted].
    ---------------------------------------------------------------

    Compatibility: Coq 8.18+ / Rocq 9.x  (no non-standard imports)
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Bool.Bool.
Require Import Coq.Lists.List.
Require Import Coq.micromega.Lia.
Import ListNotations.

Set Implicit Arguments.

(* ================================================================ *)
(** ** 1.  Input / Output types                                       *)
(* ================================================================ *)

(** A single input to the restraint controller. *)
Record input : Type := mk_input {
  phi_drift  : nat;
  step_count : nat;
  receipt_ok : bool
}.

(** Threshold constants, matching hardware RTL. *)
Definition PHI_DRIFT_THRESH  : nat := 164.
Definition STEP_COUNT_THRESH : nat := 10.

(* ================================================================ *)
(** ** 2.  State                                                       *)
(* ================================================================ *)

(** The reason bitvector encodes *which* condition(s) caused the trip.
    We model it as a list of booleans of fixed length 3:
      reason[0] = phi_drift trip
      reason[1] = step_count trip
      reason[2] = receipt trip
    The sticky flag [force_unknown] is stored separately. *)

Record state : Type := mk_state {
  force_unknown : bool;
  reason        : list bool   (* length = 3 *)
}.

(** Initial (reset) state. *)
Definition reset_state : state :=
  mk_state false [false; false; false].

(* ================================================================ *)
(** ** 3.  popcount helper                                            *)
(* ================================================================ *)

(** [popcount bs] counts the number of [true] entries in [bs]. *)
Fixpoint popcount (bs : list bool) : nat :=
  match bs with
  | []        => 0
  | b :: rest => (if b then 1 else 0) + popcount rest
  end.

(* ================================================================ *)
(** ** 4.  Single-step transition                                     *)
(* ================================================================ *)

(** The three trigger conditions, computed purely from [i]. *)
Definition cond_phi   (i : input) : bool := Nat.ltb PHI_DRIFT_THRESH  (phi_drift  i).
Definition cond_step  (i : input) : bool := Nat.ltb STEP_COUNT_THRESH (step_count i).
Definition cond_nrecv (i : input) : bool := negb (receipt_ok i).

(** The combined trigger. *)
Definition triggered (i : input) : bool :=
  orb (orb (cond_phi i) (cond_step i)) (cond_nrecv i).

(** [step_restraint s i] implements the RTL semantics:
    - If already tripped OR any condition fires, set force_unknown and
      record a one-hot reason vector for the *new* condition.
    - A pre-existing trip keeps force_unknown = true (sticky) with
      reason = [false;false;false] (no new causal bit, but flag held). *)
Definition step_restraint (s : state) (i : input) : state :=
  if force_unknown s
  then
    (* sticky: output stays high; reason cleared (no new single cause) *)
    mk_state true [false; false; false]
  else
    (* fresh evaluation *)
    let fu := triggered i in
    (* one-hot reason: only the highest-priority active bit is recorded *)
    let r :=
      if cond_phi i   then [true;  false; false]
      else if cond_step i  then [false; true;  false]
      else if cond_nrecv i then [false; false; true]
      else                      [false; false; false]
    in
    mk_state fu r.

(* ================================================================ *)
(** ** 5.  Helper lemmas                                              *)
(* ================================================================ *)

(** *** 5.1  Sticky: once tripped, remains tripped. *)
Lemma step_sticky :
  forall (s : state) (i : input),
    force_unknown s = true ->
    force_unknown (step_restraint s i) = true.
Proof.
  intros s i Hfu.
  unfold step_restraint.
  rewrite Hfu.
  simpl. reflexivity.
Qed.

(** *** 5.2  When tripped from fresh state, [force_unknown s' = triggered i]. *)
Lemma step_fresh_fu :
  forall (s : state) (i : input),
    force_unknown s = false ->
    force_unknown (step_restraint s i) = triggered i.
Proof.
  intros s i Hfu.
  unfold step_restraint.
  rewrite Hfu.
  simpl. reflexivity.
Qed.

(** *** 5.3  Reason vector is always length 3. *)
Lemma step_reason_length :
  forall (s : state) (i : input),
    length (reason (step_restraint s i)) = 3.
Proof.
  intros s i.
  unfold step_restraint.
  destruct (force_unknown s); simpl.
  - reflexivity.
  - destruct (cond_phi i); simpl; [reflexivity|].
    destruct (cond_step i); simpl; [reflexivity|].
    destruct (cond_nrecv i); simpl; reflexivity.
Qed.

(** *** 5.4  One-hot: popcount of reason ≤ 1. *)
Lemma step_reason_onehot :
  forall (s : state) (i : input),
    force_unknown (step_restraint s i) = true ->
    popcount (reason (step_restraint s i)) <= 1.
Proof.
  intros s i Hfu.
  unfold step_restraint in *.
  destruct (force_unknown s) eqn:Hs.
  - (* sticky branch: reason = [false;false;false], popcount = 0 *)
    simpl. lia.
  - (* fresh branch: destruct all three conditions *)
    destruct (cond_phi i) eqn:Hphi.
    + (* reason = [true;false;false], popcount = 1 *)
      simpl. lia.
    + destruct (cond_step i) eqn:Hstep.
      * (* reason = [false;true;false], popcount = 1 *)
        simpl. lia.
      * destruct (cond_nrecv i) eqn:Hnrecv.
        -- (* reason = [false;false;true], popcount = 1 *)
           simpl. lia.
        -- (* all conditions false => triggered = false,
               but force_unknown = true: contradiction *)
           (* Hfu : force_unknown (mk_state (triggered i) ...) = true
              after unfolding, triggered i = false *)
           unfold triggered, cond_phi, cond_step, cond_nrecv in *.
           rewrite Hphi in *. rewrite Hstep in *. rewrite Hnrecv in *.
           simpl in Hfu. discriminate.
Qed.

(** *** 5.5  Soundness of [triggered]: matches the disjunction in the spec. *)
Lemma triggered_spec :
  forall (i : input),
    triggered i = orb (orb (Nat.ltb 164 (phi_drift i))
                           (Nat.ltb 10 (step_count i)))
                      (negb (receipt_ok i)).
Proof.
  intros i.
  unfold triggered, cond_phi, cond_step, cond_nrecv,
         PHI_DRIFT_THRESH, STEP_COUNT_THRESH.
  reflexivity.
Qed.

(* ================================================================ *)
(** ** 6.  Main Theorems                                              *)
(* ================================================================ *)

(** *** Theorem 86A — Soundness (force_unknown = condition OR sticky)

    For any state [s] and input [i], either:
    (a) force_unknown s' equals the RTL disjunction, or
    (b) force_unknown was already true and remains true. *)
Theorem restraint_sound :
  forall (s : state) (i : input),
    let s' := step_restraint s i in
    force_unknown s' = orb (orb (Nat.ltb 164 (phi_drift i))
                                (Nat.ltb 10 (step_count i)))
                           (negb (receipt_ok i))
    \/ force_unknown s = true /\ force_unknown s' = true.
Proof.
  intros s i.
  unfold step_restraint.
  destruct (force_unknown s) eqn:Hfu.
  - (* sticky branch: force_unknown s = true, s' has force_unknown = true *)
    right. split.
    + (* force_unknown s = true, which is Hfu after destruct becomes true = true *)
      reflexivity.
    + reflexivity.
  - (* fresh branch: force_unknown s' = triggered i *)
    left.
    (* After unfolding and rewriting with Hfu = false, the goal is:
       triggered i = orb (orb ...) ... *)
    rewrite triggered_spec.
    reflexivity.
Qed.

(** *** Theorem 86B — Sticky property

    If force_unknown is set in state [s], it remains set after any
    two further transitions. *)
Theorem restraint_sticky :
  forall (s : state) (i1 i2 : input),
    force_unknown s = true ->
    force_unknown (step_restraint (step_restraint s i1) i2) = true.
Proof.
  intros s i1 i2 Hfu.
  apply step_sticky.
  apply step_sticky.
  exact Hfu.
Qed.

(** *** Theorem 86C — Reason one-hot

    When force_unknown is set, the reason bitvector has at most one
    bit set (popcount ≤ 1). *)
Theorem restraint_reason_onehot :
  forall (s : state) (i : input),
    force_unknown (step_restraint s i) = true ->
    popcount (reason (step_restraint s i)) <= 1.
Proof.
  intros s i Hfu.
  exact (step_reason_onehot s i Hfu).
Qed.

(* ================================================================ *)
(** ** 7.  Concrete sanity checks                                     *)
(* ================================================================ *)

(** phi_drift = 165 > 164: should trip. *)
Example trip_phi_drift :
  force_unknown (step_restraint reset_state
    (mk_input 165 0 true)) = true.
Proof. reflexivity. Qed.

(** step_count = 11 > 10: should trip. *)
Example trip_step_count :
  force_unknown (step_restraint reset_state
    (mk_input 0 11 true)) = true.
Proof. reflexivity. Qed.

(** receipt_ok = false: should trip. *)
Example trip_receipt :
  force_unknown (step_restraint reset_state
    (mk_input 0 0 false)) = true.
Proof. reflexivity. Qed.

(** All within bounds: should NOT trip. *)
Example no_trip_all_ok :
  force_unknown (step_restraint reset_state
    (mk_input 164 10 true)) = false.
Proof. reflexivity. Qed.

(** Sticky: trip once, stays tripped. *)
Example sticky_stays :
  force_unknown (step_restraint
    (step_restraint reset_state (mk_input 165 0 true))
    (mk_input 0 0 true)) = true.
Proof. reflexivity. Qed.

(** phi_drift = 164 exactly (not > 164): no trip. *)
Example boundary_phi_no_trip :
  force_unknown (step_restraint reset_state
    (mk_input 164 0 true)) = false.
Proof. reflexivity. Qed.

(** step_count = 10 exactly (not > 10): no trip. *)
Example boundary_step_no_trip :
  force_unknown (step_restraint reset_state
    (mk_input 0 10 true)) = false.
Proof. reflexivity. Qed.

(* ================================================================ *)
(** ** 8.  Summary                                                    *)
(* ================================================================ *)

(*
  Theorem index  | Name                      | QED | Admitted
  ---------------+---------------------------+-----+---------
  86A            | restraint_sound           |  ✓  |    0
  86B            | restraint_sticky          |  ✓  |    0
  86C            | restraint_reason_onehot   |  ✓  |    0
  ---------------------------------------------------------------
  Supporting lemmas (all QED):
    step_sticky, step_fresh_fu, step_reason_length,
    step_reason_onehot, triggered_spec
  ---------------------------------------------------------------
  Sanity-check examples (all ✓):
    trip_phi_drift, trip_step_count, trip_receipt,
    no_trip_all_ok, sticky_stays,
    boundary_phi_no_trip, boundary_step_no_trip
  ---------------------------------------------------------------
  Total: 8 QED, 0 Admitted.
  Compiled target: coqc 8.18+ / Rocq 9.x
*)
