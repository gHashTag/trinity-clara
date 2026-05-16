(** * CLARA Gap-5: Explainability Unit Soundness — Theorem 85

    Repository : gHashTag/trinity-clara
    Path       : proofs/clara_explainability_sound.v
    Issue      : CLARA Gap-5 (explainability_unit shift-register spec)
    Date       : 2026-05-17
    Author     : Trinity S³AI Research Group

    Anchor     : φ² + φ⁻² = 3  (Trinity Identity)
    DOI        : 10.5281/zenodo.19227877

    ---------------------------------------------------------------
    Informal statement
    ---------------------------------------------------------------
    Consider a shift register of depth MAX_STEPS = 10 that records
    inference steps in reverse-chronological order (most recent
    first).  After processing a list [steps] of inference steps:

    (A) If  length steps ≤ 10  then
          buffer_contents final_state = rev steps
          ∧  overflow final_state = false.

    (B) If  length steps > 10  then
          overflow final_state = true.

    (C) Sticky overflow: once set, overflow is never cleared.

    All three are proved below by structural induction on [steps].
    Zero uses of [Admitted].
    ---------------------------------------------------------------

    Compatibility: Coq 8.18+ / Rocq 9.x  (no non-standard imports)
*)

Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Require Import Coq.Bool.Bool.
Import ListNotations.

Set Implicit Arguments.

(* ================================================================ *)
(** ** 1.  Step type                                                  *)
(* ================================================================ *)

(** We treat inference steps as an abstract type parameterised by
    a carrier type [A].  All results are polymorphic. *)

Section ExplainabilityUnit.

Variable A : Type.           (* type of a single inference step *)

(* ================================================================ *)
(** ** 2.  Shift-register state                                       *)
(* ================================================================ *)

(** [MAX_STEPS] is the hardware depth of the shift register. *)
Definition MAX_STEPS : nat := 10.

(** The state of the explainability unit:
      - [buffer]   : the recorded steps, most-recent first (head = newest)
      - [overflow] : sticky flag — set once more than MAX_STEPS steps
                     have been pushed *)
Record expl_state : Type := mk_state {
  buffer   : list A;
  overflow : bool
}.

(** The empty initial state. *)
Definition empty_state : expl_state :=
  mk_state [] false.

(* ================================================================ *)
(** ** 3.  Single-step update                                         *)
(* ================================================================ *)

(** Pushing one step into the shift register:
    - Prepend the step to the buffer (reverse-chronological order).
    - If the buffer already has MAX_STEPS entries, set overflow and
      drop the oldest entry so the buffer stays at most MAX_STEPS
      deep.  The overflow flag is sticky. *)
Definition push_step (s : expl_state) (x : A) : expl_state :=
  let new_buf := x :: buffer s in
  if Nat.leb MAX_STEPS (length (buffer s))
  then mk_state (firstn MAX_STEPS new_buf) true
  else mk_state new_buf (overflow s).

(* ================================================================ *)
(** ** 4.  Simulation: fold a list of steps                           *)
(* ================================================================ *)

(** [simulate_explainability] folds [steps] left-to-right over the
    state — each element is processed in order, consistent with the
    hardware.  After processing, the buffer contains the steps in
    reverse order (most-recent = head). *)
Definition simulate_explainability (init : expl_state) (steps : list A)
    : expl_state :=
  fold_left push_step steps init.

(* ================================================================ *)
(** ** 5.  Helper lemmas                                              *)
(* ================================================================ *)

(** *** 5.1  Length invariant: buffer length ≤ MAX_STEPS always *)
Lemma push_step_length_le :
  forall (s : expl_state) (x : A),
    length (buffer s) <= MAX_STEPS ->
    length (buffer (push_step s x)) <= MAX_STEPS.
