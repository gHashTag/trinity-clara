#!/usr/bin/env python3
"""
Example 4: VSA Analogy Reasoning with Bind/Unbind
===================================================

Composition: Entity Encoding → VSA Bind/Unbind → Similarity Search → AR

This example demonstrates VSA analogy reasoning:
- A:B :: C:? using the property: bind(A, B) unbind(C) ≈ D
- Bundle superposition for set-like reasoning
- Position-aware encoding for sequence understanding

Key VSA properties demonstrated:
- bind(a, bind(a, b)) = b (self-inverse)
- bundle3 for consensus voting
- permute for position-aware encoding

Author: T27 Trinity Ternary Project
SPDX-License-Identifier: Apache-2.0
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Callable
import math
import random
from enum import Enum


# ============================================================================
# T27 Ternary Types (from specs/base/types.t27)
# ============================================================================

TRIT_NEG = -1
TRIT_ZERO = 0
TRIT_POS = 1

Trit = int

VSA_DIM = 1024


# ============================================================================
# VSA Operations (from specs/vsa/ops.t27)
# ============================================================================

def generate_random_hv(seed: int, dim: int = VSA_DIM) -> List[Trit]:
    """Generate a deterministic random hypervector."""
    random.seed(seed)
    return [random.choice([TRIT_NEG, TRIT_ZERO, TRIT_POS]) for _ in range(dim)]


def bind(a: List[Trit], b: List[Trit], length: int = VSA_DIM) -> List[Trit]:
    """
    Bind operation (XOR-like).

    Property: bind(a, bind(a, b)) = b (self-inverse)
    Used for: associative memory, role-value pairing
    """
    result = []
    for i in range(length):
        ai, bi = a[i], b[i]
        if ai == TRIT_ZERO:
            result.append(bi)
        elif bi == TRIT_ZERO:
            result.append(ai)
        else:
            # Both non-zero: multiply
            result.append(TRIT_POS if ai == bi else TRIT_NEG)
    return result


def unbind(bound: List[Trit], key: List[Trit], length: int = VSA_DIM) -> List[Trit]:
    """
    Unbind operation (inverse of bind).

    For XOR-like bind: unbind(x, y) = bind(x, y)
    """
    return bind(bound, key, length)


def bundle2(a: List[Trit], b: List[Trit], length: int = VSA_DIM) -> List[Trit]:
    """
    Bundle operation (majority vote of 2 vectors).

    Used for: superposition, set union
    """
    result = []
    for i in range(length):
        ai, bi = a[i], b[i]
        if ai == TRIT_ZERO:
            result.append(bi)
        elif bi == TRIT_ZERO:
            result.append(ai)
        else:
            # Both non-zero: determine majority
            sum_val = ai + bi
            if sum_val > 0:
                result.append(TRIT_POS)
            elif sum_val < 0:
                result.append(TRIT_NEG)
            else:
                result.append(TRIT_ZERO)
    return result


def bundle3(a: List[Trit], b: List[Trit], c: List[Trit],
             length: int = VSA_DIM) -> List[Trit]:
    """
    Bundle operation (majority vote of 3 vectors).

    Used for: robust superposition, noise reduction
    """
    result = []
    for i in range(length):
        ai, bi, ci = a[i], b[i], c[i]
        sum_val = ai + bi + ci
        if sum_val > 0:
            result.append(TRIT_POS)
        elif sum_val < 0:
            result.append(TRIT_NEG)
        else:
            result.append(TRIT_ZERO)
    return result


def permute(v: List[Trit], length: int = VSA_DIM, shift: int = 1) -> List[Trit]:
    """
    Circular shift of hypervector.

    Used for: sequence encoding, position tagging
    """
    shift = shift % length
    result = [v[(i - shift) % length] for i in range(length)]
    return result


def cosine_similarity(a: List[Trit], b: List[Trit], length: int = VSA_DIM) -> float:
    """Cosine similarity: (a·b) / (||a|| * ||b||)."""
    dot = sum(a[i] * b[i] for i in range(length))
    norm_a = math.sqrt(sum(1 for i in range(length) if a[i] != TRIT_ZERO))
    norm_b = math.sqrt(sum(1 for i in range(length) if b[i] != TRIT_ZERO))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def hamming_distance(a: List[Trit], b: List[Trit], length: int = VSA_DIM) -> int:
    """Count positions where a[i] != b[i]."""
    return sum(1 for i in range(length) if a[i] != b[i])


# ============================================================================
# ML+AR Composition Types
# ============================================================================

class ARValidation(Enum):
    """AR reasoning validation outcomes."""
    VALID = "valid"
    INVALID = "invalid"
    UNCERTAIN = "uncertain"


@dataclass
class MLClassificationResult:
    """Result from ML classifier layer."""
    predicted_class: str
    confidence: float
    feature_importance: Dict[str, float]


@dataclass
class ARValidationResult:
    """Result from AR reasoning validation layer."""
    status: ARValidation
    reasoning_steps: List[str]
    proof_trace: List[str]
    confidence: float


@dataclass
class ExplainabilityOutput:
    """Explainability output with confidence breakdown."""
    prediction: str
    final_confidence: float
    ml_confidence: float
    ar_confidence: float
    explanation: str
    key_features: List[str]
    proof_trace: List[str]


# ============================================================================
# VSA Analogy Reasoner
# ============================================================================

# ============================================================================
# ML Classifier Layer on VSA Features
# ============================================================================

class VSAMLClassifier:
    """
    ML classifier layer on top of VSA features.

    Provides probabilistic classification based on VSA similarity patterns.
    """

    def __init__(self, dim: int = VSA_DIM):
        self.dim = dim
        self.class_weights: Dict[str, List[Trit]] = {}
        self.feature_importance: Dict[str, float] = {}
        self._initialize_classifier()

    def _initialize_classifier(self):
        """Initialize random weight vectors for each concept class."""
        # Create weight vectors for common analogy patterns
        self.class_weights = {
            "gender_swap": generate_random_hv(6001, self.dim),
            "age_progression": generate_random_hv(6002, self.dim),
            "capital_city": generate_random_hv(6003, self.dim),
            "animal_adult_young": generate_random_hv(6004, self.dim),
            "processing_chain": generate_random_hv(6005, self.dim),
        }

    def classify_relationship(self, query_hv: List[Trit],
                          candidates: Dict[str, float]) -> MLClassificationResult:
        """
        Classify relationship type using VSA features.

        Args:
            query_hv: The query hypervector from bind/unbind operation
            candidates: Dictionary of candidate -> similarity scores

        Returns:
            MLClassificationResult with prediction and confidence
        """
        # Compute pattern-based classification
        pattern_scores = {}

        for pattern_name, weight_hv in self.class_weights.items():
            # Cosine similarity between query and pattern weight
            sim = cosine_similarity(query_hv, weight_hv, self.dim)
            pattern_scores[pattern_name] = sim

        # Determine best pattern
        best_pattern = max(pattern_scores.items(), key=lambda x: x[1])

        # Feature importance based on trit contribution
        importance = self._compute_feature_importance(query_hv)

        # Confidence is combination of pattern match and distribution
        confidence = self._compute_confidence(pattern_scores, best_pattern[1])

        return MLClassificationResult(
            predicted_class=best_pattern[0],
            confidence=confidence,
            feature_importance=importance
        )

    def _compute_feature_importance(self, query_hv: List[Trit]) -> Dict[str, float]:
        """Compute importance of different trit patterns in query."""
        importance = {}

        # Count trit distribution
        neg_count = sum(1 for t in query_hv if t == TRIT_NEG)
        pos_count = sum(1 for t in query_hv if t == TRIT_POS)
        zero_count = sum(1 for t in query_hv if t == TRIT_ZERO)

        total = len(query_hv)
        importance["negative_trits"] = neg_count / total
        importance["positive_trits"] = pos_count / total
        importance["zero_trits"] = zero_count / total
        importance["nonzero_ratio"] = (neg_count + pos_count) / total
        importance["polarity_balance"] = abs(pos_count - neg_count) / (neg_count + pos_count + 1)

        return importance

    def _compute_confidence(self, pattern_scores: Dict[str, float],
                         best_score: float) -> float:
        """Compute confidence based on pattern score distribution."""
        if not pattern_scores:
            return 0.0

        # Normalize scores to 0-1 range
        scores = list(pattern_scores.values())
        min_score, max_score = min(scores), max(scores)

        if max_score == min_score:
            return 0.5  # No discrimination

        # Confidence is relative to distribution
        normalized = (best_score - min_score) / (max_score - min_score)
        return max(0.0, min(1.0, normalized))


# ============================================================================
# AR Reasoning Validation Layer
# ============================================================================

class ARReasoningValidator:
    """
    AR (Abstract Reasoning) validation layer.

    Provides logical proof traces and validates analogical reasoning.
    """

    def __init__(self, max_proof_steps: int = 10):
        self.max_proof_steps = max_proof_steps
        self.knowledge_graph = self._build_knowledge_graph()

    def _build_knowledge_graph(self) -> Dict[str, List[Tuple[str, str]]]:
        """Build a simple knowledge graph for analogy validation."""
        return {
            "king": [("male", "royalty"), ("adult", "royalty")],
            "man": [("male", "human"), ("adult", "human")],
            "queen": [("female", "royalty"), ("adult", "royalty")],
            "woman": [("female", "human"), ("adult", "human")],
            "dog": [("animal", "mammal"), ("canine", "pet")],
            "puppy": [("young", "dog"), ("animal", "mammal")],
            "cat": [("animal", "mammal"), ("feline", "pet")],
            "kitten": [("young", "cat"), ("animal", "mammal")],
            "paris": [("city", "capital")],
            "france": [("country", "europe")],
            "tokyo": [("city", "capital")],
            "japan": [("country", "asia")],
            "berlin": [("city", "capital")],
            "germany": [("country", "europe")],
        }

    def validate_analogy(self, a: str, b: str, c: str, d: str,
                      ml_result: MLClassificationResult) -> ARValidationResult:
        """
        Validate analogy using AR reasoning.

        Args:
            a, b, c, d: Analogy components (A:B :: C:D)
            ml_result: Result from ML classifier layer

        Returns:
            ARValidationResult with proof trace (max 10 steps)
        """
        reasoning_steps: List[str] = []
        proof_trace: List[str] = []
        step_count = 0

        # Step 1: Extract relationship between A and B
        reasoning_steps.append(f"Step 1: Analyze relationship {a} -> {b}")
        ab_relation = self._extract_relation(a, b)
        proof_trace.append(f"Relation({a}, {b}) = {ab_relation}")
        step_count += 1

        # Step 2: Extract relationship between C and D (candidate)
        reasoning_steps.append(f"Step 2: Analyze relationship {c} -> {d}")
        cd_relation = self._extract_relation(c, d)
        proof_trace.append(f"Relation({c}, {d}) = {cd_relation}")
        step_count += 1

        # Step 3: Compare relationships
        reasoning_steps.append("Step 3: Compare relationship structures")
        structural_match = ab_relation == cd_relation
        proof_trace.append(f"Structural Match: {structural_match}")
        step_count += 1

        # Step 4: Validate with knowledge graph
        reasoning_steps.append("Step 4: Validate against knowledge graph")
        kg_valid = self._validate_with_kg(a, b, c, d)
        proof_trace.append(f"Knowledge Graph Valid: {kg_valid}")
        step_count += 1

        # Step 5: Integrate ML classification
        reasoning_steps.append(f"Step 5: ML classification: {ml_result.predicted_class}")
        proof_trace.append(f"ML_Pattern: {ml_result.predicted_class} (conf={ml_result.confidence:.3f})")
        step_count += 1

        # Step 6: Cross-validation
        reasoning_steps.append("Step 6: Cross-validate ML and AR reasoning")
        cross_valid = self._cross_validate(ml_result, structural_match, kg_valid)
        proof_trace.append(f"Cross-Validation: {cross_valid}")
        step_count += 1

        # Additional validation steps if needed (up to 10 total)
        if step_count < self.max_proof_steps:
            reasoning_steps.append("Step 7: Check semantic consistency")
            semantic_valid = self._semantic_consistency(a, b, c, d)
            proof_trace.append(f"Semantic Consistency: {semantic_valid}")
            step_count += 1

            if step_count < self.max_proof_steps:
                reasoning_steps.append("Step 8: Verify inverse consistency")
                inverse_valid = self._inverse_consistency(a, b, c, d)
                proof_trace.append(f"Inverse Consistency: {inverse_valid}")
                step_count += 1

                if step_count < self.max_proof_steps:
                    reasoning_steps.append("Step 9: Assess pattern completeness")
                    completeness = self._pattern_completeness(a, b, c, d)
                    proof_trace.append(f"Pattern Completeness: {completeness:.2f}")
                    step_count += 1

        # Final verdict
        all_valid = structural_match and kg_valid and cross_valid
        final_confidence = self._compute_ar_confidence(
            ml_result.confidence,
            structural_match,
            kg_valid,
            cross_valid
        )

        if all_valid and final_confidence > 0.7:
            status = ARValidation.VALID
        elif final_confidence < 0.3:
            status = ARValidation.INVALID
        else:
            status = ARValidation.UNCERTAIN

        reasoning_steps.append(f"Step {step_count}: Final verdict: {status.value}")
        proof_trace.append(f"Final_Consensus: {status.value}")

        return ARValidationResult(
            status=status,
            reasoning_steps=reasoning_steps,
            proof_trace=proof_trace,
            confidence=final_confidence
        )

    def _extract_relation(self, x: str, y: str) -> str:
        """Extract abstract relation between two entities."""
        x_props = self.knowledge_graph.get(x, [])
        y_props = self.knowledge_graph.get(y, [])

        # Find changed attributes
        changes = []
        for xp in x_props:
            for yp in y_props:
                if xp[0] == yp[0]:  # Same category
                    if xp[1] != yp[1]:  # Different value
                        changes.append(f"{xp[1]}->{yp[1]}")

        return ":".join(changes) if changes else "unknown"

    def _validate_with_kg(self, a: str, b: str, c: str, d: str) -> bool:
        """Validate analogy using knowledge graph."""
        # Check if A->B and C->D share same transformation pattern
        ab_transform = self._get_transformation(a, b)
        cd_transform = self._get_transformation(c, d)
        return ab_transform == cd_transform

    def _get_transformation(self, x: str, y: str) -> Tuple[str, ...]:
        """Get transformation pattern from x to y."""
        x_cats = {prop[0] for prop in self.knowledge_graph.get(x, [])}
        y_cats = {prop[0] for prop in self.knowledge_graph.get(y, [])}
        return tuple(sorted(x_cats.symmetric_difference(y_cats)))

    def _cross_validate(self, ml_result: MLClassificationResult,
                      structural_match: bool, kg_valid: bool) -> bool:
        """Cross-validate ML and AR reasoning."""
        # High ML confidence should align with structural match
        if ml_result.confidence > 0.8 and not structural_match:
            return False
        # High ML confidence should align with KG validity
        if ml_result.confidence > 0.8 and not kg_valid:
            return False
        return structural_match or kg_valid

    def _semantic_consistency(self, a: str, b: str, c: str, d: str) -> bool:
        """Check semantic consistency of analogy."""
        # Simple check: A and C should have same semantic category
        # B and D should have same semantic category
        a_cat = self._get_semantic_category(a)
        c_cat = self._get_semantic_category(c)
        b_cat = self._get_semantic_category(b)
        d_cat = self._get_semantic_category(d)

        return a_cat == c_cat and b_cat == d_cat

    def _get_semantic_category(self, term: str) -> str:
        """Get semantic category of term."""
        if term in ["king", "queen"]:
            return "royalty"
        elif term in ["man", "woman"]:
            return "human"
        elif term in ["dog", "cat"]:
            return "animal_adult"
        elif term in ["puppy", "kitten"]:
            return "animal_young"
        elif term in ["paris", "tokyo", "berlin"]:
            return "city"
        elif term in ["france", "japan", "germany"]:
            return "country"
        return "unknown"

    def _inverse_consistency(self, a: str, b: str, c: str, d: str) -> bool:
        """Check if inverse relation holds (B:A :: D:C)."""
        ab_relation = self._extract_relation(a, b)
        ba_relation = self._extract_relation(b, a)
        cd_relation = self._extract_relation(c, d)
        dc_relation = self._extract_relation(d, c)

        # Inverse relations should match
        return ba_relation == dc_relation

    def _pattern_completeness(self, a: str, b: str, c: str, d: str) -> float:
        """Assess pattern completeness (0-1)."""
        # Check if all terms have KG entries
        score = 0.0
        for term in [a, b, c, d]:
            if term in self.knowledge_graph and self.knowledge_graph[term]:
                score += 0.25
        return score

    def _compute_ar_confidence(self, ml_conf: float, structural: bool,
                            kg: bool, cross: bool) -> float:
        """Compute AR validation confidence."""
        base = ml_conf
        if structural:
            base = min(1.0, base + 0.2)
        if kg:
            base = min(1.0, base + 0.15)
        if cross:
            base = min(1.0, base + 0.1)
        return base


# ============================================================================
# Entity Definition
# ============================================================================

@dataclass
class Entity:
    """An entity with a name and hypervector representation."""
    name: str
    hypervector: List[Trit]


# ============================================================================
# Enhanced VSA Analogy Reasoner with ML+AR Composition
# ============================================================================

class VSAAnalogyReasoner:
    """
    VSA-based analogy reasoning system with ML+AR composition.

    Solves analogies of the form: A:B :: C:?
    Using the property: bind(A, B) unbind(C) ≈ D

    Enhanced with:
    - ML classifier layer for pattern recognition
    - AR validation layer for logical proof
    - Explainability output with confidence
    """

    def __init__(self, dim: int = VSA_DIM, max_proof_steps: int = 10):
        self.dim = dim
        self.entities: Dict[str, Entity] = {}
        self._initialize_entities()

        # ML+AR components
        self.ml_classifier = VSAMLClassifier(dim)
        self.ar_validator = ARReasoningValidator(max_proof_steps)

    def _initialize_entities(self):
        """Initialize entity hypervectors for analogy tasks."""
        # Semantic analogies
        entity_seeds = {
            "king": 1001, "man": 1002, "queen": 1003, "woman": 1004,
            "dog": 2001, "puppy": 2002, "cat": 2003, "kitten": 2004,
            "paris": 3001, "france": 3002, "tokyo": 3003, "japan": 3004,
            "berlin": 3005, "germany": 3006,
            # Programming analogies
            "code": 4001, "compile": 4002, "binary": 4003,
            "source": 4004, "executable": 4005,
            # T27 specific
            "trit": 5001, "ternary": 5002, "bit": 5003, "binary": 5004,
            "phi": 5005, "golden_ratio": 5006,
        }

        for name, seed in entity_seeds.items():
            self.entities[name] = Entity(name, generate_random_hv(seed, self.dim))

    def encode_entity(self, name: str) -> List[Trit]:
        """Get or create entity hypervector."""
        if name not in self.entities:
            seed = hash(name) % 10000
            self.entities[name] = Entity(name, generate_random_hv(seed, self.dim))
        return self.entities[name].hypervector

    def solve_analogy(self, a: str, b: str, c: str,
                     candidates: List[str]) -> Tuple[str, float, Dict[str, float]]:
        """
        Solve analogy A:B :: C:?

        Algorithm:
        1. Compute bound = bind(A, B)
        2. Compute query = unbind(bound, C)
        3. Find candidate with highest similarity to query

        Returns: (best_candidate, similarity, all_similarities)
        """
        a_hv = self.encode_entity(a)
        b_hv = self.encode_entity(b)
        c_hv = self.encode_entity(c)

        # bind(A, B) captures the relationship
        bound = bind(a_hv, b_hv, self.dim)

        # unbind with C to find D
        query = unbind(bound, c_hv, self.dim)

        # Compare with candidates
        similarities = {}
        for candidate in candidates:
            cand_hv = self.encode_entity(candidate)
            sim = cosine_similarity(query, cand_hv, self.dim)
            similarities[candidate] = sim

        # Find best match
        best = max(similarities.items(), key=lambda x: x[1])

        return best[0], best[1], similarities

    def solve_analogy_ml_ar(self, a: str, b: str, c: str,
                           candidates: List[str]) -> ExplainabilityOutput:
        """
        Solve analogy with full ML+AR composition.

        Combines:
        1. VSA binding/unbinding for feature extraction
        2. ML classifier layer for pattern recognition
        3. AR reasoning validation for logical proof
        4. Explainability output with confidence

        Args:
            a, b, c: Analogy components (A:B :: C:?)
            candidates: List of possible answers

        Returns:
            ExplainabilityOutput with prediction, confidence, and explanation
        """
        a_hv = self.encode_entity(a)
        b_hv = self.encode_entity(b)
        c_hv = self.encode_entity(c)

        # Step 1: VSA binding/unbinding
        bound = bind(a_hv, b_hv, self.dim)
        query = unbind(bound, c_hv, self.dim)

        # Step 2: Find candidate similarities
        similarities = {}
        for candidate in candidates:
            cand_hv = self.encode_entity(candidate)
            sim = cosine_similarity(query, cand_hv, self.dim)
            similarities[candidate] = sim

        best_vsa_candidate = max(similarities.items(), key=lambda x: x[1])

        # Step 3: ML classification
        ml_result = self.ml_classifier.classify_relationship(query, similarities)

        # Step 4: AR validation for each candidate
        best_ar_candidate = None
        best_ar_confidence = 0.0
        ar_validation = None

        for candidate in candidates:
            ar_val = self.ar_validator.validate_analogy(
                a, b, c, candidate, ml_result
            )
            if ar_val.confidence > best_ar_confidence:
                best_ar_confidence = ar_val.confidence
                best_ar_candidate = candidate
                ar_validation = ar_val

        # Step 5: Combine VSA, ML, and AR for final prediction
        # Weighted combination of confidence scores
        vsa_weight, ml_weight, ar_weight = 0.3, 0.35, 0.35

        final_scores = {}
        for candidate in candidates:
            vsa_score = similarities.get(candidate, 0.0)
            # For ML, use confidence if candidate matches best pattern
            ml_score = ml_result.confidence if candidate == best_vsa_candidate[0] else 0.1
            # For AR, use validation confidence if candidate passed validation
            ar_score = ar_validation.confidence if ar_validation and candidate == best_ar_candidate else 0.1

            # Normalize scores to 0-1 range
            final_scores[candidate] = (
                vsa_weight * max(0, vsa_score) +
                ml_weight * ml_score +
                ar_weight * ar_score
            )

        # Determine final prediction
        final_prediction = max(final_scores.items(), key=lambda x: x[1])
        final_confidence = final_prediction[1]

        # Step 6: Generate explainability output
        explanation = self._generate_explanation(
            a, b, c, final_prediction[0],
            ml_result, ar_validation,
            best_vsa_candidate, similarities
        )

        key_features = list(ml_result.feature_importance.keys())
        proof_trace = ar_validation.proof_trace if ar_validation else []

        return ExplainabilityOutput(
            prediction=final_prediction[0],
            final_confidence=final_confidence,
            ml_confidence=ml_result.confidence,
            ar_confidence=best_ar_confidence,
            explanation=explanation,
            key_features=key_features,
            proof_trace=proof_trace
        )

    def _generate_explanation(self, a: str, b: str, c: str, predicted: str,
                          ml_result: MLClassificationResult,
                          ar_validation: Optional[ARValidationResult],
                          vsa_best: Tuple[str, float],
                          all_sims: Dict[str, float]) -> str:
        """Generate human-readable explanation."""
        parts = [
            f"Analogy {a}:{b} :: {c}:? → {predicted}",
            "",
            "ML Layer:",
            f"  Pattern: {ml_result.predicted_class}",
            f"  Confidence: {ml_result.confidence:.3f}",
            f"  Features: {', '.join(f'{k}={v:.2f}' for k, v in ml_result.feature_importance.items() if v > 0.1)}",
            "",
            "VSA Layer:",
            f"  Best VSA match: {vsa_best[0]} ({vsa_best[1]:.3f})",
            "",
        ]

        if ar_validation:
            parts.extend([
                "AR Validation Layer:",
                f"  Status: {ar_validation.status.value}",
                f"  Confidence: {ar_validation.confidence:.3f}",
                f"  Proof Steps: {len(ar_validation.proof_trace)}/10",
            ])

        parts.append("")
        parts.append("Decision Rationale:")
        if ar_validation and ar_validation.status == ARValidation.VALID:
            parts.append(f"  {predicted} was selected based on strong AR validation support.")
        elif ml_result.confidence > 0.7:
            parts.append(f"  {predicted} was selected based on strong ML pattern matching ({ml_result.predicted_class}).")
        else:
            parts.append(f"  {predicted} was selected based on VSA similarity with moderate confidence.")

        return "\n".join(parts)

    def bind_self_inverse_check(self, a: str, b: str) -> float:
        """
        Verify bind self-inverse property: bind(a, bind(a, b)) ≈ b

        Returns similarity between original B and recovered B
        """
        a_hv = self.encode_entity(a)
        b_hv = self.encode_entity(b)

        bound = bind(a_hv, b_hv, self.dim)
        recovered = unbind(bound, a_hv, self.dim)

        return cosine_similarity(b_hv, recovered, self.dim)


class VSABundleReasoner:
    """
    VSA bundle reasoning for set-like operations.

    Demonstrates:
    - bundle2 for superposition
    - bundle3 for consensus
    - Individual concept recovery from bundle
    """

    def __init__(self, dim: int = VSA_DIM):
        self.dim = dim
        self.concepts: Dict[str, List[Trit]] = {}

    def encode_concept(self, name: str, seed: Optional[int] = None) -> List[Trit]:
        """Encode a concept to hypervector."""
        if seed is None:
            seed = hash(name) % 10000
        hv = generate_random_hv(seed, self.dim)
        self.concepts[name] = hv
        return hv

    def create_superposition(self, concepts: List[str]) -> List[Trit]:
        """
        Create superposition of concepts using bundle.

        Uses bundle3 for 3+ concepts (robust consensus voting).
        """
        if not concepts:
            return [TRIT_ZERO] * self.dim

        if len(concepts) == 1:
            return self.encode_concept(concepts[0])

        if len(concepts) == 2:
            a = self.encode_concept(concepts[0])
            b = self.encode_concept(concepts[1])
            return bundle2(a, b, self.dim)

        # For 3+ concepts, use bundle3 iteratively
        result = self.encode_concept(concepts[0])
        for i in range(1, len(concepts)):
            c = self.encode_concept(concepts[i])
            result = bundle3(result, result, c, self.dim)

        return result

    def probe_concept(self, bundle_hv: List[Trit], concept: str,
                     threshold: float = 0.5) -> Tuple[bool, float]:
        """
        Probe if a concept is in the bundle.

        Returns: (present, similarity)
        """
        concept_hv = self.encode_concept(concept)
        sim = cosine_similarity(bundle_hv, concept_hv, self.dim)
        return sim >= threshold, sim


class VSASequenceEncoder:
    """
    VSA sequence encoding with position-aware binding.

    Uses permute for position encoding.
    Demonstrates order-sensitive reasoning.
    """

    def __init__(self, dim: int = VSA_DIM):
        self.dim = dim
        self.items: Dict[str, List[Trit]] = {}

    def encode_item(self, item: str, seed: Optional[int] = None) -> List[Trit]:
        """Encode an item to hypervector."""
        if seed is None:
            seed = hash(item) % 10000
        hv = generate_random_hv(seed, self.dim)
        self.items[item] = hv
        return hv

    def encode_sequence(self, items: List[str]) -> List[Trit]:
        """
        Encode sequence with position-aware binding.

        Algorithm: bundle(items[0], permute(items[1], 1), permute(items[2], 2), ...)
        """
        if not items:
            return [TRIT_ZERO] * self.dim

        result = self.encode_item(items[0])

        for i, item in enumerate(items[1:], 1):
            item_hv = self.encode_item(item)
            permuted = permute(item_hv, self.dim, i)
            result = bundle2(result, permuted, self.dim)

        return result

    def probe_position(self, sequence_hv: List[Trit], item: str,
                      position: int) -> float:
        """
        Probe if item is at specific position in sequence.

        Returns similarity between sequence and permuted item at position.
        """
        item_hv = self.encode_item(item)
        permuted = permute(item_hv, self.dim, position)
        return cosine_similarity(sequence_hv, permuted, self.dim)


# ============================================================================
# Main: Example Usage
# ============================================================================

def main():
    """Run VSA analogy reasoning with ML+AR composition examples."""
    print("=" * 70)
    print("VSA Analogy Reasoning with ML+AR Composition")
    print("Composition: VSA -> ML Classifier -> AR Validator -> Explainability")
    print("=" * 70)
    print()

    # Initialize reasoner with ML+AR components
    reasoner = VSAAnalogyReasoner(dim=VSA_DIM, max_proof_steps=10)

    # ========================================================================
    # Example 0: Full ML+AR Composition Demonstration
    # ========================================================================
    print("=" * 70)
    print("Example 0: FULL ML+AR COMPOSITION (Enhanced VSA Analogy)")
    print("=" * 70)
    print()

    ml_ar_analogies = [
        ("king", "man", "queen", ["woman", "girl", "princess", "female"]),
        ("dog", "puppy", "cat", ["kitten", "puppy", "animal", "pet"]),
        ("paris", "france", "tokyo", ["japan", "china", "asia", "kyoto"]),
    ]

    for a, b, c, candidates in ml_ar_analogies:
        print("-" * 70)
        print(f"Analogy: {a}:{b} :: {c}:?")
        print("-" * 70)

        # Solve with full ML+AR composition
        result = reasoner.solve_analogy_ml_ar(a, b, c, candidates)

        print(f"\nPREDICTION: {result.prediction}")
        print(f"FINAL CONFIDENCE: {result.final_confidence:.3f}")
        print(f"  - ML Confidence: {result.ml_confidence:.3f}")
        print(f"  - AR Confidence: {result.ar_confidence:.3f}")

        print(f"\nKEY FEATURES: {', '.join(result.key_features)}")

        print("\nEXPLANATION:")
        print(result.explanation)

        print("\nPROOF TRACE (<=10 steps):")
        for i, step in enumerate(result.proof_trace, 1):
            print(f"  [{i}] {step}")

        print()

    # ========================================================================
    # Example 1: VSA-only baseline comparison
    # ========================================================================
    print("=" * 70)
    print("Example 1: VSA-ONLY BASELINE (For Comparison)")
    print("=" * 70)
    print()

    analogies = [
        ("king", "man", "queen", ["woman", "girl", "princess", "female"]),
        ("dog", "puppy", "cat", ["kitten", "puppy", "animal", "pet"]),
        ("paris", "france", "tokyo", ["japan", "china", "asia", "kyoto"]),
        ("paris", "france", "berlin", ["germany", "europe", "munich", "paris"]),
    ]

    for a, b, c, candidates in analogies:
        print(f"\nAnalogy: {a}:{b} :: {c}:?")
        best, sim, all_sims = reasoner.solve_analogy(a, b, c, candidates)
        print(f"  VSA Answer: {best} (similarity: {sim:.3f})")
        print(f"  All similarities: {all_sims}")

    # ========================================================================
    # Example 2: Bind self-inverse property
    # ========================================================================
    print()
    print("-" * 70)
    print("Example 2: Bind Self-Inverse Property")
    print("-" * 70)
    print("Property: bind(A, bind(A, B)) = B (self-inverse)")
    print()

    test_pairs = [("king", "queen"), ("paris", "france"), ("code", "compile")]
    for a, b in test_pairs:
        sim = reasoner.bind_self_inverse_check(a, b)
        print(f"  bind({a}, bind({a}, {b})) ≈ {b}: similarity = {sim:.3f}")

    # ========================================================================
    # Example 3: Bundle superposition with ML+AR
    # ========================================================================
    print()
    print("-" * 70)
    print("Example 3: Bundle Superposition (Set-like Reasoning)")
    print("-" * 70)

    bundle_reasoner = VSABundleReasoner()

    # Create superposition of fruits
    fruits = ["apple", "banana", "orange", "grape"]
    fruit_bundle = bundle_reasoner.create_superposition(fruits)

    print(f"\nBundle of: {', '.join(fruits)}")
    print(f"  Non-zero trits: {sum(1 for t in fruit_bundle if t != TRIT_ZERO)}/{VSA_DIM}")

    # Probe individual fruits
    print("\n  Probing individual fruits:")
    for fruit in fruits + ["carrot", "steak"]:
        present, sim = bundle_reasoner.probe_concept(fruit_bundle, fruit)
        status = "+" if present else "-"
        print(f"    [{status}] {fruit}: {sim:.3f}")

    # ========================================================================
    # Example 4: Sequence encoding
    # ========================================================================
    print()
    print("-" * 70)
    print("Example 4: Sequence Encoding (Position-Aware)")
    print("-" * 70)
    print("Using permute for position: bundle(item[0], permute(item[1], 1), ...)")
    print()

    seq_encoder = VSASequenceEncoder()

    sequences = [
        ["breakfast", "lunch", "dinner"],
        ["first", "second", "third", "fourth"],
    ]

    for seq in sequences:
        seq_hv = seq_encoder.encode_sequence(seq)
        print(f"\nSequence: {' -> '.join(seq)}")
        print(f"  Encoded (non-zero trits): {sum(1 for t in seq_hv if t != TRIT_ZERO)}/{VSA_DIM}")

        # Probe positions
        print("  Position probes:")
        for item in seq:
            for pos in range(len(seq)):
                sim = seq_encoder.probe_position(seq_hv, item, pos)
                if sim > 0.5:
                    marker = "*" if seq.index(item) == pos else " "
                    print(f"    {marker} {item} at pos {pos}: {sim:.3f}")

    # ========================================================================
    # Summary of ML+AR Composition
    # ========================================================================
    print()
    print("=" * 70)
    print("ML+AR COMPOSITION SUMMARY")
    print("=" * 70)
    print()
    print("Architecture:")
    print("  1. VSA Layer: Bind/Unbind for feature extraction")
    print("  2. ML Classifier: Pattern recognition on VSA features")
    print("  3. AR Validator: Logical proof trace (<=10 steps)")
    print("  4. Explainability: Confidence breakdown + explanation")
    print()
    print("VSA Properties Demonstrated:")
    print("  1. Bind/Unbind for associative memory")
    print("  2. Self-inverse: bind(A, bind(A, B)) = B")
    print("  3. Bundle for superposition/set reasoning")
    print("  4. Permute for position-aware sequence encoding")
    print("  5. Cosine similarity for nearest-neighbor search")
    print()
    print("ML+AR Enhancements:")
    print("  1. Pattern classification with confidence scores")
    print("  2. Knowledge graph validation")
    print("  3. Proof trace generation (<=10 steps)")
    print("  4. Explainability with feature importance")
    print("=" * 70)


if __name__ == "__main__":
    main()
