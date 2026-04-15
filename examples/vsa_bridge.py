#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Licensed under Apache License 2.0 —
# http://www.apache.org/licenses/LICENSE-2.0
"""
VSA Bridge Layer - Centralized VSA Operations for CLARA Examples
==================================================================

This module provides centralized VSA operations for all examples,
implementing the specification in specs/ar/vsa_bridge.t27

Bridges VSA hypervectors with AR reasoning components.

Author: T27 Trinity S³AI Project
Reference: specs/ar/vsa_bridge.t27
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import math
import random


# ============================================================================
# T27 Ternary Types (from specs/base/types.t27)
# ============================================================================

TRIT_NEG = -1
TRIT_ZERO = 0
TRIT_POS = 1

Trit = int  # Type alias for ternary value


# ============================================================================
# Constants (from specs/ar/vsa_bridge.t27)
# ============================================================================

VSA_DIMENSION = 1024
MAX_FACTS = 256
SIMILARITY_THRESHOLD = 0.15
MAX_PREDICATE_ARGS = 8
VSA_SEED = 0xDEADBEEF


# ============================================================================
# VSA Core Types
# ============================================================================

HyperVector = List[Trit]  # 1024-dimensional ternary hypervector


@dataclass
class HornClause:
    """AR Horn clause representation."""
    name: int  # Predicate identifier (hash of name string)
    args: List[Trit]  # Arguments as Trit values
    arg_count: int  # Actual number of arguments used


@dataclass
class FactEncoding:
    """VSA representation of an AR fact."""
    hypervector: HyperVector
    predicate_hash: int
    confidence: float
    original_fact: HornClause


@dataclass
class SimilarityResult:
    """Result of VSA similarity search."""
    matches: List[FactEncoding]
    best_similarity: float


# ============================================================================
# VSA Core Operations (from specs/vsa/core.t27 and specs/vsa/ops.t27)
# ============================================================================

def random_hypervector(seed: int, dim: int = VSA_DIMENSION) -> HyperVector:
    """Generate a pseudo-random hypervector from seed using xorshift64."""
    result = []
    state = seed

    for _ in range(dim):
        # xorshift64 PRNG
        state ^= (state << 13) & 0xFFFFFFFFFFFFFFFF
        state ^= (state >> 7) & 0xFFFFFFFFFFFFFFFF
        state ^= (state << 17) & 0xFFFFFFFFFFFFFFFF

        r = state % 3
        if r == 0:
            result.append(TRIT_NEG)
        elif r == 1:
            result.append(TRIT_ZERO)
        else:
            result.append(TRIT_POS)

    return result


def to_trits(vector: List[float], dim: int = VSA_DIMENSION) -> List[Trit]:
    """Convert float vector to ternary hypervector."""
    trits = []
    for v in vector[:dim]:
        if v > 0.33:
            trits.append(TRIT_POS)
        elif v < -0.33:
            trits.append(TRIT_NEG)
        else:
            trits.append(TRIT_ZERO)
    # Pad if needed
    while len(trits) < dim:
        trits.append(TRIT_ZERO)
    return trits[:dim]


def dot_product(a: List[Trit], b: List[Trit], length: int) -> float:
    """Compute dot product Σ a[i] * b[i]."""
    return float(sum(a[i] * b[i] for i in range(length)))


def vector_norm(v: List[Trit], length: int) -> float:
    """Compute L2 norm: sqrt(Σ v[i]²)."""
    nonzero = sum(1 for i in range(length) if v[i] != TRIT_ZERO)
    return math.sqrt(nonzero)


def cosine_similarity(a: List[Trit], b: List[Trit], length: int) -> float:
    """Cosine similarity: (a·b) / (||a|| * ||b||)."""
    dot = dot_product(a, b, length)
    norm_a = vector_norm(a, length)
    norm_b = vector_norm(b, length)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def hamming_similarity(a: List[Trit], b: List[Trit], length: int) -> float:
    """Hamming similarity: 1 - (distance / length)."""
    distance = sum(1 for i in range(length) if a[i] != b[i])
    return 1.0 - (distance / length)


def similarity(a: List[Trit], b: List[Trit], length: int,
               metric: str = 'cosine') -> float:
    """Compute similarity between two hypervectors."""
    if metric == 'cosine':
        return cosine_similarity(a, b, length)
    elif metric == 'hamming':
        return hamming_similarity(a, b, length)
    return dot_product(a, b, length)


# ============================================================================
# VSA Bridge Operations (from specs/ar/vsa_bridge.t27)
# ============================================================================

def encode_fact(fact: HornClause, seed: int = VSA_SEED) -> FactEncoding:
    """Encode an AR HornClause as a VSA hypervector.

    Algorithm:
    1. Create combined seed from predicate name and args
    2. Generate hypervector with random_hypervector(seed)
    3. Return FactEncoding with hypervector and metadata

    Complexity: O(D) where D = VSA_DIMENSION
    """
    # Create combined seed from predicate name and args
    combined_seed = fact.name

    for i in range(fact.arg_count):
        arg_val = (fact.args[i] + 1) if i < len(fact.args) else 0
        combined_seed ^= (arg_val << (8 * i))

    # Add VSA seed constant
    combined_seed ^= seed

    # Generate hypervector
    hypervector = random_hypervector(combined_seed)

    return FactEncoding(
        hypervector=hypervector,
        predicate_hash=fact.name,
        confidence=1.0,  # Facts have full confidence
        original_fact=fact
    )


def encode_predicate(name: str, args: List[Trit],
                     seed: int = VSA_SEED) -> FactEncoding:
    """Encode a predicate-argument structure directly to VSA.

    Alternative to encode_fact when predicate name is available as string.

    Complexity: O(D + n)
    """
    # Compute hash of predicate name
    name_hash = 0
    for i, ch in enumerate(name):
        name_hash ^= (ord(ch) << (8 * (i % 8)))

    # Create seed from hash + args
    combined_seed = name_hash

    for i, arg in enumerate(args):
        arg_val = (arg + 1)
        combined_seed ^= (arg_val << (8 * i))

    # Generate hypervector
    hypervector = random_hypervector(combined_seed ^ seed)

    return FactEncoding(
        hypervector=hypervector,
        predicate_hash=name_hash & 0xFFFF,
        confidence=1.0,
        original_fact=HornClause(
            name=name_hash & 0xFFFF,
            args=args,
            arg_count=len(args)
        )
    )


def similarity_fact_query(query: HyperVector,
                          fact_encodings: List[FactEncoding],
                          limit: int = MAX_FACTS) -> SimilarityResult:
    """Find the most similar encoded facts to a query hypervector.

    Algorithm:
    1. Compute cosine similarity with all encoded facts
    2. Filter by SIMILARITY_THRESHOLD
    3. Return top 'limit' matches sorted by similarity

    Complexity: O(n * D) where n = encoding_count, D = VSA_DIMENSION
    """
    results = []

    for fact_enc in fact_encodings:
        sim = cosine_similarity(query, fact_enc.hypervector, VSA_DIMENSION)

        if sim >= SIMILARITY_THRESHOLD:
            results.append((sim, fact_enc))

    # Sort by similarity (descending)
    results.sort(key=lambda x: x[0], reverse=True)

    # Take top matches
    matches = [fact_enc for _, fact_enc in results[:limit]]

    best_sim = results[0][0] if results else 0.0

    return SimilarityResult(
        matches=matches,
        best_similarity=best_sim
    )


def bind_fact(fact_a: FactEncoding, fact_b: FactEncoding) -> FactEncoding:
    """Bind two encoded facts using VSA bind operation.

    Represents relationship: fact_a(fact_b)

    Complexity: O(D)
    """
    result_vector = []

    # Perform element-wise XOR (bind operation)
    for i in range(VSA_DIMENSION):
        a_trit = fact_a.hypervector[i]
        b_trit = fact_b.hypervector[i]

        # Trit XOR (treated as signed for trit values)
        xor_val = a_trit + b_trit
        if xor_val == -2:
            result_vector.append(TRIT_POS)
        elif xor_val == 0:
            result_vector.append(TRIT_ZERO)
        elif xor_val == 2:
            result_vector.append(TRIT_NEG)
        else:
            result_vector.append(xor_val)

    return FactEncoding(
        hypervector=result_vector,
        predicate_hash=fact_a.predicate_hash,
        confidence=(fact_a.confidence + fact_b.confidence) / 2.0,
        original_fact=fact_a.original_fact
    )


def bundle_facts(facts: List[FactEncoding]) -> FactEncoding:
    """Bundle multiple encoded facts using VSA bundle operation.

    Represents superposition (set union) of facts.

    Complexity: O(D * n)
    """
    if not facts:
        return FactEncoding(
            hypervector=[TRIT_ZERO] * VSA_DIMENSION,
            predicate_hash=0,
            confidence=0.0,
            original_fact=HornClause(0, [], 0)
        )

    # Initialize with first fact
    result_vector = facts[0].hypervector.copy()

    # Bundle remaining facts (majority vote)
    for fact in facts[1:]:
        for i in range(VSA_DIMENSION):
            a_trit = result_vector[i]
            b_trit = fact.hypervector[i]

            # Majority vote for trits
            result_vector[i] = a_trit if a_trit == b_trit else TRIT_ZERO

    # Average confidence across facts
    total_confidence = sum(f.confidence for f in facts)

    return FactEncoding(
        hypervector=result_vector,
        predicate_hash=facts[0].predicate_hash,
        confidence=total_confidence / len(facts),
        original_fact=facts[0].original_fact
    )


def permute(vector: HyperVector, shift: int) -> HyperVector:
    """Permute hypervector by shift positions.

    Used for position-aware encoding in VSA.

    Complexity: O(D)
    """
    dim = len(vector)
    shift = shift % dim
    return vector[shift:] + vector[:shift]


# ============================================================================
# VSA Codebook (cleanup memory)
# ============================================================================

class VSA_Codebook:
    """Cleanup memory / item memory for nearest-neighbor lookup."""

    def __init__(self, capacity: int = MAX_FACTS):
        self.entries: List[HyperVector] = []
        self.labels: List[int] = []
        self.capacity = capacity

    def add(self, vector: HyperVector, label: int) -> bool:
        """Add a labeled vector to the codebook."""
        if len(self.entries) >= self.capacity:
            return False
        if len(vector) != VSA_DIMENSION:
            return False

        self.entries.append(vector.copy())
        self.labels.append(label)
        return True

    def lookup(self, query: HyperVector) -> Optional[int]:
        """Find the label of the most similar entry."""
        if not self.entries:
            return None

        best_label = self.labels[0]
        best_sim = -2.0

        for entry, label in zip(self.entries, self.labels):
            sim = cosine_similarity(query, entry, VSA_DIMENSION)
            if sim > best_sim:
                best_sim = sim
                best_label = label

        return best_label if best_sim >= SIMILARITY_THRESHOLD else None

    def cleanup(self, noisy: HyperVector) -> HyperVector:
        """Map a noisy vector to the nearest clean entry."""
        if not self.entries:
            return noisy

        best_idx = 0
        best_sim = -2.0

        for i, entry in enumerate(self.entries):
            sim = cosine_similarity(noisy, entry, VSA_DIMENSION)
            if sim > best_sim:
                best_sim = sim
                best_idx = i

        if best_sim < SIMILARITY_THRESHOLD:
            return noisy

        return self.entries[best_idx].copy()


# ============================================================================
# Utility Functions
# ============================================================================

def trit_to_str(trit: Trit) -> str:
    """Convert trit to string representation."""
    if trit == TRIT_POS:
        return "TRUE"
    elif trit == TRIT_NEG:
        return "FALSE"
    return "UNKNOWN"


def str_to_trit(s: str) -> Trit:
    """Convert string to trit."""
    s_upper = s.upper()
    if s_upper in ("TRUE", "T", "K_TRUE", "+"):
        return TRIT_POS
    elif s_upper in ("FALSE", "F", "K_FALSE", "-"):
        return TRIT_NEG
    return TRIT_ZERO


def print_hypervector_summary(hv: HyperVector, name: str = "HyperVector") -> None:
    """Print summary statistics of a hypervector."""
    pos_count = sum(1 for t in hv if t == TRIT_POS)
    neg_count = sum(1 for t in hv if t == TRIT_NEG)
    zero_count = sum(1 for t in hv if t == TRIT_ZERO)

    print(f"{name}: dim={len(hv)}, +={pos_count}, -={neg_count}, 0={zero_count}")


# ============================================================================
# Export symbols
# ============================================================================

__all__ = [
    # Constants
    'VSA_DIMENSION', 'MAX_FACTS', 'SIMILARITY_THRESHOLD',
    'VSA_SEED', 'TRIT_NEG', 'TRIT_ZERO', 'TRIT_POS',
    # Types
    'Trit', 'HyperVector', 'HornClause', 'FactEncoding', 'SimilarityResult',
    # Core operations
    'random_hypervector', 'to_trits', 'dot_product', 'vector_norm',
    'cosine_similarity', 'hamming_similarity', 'similarity',
    # Bridge operations
    'encode_fact', 'encode_predicate', 'similarity_fact_query',
    'bind_fact', 'bundle_facts', 'permute',
    # Codebook
    'VSA_Codebook',
    # Utilities
    'trit_to_str', 'str_to_trit', 'print_hypervector_summary',
]
