# SPDX-License-Identifier: Apache-2.0
# Licensed under Apache License 2.0 — http://www.apache.org/licenses/LICENSE-2.0

# Integration Guide for TRINITY CLARA

This guide provides best practices for integrating VSA, AR, and ML components in TRINITY systems.

---

## 1. VSA Integration

### Quick Import

```python
from specs.vsa_bridge import encode_fact, decode_to_fact, similarity_fact_query
```

### Best Practices

1. **Always use centralized VSA operations** — Don't reimplement bind/unbind/bundle
   ```python
   # CORRECT: Use bridge API
   encoded = encode_fact({'entity': 'king', 'type': 'entity'})
   
   # INCORRECT: Local implementation
   encoded = [trit_neg if v < 0 else trit_pos for v in features]
   ```

2. **Use MAX_FACTS for memory management** — Prevents unbounded growth
   ```python
   results = similarity_fact_query(query_vector, MAX_FACTS=256)
   ```

3. **Encode facts, not raw values** — Use encode_fact() for AR integration
   ```python
   # CORRECT: VSA encoding
   fact_hv = encode_fact({'patient': '001', 'symptom': 'fever'})
   
   # INCORRECT: Raw fact
   fact_hv = [0.5, -0.2, 0.8, 0, 0]
   ```

---

## 2. AR Reasoning Integration

### Quick Import

```python
from specs.ar.ternary_logic import k3_and, k3_or, k3_not, TRIT_NEG, TRIT_UNKNOWN, TRIT_POS
from specs.ar.proof_trace import MAX_STEPS
```

### Best Practices

1. **Respect MAX_STEPS=10** — All AR reasoning must be bounded
   ```python
   # Always check step limit
   for rule in rules:
       if step_count >= MAX_STEPS:
           break  # Must enforce CLARA requirement
   ```

2. **Use K3 quality levels** — Represent uncertainty explicitly
   ```python
   # Use Trit values (not boolean)
   def classify_symptom(severity: str) -> Trit:
       if severity == 'critical':
           return TRIT_POS  # Definitely present
       elif severity == 'absent':
           return TRIT_NEG  # Definitely not present
       else:
           return TRIT_UNKNOWN  # Unsure (bounded rationality)
   ```

3. **Always return explanation** — Provide proof trace
   ```python
   from dataclasses import dataclass
   
   @dataclass
   class Conclusion:
       prediction: str
       confidence: float
       proof_trace: List[Step]  # REQUIRED for explainability
       steps_used: int  # Must be ≤ 10
   ```

---

## 3. Confidence Scoring

### GF16 Encoding

```python
from specs.numeric.gf16 import GF16_ZERO, GF16_ONE

def encode_confidence(conf: float) -> GF16:
    """Encode confidence using GF16 for optimal range."""
    # Clamp to [0.1, 0.9] for GF16
    clamped = max(0.1, min(0.9, conf))
    # Scale to 0-65535 for GF16
    return int(clamped * 65535)
```

### Combination Strategy

```python
def weighted_confidence(vsa_conf: float, ml_conf: float, ar_conf: float) -> float:
    """Combine confidence scores from multiple sources."""
    weights = [0.3, 0.35, 0.35]  # VSA, ML, AR
    
    # Normalize (already [0,1])
    vsa_norm = max(0.0, min(1.0, vsa_conf))
    ml_norm = max(0.0, min(1.0, ml_conf))
    ar_norm = max(0.0, min(1.0, ar_conf))
    
    # Weighted average
    return sum(w * c for w, c in zip(weights, [vsa_norm, ml_norm, ar_norm])) / sum(weights)
```

---

## 4. Full ML+AR Pipeline

### Complete Pattern

```python
from dataclasses import dataclass
from typing import List

@dataclass
class CompositionResult:
    """Result of ML+AR composition."""
    prediction: str
    confidence: float
    vsa_confidence: float
    ml_confidence: float
    ar_confidence: float
    explanation: str
    proof_trace: List[Step]
    steps_used: int  # Must be ≤ 10

def compose_ml_ar_vsa(
    raw_input,
    ml_classifier,
    ar_reasoner,
    max_steps=10
) -> CompositionResult:
    """Complete ML+VSA+AR composition pipeline."""
    
    # Step 1: ML Feature Extraction
    ml_result = ml_classifier.predict(raw_input)
    
    # Step 2: VSA Encoding
    hv_input = encode_fact({'input': raw_input})
    
    # Step 3: VSA Similarity Search
    similar_hv = similarity_fact_query(hv_input, MAX_FACTS=128)
    
    # Step 4: AR Reasoning (bounded)
    ar_result = ar_reasoner.reason(
        facts=decode_to_fact(similar_hv),
        max_steps=max_steps - 4  # Reserve for proof generation
    )
    
    # Step 5: Proof Trace Generation
    proof_steps = ar_result.trace
    
    # Step 6: Explanation Generation
    explanation = generate_explanation(proof_steps, ml_result)
    
    # Combine confidences
    final_confidence = weighted_confidence(
        vsa_conf=similar_hv['confidence'],
        ml_conf=ml_result['confidence'],
        ar_conf=ar_result.confidence
    )
    
    return CompositionResult(
        prediction=ar_result.conclusion,
        confidence=final_confidence,
        explanation=explanation,
        proof_trace=proof_steps,
        steps_used=len(proof_steps)
    )
```