Proof.
  intros s x Hle.
  unfold push_step, MAX_STEPS in *.
  simpl.
  destruct (Nat.leb 10 (length (buffer s))) eqn:Heq.
  - (* overflow branch: firstn 10 (x :: buffer s) *)
    simpl.
    rewrite firstn_length.
    (* firstn_length: length (firstn 10 ...) = Nat.min 10 (length ...) *)
    (* Nat.min 10 n <= 10 always *)
    apply Nat.le_min_l.
  - (* normal branch: x :: buffer s *)
    simpl. lia.
Qed.

Lemma simulate_length_le :
  forall (steps : list A) (s : expl_state),
    length (buffer s) <= MAX_STEPS ->
    length (buffer (simulate_explainability s steps)) <= MAX_STEPS.
Proof.
  induction steps as [| x rest IH]; intros s Hle.
  - (* base *) simpl. exact Hle.
  - (* step *) simpl.
    apply IH.
    apply push_step_length_le.
    exact Hle.
Qed.

(** *** 5.2  Overflow sticky: once true, stays true *)
Lemma push_step_overflow_sticky :
  forall (s : expl_state) (x : A),
    overflow s = true ->
    overflow (push_step s x) = true.
Proof.
  intros s x Hov.
  unfold push_step.
  destruct (Nat.leb MAX_STEPS (length (buffer s))); simpl; auto.
Qed.

Lemma simulate_overflow_sticky :
  forall (steps : list A) (s : expl_state),
    overflow s = true ->
    overflow (simulate_explainability s steps) = true.
Proof.
  induction steps as [| x rest IH]; intros s Hov.
  - simpl. exact Hov.
  - simpl.
    apply IH.
    apply push_step_overflow_sticky.
    exact Hov.
Qed.

(** *** 5.3  Under capacity: push preserves buffer = rev prefix *)
(** When the buffer length is strictly less than MAX_STEPS, pushing
    a new step simply conses it onto the front and leaves overflow
    unchanged. *)
Lemma push_step_under_cap :
  forall (s : expl_state) (x : A),
    length (buffer s) < MAX_STEPS ->
    buffer (push_step s x) = x :: buffer s /\
    overflow (push_step s x) = overflow s.
Proof.
  intros s x Hlt.
  unfold push_step, MAX_STEPS in *.
  assert (Hle: Nat.leb 10 (length (buffer s)) = false).
  { apply Nat.leb_gt. exact Hlt. }
  rewrite Hle.
  simpl. split; reflexivity.
Qed.

(** *** 5.4  Under capacity: simulation gives rev steps when init is
             empty and steps fit *)
Lemma simulate_under_cap_buffer :
  forall (steps : list A),
    length steps <= MAX_STEPS ->
    buffer (simulate_explainability empty_state steps) = rev steps.
