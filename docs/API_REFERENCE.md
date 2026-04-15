# SPDX-License-Identifier: Apache-2.0
# Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0

# API Reference Guide for TRINITY CLARA

Complete API reference for all TRINITY CLARA components, organized by module.

---

## Table of Contents

1. [Base Types](#base-types) — Trit enums, GF16 encoding
2. [VSA Operations](#vsa-operations) — Bind/unbind/bundle/permute
3. [VSA Bridge](#vsa-bridge) — AR-VSA integration layer
4. [Ternary Logic](#ternary-logic) — K3 operations
5. [AR Reasoning](#ar-reasoning) — Forward-chaining, ASP, proof traces
6. [Explainability](#explainability) — XAI formats, confidence scoring
7. [COA Planning](#coa-planning) — Course of Action with constraints
8. [Composition Patterns](#composition-patterns) — ML+AR integration

---

## Base Types

### Trit Values

```python
from specs.base.types import Trit

TRIT_NEG = -1  # K_FALSE
TRIT_ZERO = 0   # K_UNKNOWN
TRIT_POS = 1   # K_TRUE
```

**Usage:** Trit values represent Kleene K3 truth values. Used throughout all AR reasoning components.

### GF16 Encoding

```python
from specs.numeric.gf16 import GF16_ZERO, GF16_ONE

# φ-optimized confidence encoding
# 1.0 = GF16_ONE (full confidence)
# 0.65535 = GF16_ONE / φ  # GF16 optimized value
# 0.9 = 0.9 * GF16_ONE  # Alternative linear scale
```

**Usage:** GF16 provides wider dynamic range (65,000×) and better precision (1.8×) than float32 for confidence encoding.

---

## VSA Operations

### Core Constants

```python
from specs.vsa.core import VSA_DIM, SIMILARITY_THRESHOLD

VSA_DIM = 1024  # Hypervector dimension
SIMILARITY_THRESHOLD = 0.15  # 99.9% specificity
```

### bind(a: List[Trit], b: List[Trit]) -> List[Trit]

**Purpose:** Associative memory binding operation
**Complexity:** O(n) where n = VSA_DIM
**Returns:** bound vector representing associative memory binding

```python
from specs.vsa.ops import bind

# Example
result = bind([1, 0, -1, 1], [1, -1, 0, 1])
```

### unbind(bound: List[Trit], key: List[Trit]) -> List[Trit]

**Purpose:** Inverse of bind operation for content-addressable retrieval
**Complexity:** O(n) where n = VSA_DIM
**Returns:** key vector that was bound to `bound`

```python
from specs.vsa.ops import unbind

# Example
key = unbind(result, key)  # Retrieves original key vector
```

### bundle2(a: List[Trit], b: List[Trit]) -> List[Trit]

**Purpose:** Superposition of two vectors using majority voting
**Complexity:** O(n) where n = VSA_DIM
**Returns:** Result vector where each trit is majority of inputs at that position

```python
from specs.vsa.ops import bundle2

# Example
result = bundle2([1, 1, 0], [0, 0, 1])
# Result: [1, 1, 0] (1 and 1 are majority at position 0)
```

### bundle3(a: List[Trit], b: List[Trit], c: List[Trit]) -> List[Trit]

**Purpose:** Superposition of three vectors using 2/3 majority voting
**Complexity:** O(n) where n = VSA_DIM
**Returns:** Result vector where each trit is majority of inputs at that position

```python
from specs.vsa.ops import bundle3

# Example
result = bundle3([1, 1, 0], [0, 0, 1], [1, 0, 1])
# Result: [1, 1, 0] (2 out of 3 are majority at position 0)
```

### permute(vector: List[Trit], shift: int) -> List[Trit]

**Purpose:** Position-aware encoding by circular shift
**Complexity:** O(n) where n = VSA_DIM
**Returns:** Permutated vector where V'[i] = V[(i+shift)%n]

```python
from specs.vsa.ops import permute

# Example
result = permute([1, 2, 3, 4, 5], 1)
# Result: [2, 3, 4, 5, 1, 2, 3, 4, 5]
```

### cosine_similarity(a: List[Trit], b: List[Trit]) -> float

**Purpose:** Cosine similarity metric for nearest-neighbor search
**Complexity:** O(n) where n = VSA_DIM
**Returns:** Similarity score in [-1.0, 1.0] range

```python
from specs.vsa.ops import cosine_similarity

# Example
score = cosine_similarity(vector_a, vector_b)
if score > SIMILARITY_THRESHOLD:
    # Consider similar
```

### hamming_distance(a: List[Trit], b: List[Trit]) -> int

**Purpose:** Hamming distance (count of differing positions) for dissimilarity
**Complexity:** O(n) where n = VSA_DIM
**Returns:** Integer count in [0, n] range

```python
from specs.vsa.ops import hamming_distance

# Example
distance = hamming_distance(vector_a, vector_b)
# Maximum is 1024 for 1024-dimensional vectors
```

---

## VSA Bridge

### encode_fact(data: dict) -> List[Trit]

**Purpose:** Encode arbitrary data into ternary hypervector for VSA operations
**Complexity:** O(n) where n = VSA_DIM
**Returns:** 1024-dimensional ternary hypervector

```python
from specs.vsa_bridge import encode_fact

# Example: Encode a patient case
patient_hv = encode_fact({
    'patient_id': 'patient_001',
    'symptoms': ['fever', 'cough']
})
```

### decode_to_fact(hv: List[Trit]) -> dict

**Purpose:** Decode ternary hypervector back to original data structure
**Complexity:** O(n) where n = VSA_DIM
**Returns:** Dictionary with original data keys

```python
from specs.vsa_bridge import decode_to_fact

# Example
data = decode_to_fact(patient_hv)
# Returns: {'patient_id': 'patient_001', 'symptoms': ['fever', 'cough']}
```

### similarity_fact_query(query_hv: List[Trit], max_facts: int = 256) -> List[dict]

**Purpose:** Query fact store for semantically similar hypervectors
**Complexity:** O(n) where n = VSA_DIM
**Returns:** List of matching facts sorted by similarity

```python
from specs.vsa_bridge import similarity_fact_query

# Example
results = similarity_fact_query(patient_hv, MAX_FACTS=128)
# Returns list of similar patient cases sorted by similarity
```

---

## Ternary Logic

### k3_and(a: Trit, b: Trit) -> Trit

**Purpose:** Kleene K3 conjunction (minimum of truth values)
**Truth Table:**
| a \ b | -1  |  0   | +1  |
|-------|-------|-------|-------|
| -1    | -1   |  0   | -1   |
|  0    |  0   |  0   |  0   |
| +1    | -1   |  0   | +1   |

```python
from specs.ar.ternary_logic import k3_and

# Example
result = k3_and(TRIT_NEG, TRIT_POS)  # Returns TRIT_NEG
```

### k3_or(a: Trit, b: Trit) -> Trit

**Purpose:** Kleene K3 disjunction (maximum of truth values)
**Truth Table:**
| a \ b | -1  |  0   | +1  |
|-------|-------|-------|-------|
| -1    |  0   | +1  | +1   |
|  0    |  0   | +1  | +1   |

```python
from specs.ar.ternary_logic import k3_or

# Example
result = k3_or(TRIT_NEG, TRIT_ZERO)  # Returns TRIT_ZERO
```

### k3_not(a: Trit) -> Trit

**Purpose:** Kleene K3 negation
**Truth Table:**
| a | ¬a |
|----|----|
| -1 |  0  |
|  0  |  1  |

```python
from specs.ar.ternary_logic import k3_not

# Example
result = k3_not(TRIT_POS)  # Returns TRIT_NEG
```

### k3_implies(a: Trit, b: Trit) -> Trit

**Purpose:** Kleene K3 material implication
**Truth Table:**
| a \ b | ¬a → b |
|-------|-------|--------|
| -1    |  0   |
|  0    |  0   | +1   |

```python
from specs.ar.ternary_logic import k3_implies

# Example
result = k3_implies(TRIT_POS, TRIT_NEG)  # Returns TRIT_NEG
```

---

## AR Reasoning

### MAX_STEPS

```python
from specs.ar.proof_trace import MAX_STEPS

MAX_STEPS = 10  # CLARA requirement for explanation length
```

**Usage:** All AR reasoning operations must enforce this limit for CLARA compliance.

### forward_chain(facts: List[Fact], rules: List[Rule]) -> Conclusion

**Purpose:** Forward-chaining AR with bounded step limit
**Complexity:** O(n×m×k) where n = number of facts, m = number of rules, k = MAX_STEPS
**Returns:** Conclusion with trace, steps used, confidence

```python
from specs.ar.datelog_engine import forward_chain

# Example
conclusion = forward_chain(
    facts=[Fact(predicate='has_fever', value='yes')],
    rules=[Rule(if_facts=[Fact(predicate='has_fever', value='yes')],
                  then_conclusion='respiratory_infection')],
    max_steps=MAX_STEPS
)
```

### HornClause

```python
from specs.ar.datelog_engine import HornClause

@dataclass
class HornClause:
    if_facts: List[Fact]
    then_conclusion: str
```

**Usage:** Dataclass representing a single logical rule in Horn clause form.

### Fact

```python
from specs.ar.datelog_engine import Fact

@dataclass
class Fact:
    predicate: str
    value: str
    confidence: float = 1.0
```

**Usage:** Dataclass representing a single logical fact with confidence.

---

## Explainability

### generate_explanation(trace: List[Step]) -> str

**Purpose:** Generate human-readable explanation from proof trace
**Complexity:** O(s) where s = number of steps

```python
from specs.ar.explainability import generate_explanation

# Example
explanation = generate_explanation(proof_trace)
# Returns formatted text with step-by-step reasoning
```

### Explanation Format: Natural

```
Step 1: apply_rule
    Premise: [symptom=fever, symptom=cough]
    Conclusion: respiratory_infection

Step 2: apply_rule
    Premise: [diagnosis=respiratory_infection, symptom=shortness_of_breath]
    Conclusion: pneumonia

Total steps: 2 (≤10 limit)
```

---

## COA Planning

### MAX_CLAUSES

```python
from specs.ar.coa_planning import MAX_CLAUSES

MAX_CLAUSES = 256  # Maximum number of planning rules
```

**Usage:** Limits planning rule set size for COA optimization.

---

## Composition Patterns

### CNN_RULES

**Pattern ID:** 0
**Components:** CNN (feature extraction) + AR Rules + XAI
**Use Case:** Medical diagnosis from images

```python
from specs.ar.composition import CNN_RULES

# Extract CNN features from image
features = cnn.extract_features(image)
# Apply AR rules for classification
result = ar_reasoner.reason(features)
# Generate explanation
explanation = xai.generate_explanation(result.proof_trace)
```

### MLP_BAYESIAN

**Pattern ID:** 1
**Components:** MLP (forward pass) + Bayesian (inference)
**Use Case:** Legal QA with probabilistic reasoning

```python
from specs.ar.composition import MLP_BAYESIAN

# Forward pass through neural network
logits = mlp.forward(features)
# Apply Bayesian inference
posterior = bayesian.update(logits, prior)
# Combine probabilities
result = combine_probabilities(logits, posterior)
```

### TRANSFORMER_XAI

**Pattern ID:** 2
**Components:** Transformer (attention) + XAI (explanation)
**Use Case:** Legal QA with attention-based evidence

```python
from specs.ar.composition import TRANSFORMER_XAI

# Compute attention weights
attention = transformer.compute_attention(inputs, outputs)
# Extract important features for explanation
important_features = extract_important(attention, threshold=0.5)
# Generate explanation
explanation = generate_xai_explanation(important_features, max_steps=10)
```

### RL_GUARDRAILS

**Pattern ID:** 3
**Components:** RL (policy) + Safety Rules (guardrails)
**Use Case:** Autonomous driving with action validation

```python
from specs.ar.composition import RL_GUARDRAILS

# Sample action from RL policy
action = rl_policy.select_action(state)
# Validate against safety rules
is_safe = safety_rules.validate(action, state)
# Return final decision
result = action if is_safe else safe_default
```

---

## Usage Examples

### Complete ML+AR+XAI Pipeline

```python
from dataclasses import dataclass
from typing import List

@dataclass
class PipelineResult:
    prediction: str
    confidence: float
    explanation: str
    proof_trace: List[Step]
    steps_used: int

def run_complete_pipeline(input_data: dict) -> PipelineResult:
    """Run complete ML+VSA+AR+XAI pipeline."""
    
    # Step 1: ML Feature Extraction
    ml_features = ml_component.extract(input_data)
    
    # Step 2: VSA Encoding
    hv_input = encode_fact({'input': input_data})
    
    # Step 3: VSA Similarity Search
    similar_hv = similarity_fact_query(hv_input, MAX_FACTS=128)
    
    # Step 4: AR Reasoning (bounded)
    from specs.ar.proof_trace import MAX_STEPS
    ar_result = forward_chain(
        facts=decode_to_fact(similar_hv),
        rules=ar_rules,
        max_steps=MAX_STEPS
    )
    
    # Step 5: Explanation Generation
    from specs.ar.explainability import generate_explanation
    explanation = generate_explanation(ar_result.proof_trace)
    
    # Step 6: Confidence Scoring
    from specs.numeric.gf16 import GF16_ONE
    final_confidence = encode_confidence(
        min(ar_result.confidence, ml_features.confidence)
    )
    
    return PipelineResult(
        prediction=ar_result.conclusion,
        confidence=final_confidence,
        explanation=explanation,
        proof_trace=ar_result.proof_trace,
        steps_used=ar_result.steps_used
    )
```

---

## Integration Best Practices

### 1. Always Use Centralized VSA Operations

```python
# CORRECT
from specs.vsa_bridge import encode_fact, decode_to_fact

# INCORRECT: Local implementation
def bind(a, b):
    # ... local code ...

# INCORRECT
def unbind(bound, key):
    # ... local code ...
```

### 2. Enforce MAX_STEPS in All AR Reasoning

```python
from specs.ar.proof_trace import MAX_STEPS

def safe_reason(facts, rules):
    """Always check step limit."""
    steps = 0
    for rule in rules:
        if steps >= MAX_STEPS:
            break  # Enforce CLARA requirement
        # ... apply rule ...
        steps += 1
    return result, steps_used=steps
```

### 3. Use K3 Trit Values for Uncertainty

```python
from specs.ar.ternary_logic import TRIT_UNKNOWN

# CORRECT: Represent uncertainty explicitly
result.trit = TRIT_UNKNOWN  # Bounded rationality

# INCORRECT: Boolean cannot represent uncertainty
is_diagnosed = True  # No way to represent uncertainty
```

### 4. Combine Confidences Using Weighted Average

```python
def weighted_confidence(vsa_conf, ml_conf, ar_conf):
    """Combine confidence scores from multiple sources."""
    weights = [0.3, 0.35, 0.35]  # VSA, ML, AR
    total = sum(weights)
    return sum(w * c for w, c in [vsa_conf, ml_conf, ar_conf])) / total
```

---

## Error Handling

### Common Error Messages

```python
# Step limit exceeded
STEP_LIMIT_EXCEEDED = f"Explanation limit exceeded ({MAX_STEPS} steps). Partial result returned."

# No matching facts found
NO_MATCHING_FACTS = "No facts match similarity threshold in codebook."

# Confidence too low
LOW_CONFIDENCE = f"Confidence {confidence:.2f} below minimum quality threshold {MIN_QUALITY}. Recommendation: Request additional context."
```

---

## Versioning

All API components follow semantic versioning:

- Major version: X.Y.Z (e.g., 1.0.0)
- Minor version: X.Y.Z-a (e.g., 1.0.1-a)
- Compatibility version: X.Y.Z-rc (release candidate)

---

**φ² + 1/φ² = 3 | TRINITY**