---

## 5. Adversarial Robustness

### Detection Strategy

```python
def is_adversarial(input_data: dict) -> bool:
    """Check if input might be adversarial."""
    suspicious_indicators = 0
    
    # Check 1: Fuel deception (reported ≠ actual)
    if 'fuel_reported' in input_data and 'fuel_actual' in input_data:
        if abs(input_data['fuel_reported'] - input_data['fuel_actual']) > 0.1:
            suspicious_indicators += 1
    
    # Check 2: Action sequence exhaustion (many small actions)
    if 'actions' in input_data:
        if len(input_data['actions']) > 100:
            suspicious_indicators += 1
    
    # Check 3: Timeline manipulation (compressed timeline)
    if 'timeline_reported' in input_data and 'timeline_actual' in input_data:
        reported_duration = input_data['timeline_reported']
        actual_duration = input_data['timeline_actual']
        if actual_duration > reported_duration * 1.5:
            suspicious_indicators += 1
    
    # Check 4: Resource poisoning (invalid confidence values)
    if 'confidence' in input_data:
        if not (0.0 <= input_data['confidence'] <= 1.0):
            suspicious_indicators += 1
    
    # Check 5: Proof trace manipulation (excessive steps)
    if 'proof_trace' in input_data:
        if len(input_data['proof_trace']) > 10:
            suspicious_indicators += 1
    
    return suspicious_indicators >= 2  # Multiple indicators required
```

### Guardrail Response

```python
def apply_guardrails(input_data: dict, ar_result: Conclusion) -> dict:
    """Apply safety guardrails to AR result."""
    
    # Check if adversarial detected
    if is_adversarial(input_data):
        # Return safe default with explanation
        return {
            'prediction': 'SAFE_DEFAULT',
            'confidence': 1.0,
            'explanation': 'Adversarial pattern detected, returning safe default',
            'block_reason': 'ADVERSARIAL',
            'steps_used': 0
        }
    
    # Check AR confidence is sufficient
    if ar_result.confidence < MIN_QUALITY:  # MIN_QUALITY = 0.7
        # Request clarification
        return {
            'prediction': ar_result.prediction,
            'confidence': ar_result.confidence,
            'explanation': f'Low confidence ({ar_result.confidence:.2f}), additional context requested',
            'needs_clarification': True
        }
    
    # Return normal result
    return {
        'prediction': ar_result.prediction,
        'confidence': ar_result.confidence,
        'explanation': ar_result.explanation,
        'proof_trace': ar_result.proof_trace,
        'steps_used': ar_result.steps_used,
        'needs_clarification': False
    }
```

---

## 6. Testing Guidelines

### Unit Testing

```python
import pytest
from dataclasses import dataclass

@dataclass
class TestCase:
    input_data: dict
    expected_output: dict
    description: str

def test_example(test_case: TestCase) -> bool:
    """Run example and verify output."""
    result = compose_ml_ar_vsa(
        test_case.input_data,
        ml_classifier=MLClassifier(),
        ar_reasoner=ARReasoner(),
        max_steps=10
    )
    
    # Verify prediction
    assert result.prediction == test_case.expected_output['prediction']
    
    # Verify confidence range
    assert 0.0 <= result.confidence <= 1.0
    
    # Verify step count
    assert result.steps_used <= 10, f"Step limit exceeded: {result.steps_used}"
    
    # Verify proof trace exists
    assert len(result.proof_trace) > 0, "No proof trace generated"
    
    return True
```

### Integration Testing

```python
def test_vsa_integration():
    """Test VSA bridge layer integration."""
    
    # Test 1: Encoding
    test_fact = encode_fact({'key': 'test', 'value': 123})
    decoded_fact = decode_to_fact(test_fact)
    assert decoded_fact['key'] == 'test'
    assert decoded_fact['value'] == '123'
    
    # Test 2: Similarity query
    test_hv1 = encode_fact({'a': 1, 'b': 2})
    test_hv2 = encode_fact({'a': 1, 'b': 2})
    similarity = similarity_fact_query(test_hv1, test_hv2)
    assert similarity['match'] == True
    assert 0.8 < similarity['confidence'] < 1.0
    
    return True
```

---

## 7. Common Pitfalls

### ❌ DO NOT

1. **Do NOT implement local VSA operations** in each example
   ```python
   # INCORRECT: Reimplements bind/unbind
   def bind(self, a, b):
       # ... local implementation
   ```
   
   ```python
   # CORRECT: Use bridge API
   from specs.vsa_bridge import bind
   ```