Proof.
  intros steps Hle.
  (* We prove the more general statement by induction with an
     accumulator that tracks what has been processed so far. *)
  (* Generalise to: for any prefix acc already processed,
       buffer (simulate_explainability (mk_state (rev acc) false) rest)
       = rev (acc ++ rest)
     We prove this for acc = [] which gives the desired result. *)
  assert (Hgen :
    forall (rest : list A) (acc : list A),
      length acc + length rest <= MAX_STEPS ->
      buffer (simulate_explainability (mk_state (rev acc) false) rest)
      = rev (acc ++ rest)).
  {
    intros rest.
    induction rest as [| x tl IH]; intros acc Hacc.
    - (* base: rest = [] *)
      simpl.
      rewrite app_nil_r.
      reflexivity.
    - (* step: rest = x :: tl *)
      simpl.
      (* After pushing x onto mk_state (rev acc) false: *)
      assert (Hpush : push_step (mk_state (rev acc) false) x
                      = mk_state (x :: rev acc) false).
      {
        unfold push_step, MAX_STEPS. simpl.
        assert (Hlt : Nat.leb 10 (length (rev acc)) = false).
        { apply Nat.leb_gt.
          rewrite List.rev_length.
          simpl in Hacc. lia. }
        rewrite Hlt. reflexivity.
      }
      rewrite Hpush.
      (* Now state is mk_state (x :: rev acc) false.
         Note: x :: rev acc = rev (acc ++ [x]).         *)
      assert (Hrev_eq : x :: rev acc = rev (acc ++ [x])).
      { rewrite rev_app_distr. simpl. reflexivity. }
      rewrite Hrev_eq.
      (* Apply IH with acc' = acc ++ [x] *)
      assert (Hacc' : length (acc ++ [x]) + length tl <= MAX_STEPS).
      { rewrite app_length. simpl in *. lia. }
      specialize (IH (acc ++ [x]) Hacc').
      (* IH: buffer (simulate_explainability (mk_state (rev (acc++[x])) false) tl)
               = rev ((acc++[x]) ++ tl)                                             *)
      rewrite IH.
      (* Goal: rev ((acc ++ [x]) ++ tl) = rev (acc ++ x :: tl) *)
      rewrite app_assoc. simpl. reflexivity.
  }
  specialize (Hgen steps [] Hle).
  simpl in Hgen.
  exact Hgen.
Qed.

(** *** 5.5  Under capacity: simulation keeps overflow = false *)
Lemma simulate_under_cap_overflow :
  forall (steps : list A),
    length steps <= MAX_STEPS ->
    overflow (simulate_explainability empty_state steps) = false.
Proof.
  assert (Hgen :
    forall (rest : list A) (acc : list A),
      length acc + length rest <= MAX_STEPS ->
      overflow (simulate_explainability (mk_state (rev acc) false) rest)
      = false).
  {
    intros rest.
    induction rest as [| x tl IH]; intros acc Hacc.
    - simpl. reflexivity.
    - simpl.
      assert (Hpush : push_step (mk_state (rev acc) false) x
                      = mk_state (x :: rev acc) false).
      {
        unfold push_step, MAX_STEPS. simpl.
        assert (Hlt : Nat.leb 10 (length (rev acc)) = false).
        { apply Nat.leb_gt.
          rewrite List.rev_length.
          simpl in Hacc. lia. }
        rewrite Hlt. reflexivity.
      }
      rewrite Hpush.
      assert (Hrev_eq2 : x :: rev acc = rev (acc ++ [x])).
      { rewrite rev_app_distr. simpl. reflexivity. }
      rewrite Hrev_eq2.
      apply IH.
      rewrite app_length. simpl in *. lia.
  }
  intros steps Hle.
  specialize (Hgen steps [] Hle).
  simpl in Hgen.
  exact Hgen.
Qed.

(** *** 5.6  Over capacity: overflow is set *)
(** When we push more than MAX_STEPS steps, the overflow flag is set. *)
Lemma push_step_at_cap_overflow :
  forall (s : expl_state) (x : A),
    length (buffer s) >= MAX_STEPS ->
    overflow (push_step s x) = true.
Proof.
  intros s x Hge.
  unfold push_step, MAX_STEPS in *.
  assert (Hleb : Nat.leb 10 (length (buffer s)) = true).
  { apply Nat.leb_le. exact Hge. }
  rewrite Hleb. simpl. reflexivity.
Qed.

(** When list is longer than MAX_STEPS, after simulation overflow = true. *)
Lemma simulate_over_cap_overflow :
  forall (steps : list A),
    length steps > MAX_STEPS ->
    overflow (simulate_explainability empty_state steps) = true.
Proof.
  (* We split steps into a prefix of length MAX_STEPS+1 and a suffix. *)
  intros steps Hgt.
  (* Use the fact that after MAX_STEPS+1 steps, overflow is set,
     and by the sticky lemma it stays set. *)
  assert (Hge : length steps >= MAX_STEPS + 1) by lia.
  (* Decompose: steps = first (MAX_STEPS+1) steps ++ drop (MAX_STEPS+1) steps *)
  remember (firstn (MAX_STEPS + 1) steps) as prefix.
  remember (skipn  (MAX_STEPS + 1) steps) as suffix.
  assert (Hsteps : steps = prefix ++ suffix).
  { subst. rewrite firstn_skipn. reflexivity. }
  assert (Hplen : length prefix = MAX_STEPS + 1).
  { subst. rewrite List.firstn_length.
    apply Nat.min_l. unfold MAX_STEPS in *. lia. }
  (* simulate_explainability empty_state steps
     = simulate_explainability
         (simulate_explainability empty_state prefix) suffix *)
  rewrite Hsteps.
  (* Rewrite using fold_left_app at the simulate_explainability level *)
  assert (Hsplit : simulate_explainability empty_state (prefix ++ suffix)
                  = simulate_explainability
                      (simulate_explainability empty_state prefix)
                      suffix).
  { unfold simulate_explainability. rewrite fold_left_app. reflexivity. }
  rewrite Hsplit.
  (* Show that after processing prefix, overflow = true *)
  apply simulate_overflow_sticky.
  (* Now we need: overflow (simulate_explainability empty_state prefix) = true *)
  (* prefix = firstn (MAX_STEPS+1) steps.
     We further split prefix into firstn MAX_STEPS steps ++ [last_step]. *)
  assert (Hpge : length prefix >= MAX_STEPS + 1) by lia.
  (* Decompose prefix = inner ++ [last] where length inner = MAX_STEPS *)
  remember (firstn MAX_STEPS prefix) as inner.
  remember (skipn  MAX_STEPS prefix) as last_part.
  assert (Hprefix : prefix = inner ++ last_part).
  { subst. rewrite firstn_skipn. reflexivity. }
  assert (Hilen : length inner = MAX_STEPS).
  { subst. rewrite List.firstn_length.
    apply Nat.min_l. lia. }
  assert (Hllen : length last_part = 1).
  { assert (Happ_len : length inner + length last_part = length prefix).
    { subst. rewrite <- app_length. rewrite firstn_skipn. reflexivity. }
    lia. }
  (* last_part = [x] for some x *)
  destruct last_part as [| x rest_lp].
  - simpl in Hllen. discriminate.
  - assert (Hrest : rest_lp = []).
    { destruct rest_lp. reflexivity. simpl in Hllen. lia. }
    subst rest_lp.
    (* prefix = inner ++ [x], simulate over it *)
    rewrite Hprefix.
    (* Goal: overflow (simulate_explainability empty_state (inner ++ [x])) = true *)
    assert (Hilen_le : length inner <= MAX_STEPS) by lia.
    (* Key facts about the intermediate state after processing inner *)
    assert (Hmid_buf : buffer (simulate_explainability empty_state inner) = rev inner).
    { exact (simulate_under_cap_buffer inner Hilen_le). }
    assert (Hmid_ov : overflow (simulate_explainability empty_state inner) = false).
    { exact (simulate_under_cap_overflow inner Hilen_le). }
    assert (Hbuflen : length (buffer (simulate_explainability empty_state inner))
                      = MAX_STEPS).
    { rewrite Hmid_buf. rewrite List.rev_length. exact Hilen. }
    (* Unroll: simulate_explainability empty_state (inner ++ [x])
                = simulate_explainability (simulate_explainability empty_state inner) [x]
                = push_step (simulate_explainability empty_state inner) x *)
    unfold simulate_explainability.
    rewrite fold_left_app.
    (* Goal: overflow (fold_left push_step [x]
                        (fold_left push_step inner empty_state)) = true *)
    simpl fold_left.
    (* Goal: overflow (push_step (fold_left push_step inner empty_state) x) = true *)
    (* Restate using simulate_explainability for applying push_step_at_cap_overflow *)
    fold (simulate_explainability empty_state inner).
    apply push_step_at_cap_overflow.
    lia.
Qed.

(* ================================================================ *)
(** ** 6.  Main Theorems                                              *)
(* ================================================================ *)

(** *** Theorem 85A — Soundness (within capacity)

    For any sequence of inference steps of length ≤ MAX_STEPS (= 10),
    the explainability unit:
    (1) records them in reverse-chronological order, and
    (2) does NOT set the overflow flag. *)
(** [buffer_contents] is a transparent alias for [buffer],
    matching the informal spec's terminology. *)
Definition buffer_contents (s : expl_state) : list A := buffer s.

Theorem explainability_sound :
  forall (steps : list A),
    length steps <= MAX_STEPS ->
    let final_state := simulate_explainability empty_state steps in
    buffer_contents final_state = rev steps /\
    overflow final_state = false.
Proof.
  intros steps Hle.
  unfold buffer_contents.
  split.
  - (* buffer = rev steps *)
    exact (simulate_under_cap_buffer steps Hle).
  - (* overflow = false *)
    exact (simulate_under_cap_overflow steps Hle).
Qed.

(** *** Theorem 85B — Overflow soundness (beyond capacity)

    For any sequence of more than MAX_STEPS steps, the overflow
    flag is set (sticky). *)
Theorem explainability_overflow :
  forall (steps : list A),
    length steps > MAX_STEPS ->
    overflow (simulate_explainability empty_state steps) = true.
Proof.
  intros steps Hgt.
  exact (simulate_over_cap_overflow steps Hgt).
Qed.

(** *** Theorem 85C — Overflow is sticky

    If the explainability unit is in overflow, it stays in overflow
    regardless of further steps processed. *)
Theorem explainability_overflow_sticky :
  forall (steps_extra : list A) (s : expl_state),
    overflow s = true ->
    overflow (simulate_explainability s steps_extra) = true.
Proof.
  intros steps_extra s Hov.
  exact (simulate_overflow_sticky steps_extra s Hov).
Qed.

End ExplainabilityUnit.

(* ================================================================ *)
(** ** 7.  Instantiation: nat steps (concrete sanity check)           *)
(* ================================================================ *)

(** Sanity check: instantiate with [nat] as the step type.
    [Set Implicit Arguments] makes [A] implicit; Coq infers it
    from the list literal. *)

(** Compute the final state for concrete nat-step lists. *)
Definition run_nat (steps : list nat) : expl_state :=
  simulate_explainability empty_state steps.

Example sound_5_steps :
  buffer (run_nat [1; 2; 3; 4; 5]) = rev [1; 2; 3; 4; 5] /\
  overflow (run_nat [1; 2; 3; 4; 5]) = false.
Proof.
  split; reflexivity.
Qed.

Example overflow_11_steps :
  overflow (run_nat [1;2;3;4;5;6;7;8;9;10;11]) = true.
Proof.
  reflexivity.
Qed.

Example no_overflow_10_steps :
  overflow (run_nat [1;2;3;4;5;6;7;8;9;10]) = false.
Proof.
  reflexivity.
Qed.

(* ================================================================ *)
(** ** 8.  Summary                                                    *)
(* ================================================================ *)

(*
  Theorem index  | Name                           | QED | Admitted
  ---------------+--------------------------------+-----+---------
  85A            | explainability_sound           |  ✓  |    0
  85B            | explainability_overflow        |  ✓  |    0
  85C            | explainability_overflow_sticky |  ✓  |    0
  ---------------------------------------------------------------
  Supporting lemmas (all QED):
    push_step_length_le, simulate_length_le,
    push_step_overflow_sticky, simulate_overflow_sticky,
    push_step_under_cap, simulate_under_cap_buffer,
    simulate_under_cap_overflow, push_step_at_cap_overflow,
    simulate_over_cap_overflow
  ---------------------------------------------------------------
  Total: 12 QED, 0 Admitted.
  Compiled target: coqc 8.18+ / Rocq 9.x
*)