2. **Do NOT exceed MAX_STEPS=10** in AR reasoning
   ```python
   # INCORRECT: Unbounded reasoning loop
   while True:
       result = apply_rule(result)
       if not result.done:
           continue  # Never terminates!
   ```
   
   ```python
   # CORRECT: Bounded loop
   for i in range(MAX_STEPS):
       result = apply_rule(result)
       if result.done:
           break  # Enforces termination
   ```

3. **Do NOT use boolean logic** for uncertainty
   ```python
   # INCORRECT: Boolean cannot represent uncertainty
   is_diagnosed = True  # No uncertainty
   ```
   
   ```python
   # CORRECT: Use K3 Trit values
   diagnosis_trit = TRIT_POS  # Definite
   diagnosis_trit = TRIT_UNKNOWN  # Uncertain (bounded)
   ```

4. **Do NOT return raw proof traces** without formatting
   ```python
   # INCORRECT: Raw data dump
   return steps
   ```
   
   ```python
   # CORRECT: Formatted explanation
   return generate_explanation(steps, format='natural')
   ```

### ✅ DO

1. **Always use centralized VSA operations** via bridge API
2. **Always enforce MAX_STEPS=10** in AR reasoning
3. **Use K3 Trit values** for CLARA restraint compliance
4. **Always return formatted explanations** with proof traces
5. **Implement adversarial detection** for defense systems
6. **Apply guardrails** at all decision points
7. **Test integration points** between VSA, AR, and ML components

---

## 8. Debugging Tips

### Enable Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

class DebuggableSystem:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def debug_step(self, step: str, data: dict):
        """Log a reasoning step with full context."""
        self.logger.debug(f"[{step}] Data: {data}")
    
    def debug_vsa(self, op: str, input_data: dict, output: dict):
        """Log VSA operation with inputs and outputs."""
        self.logger.debug(f"[{op}] Input: {input_data}")
        self.logger.debug(f"[{op}] Output: {output}")
```

### Use Assertions

```python
# Development assertions (disabled in production)
DEBUG_MODE = True

def assert_vsa_dimensions(hv: List[int]) -> None:
    """Assert VSA hypervector has correct dimensions."""
    assert len(hv) == VSA_DIM, f"Invalid VSA dimensions: {len(hv)}, expected {VSA_DIM}"

def assert_trit_value(trit: int) -> None:
    """Assert Trit value is valid (-1, 0, or 1)."""
    assert trit in [TRIT_NEG, TRIT_ZERO, TRIT_POS], f"Invalid Trit value: {trit}"

# Usage in development
if DEBUG_MODE:
    assert_vsa_dimensions(encoded_vector)
    assert_trit_value(result[-1])
```

---

## 9. Performance Optimization

### Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_similarity_fact_query(query_hv: List[int]) -> dict:
    """Cache VSA similarity queries to avoid recomputation."""
    return similarity_fact_query(query_hv, MAX_FACTS=128)

# Usage
result1 = cached_similarity_fact_query(vector1)
result2 = cached_similarity_fact_query(vector1)  # Returns cached result
```

### Vector Operations

```python
# Use built-in Python operations for VSA operations
import numpy as np

def fast_bundle(hvs: List[List[int]]) -> List[int]:
    """Fast bundle operation using NumPy."""
    # Convert to numpy array
    arr = np.array(hvs, dtype=np.int8)
    
    # Majority vote (2/3 rule)
    # Initialize result array
    result = np.zeros(len(hvs[0]), dtype=np.int8)
    
    # Count votes for each position
    for hv in hvs[1:]:
        result += (hv == 1).astype(np.int8)
    
    # Majority decision
    result = (result > len(hvs) // 2).astype(np.int8)
    
    return result.tolist()
```

---

## 10. Code Organization

### File Structure

```
trinity-clara/
├── integration/
│   ├── vsa_bridge.py        # VSA bridge layer
│   ├── ar_bridge.py          # AR integration
│   └── common.py            # Shared utilities
├── tests/
│   ├── test_vsa_bridge.py    # VSA integration tests
│   ├── test_ar_bridge.py      # AR integration tests
│   └── test_integration.py    # End-to-end tests
└── docs/
    ├── INTEGRATION_GUIDE.md # This file
    ├── API_REFERENCE.md     # Complete API documentation
    └── ARCHITECTURE.md     # System architecture
```

### Module Naming

```
# Use descriptive module names
module_name: "vsa_bridge"  # CORRECT: Clear and specific
module_name: "bridge"          # INCORRECT: Too generic

# Use descriptive function names
def encode_fact(data: dict) -> List[int]:  # CORRECT: Clear purpose
def process(data: dict) -> dict:        # INCORRECT: Too generic
```

---

**φ² + 1/φ² = 3 | TRINITY**
