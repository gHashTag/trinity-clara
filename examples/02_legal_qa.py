#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Licensed under Apache License 2.0 —
# http://www.apache.org/licenses/LICENSE-2.0
"""
Example 2: Legal Document QA with VSA Semantic Memory
======================================================

Composition: Query Encoder → VSA Similarity Search → Retrieval → AR

This example demonstrates question answering over legal documents using:
1. Query encoding to hypervectors
2. VSA similarity search for context retrieval
3. AR reasoning over retrieved context
4. Bounded step limit for explainability

Uses centralized VSA Bridge Layer (specs/ar/vsa_bridge.t27)

Author: T27 Trinity S³AI Project
Reference: examples/vsa_bridge.py
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import math
import sys
import os

# Add parent directory to path for VSA Bridge import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vsa_bridge import (
    VSA_DIMENSION, MAX_FACTS, SIMILARITY_THRESHOLD, TRIT_NEG,
    TRIT_ZERO, TRIT_POS, Trit, HyperVector, HornClause,
    FactEncoding, encode_fact, similarity_fact_query
    cosine_similarity, trit_to_str
)


# ============================================================================
# AR Operations (from specs/ar/datalog_engine.t27)
# ============================================================================

MAX_STEPS = 10


@dataclass
class Fact:
    predicate: str
    value: str


@dataclass
class Rule:
    if_predicate: str
    if_value: str
    then_conclusion: str


@dataclass
class Step:
    step_number: int
    action: str
    premise: str
    conclusion: str


@dataclass
class Answer:
    answer: str
    confidence: float
    trace: List[Step]


@dataclass
class LegalDocument:
    """A legal document with pre-encoded hypervector."""
    doc_id: str
    title: str
    category: str
    content: str
    hypervector: HyperVector


class LegalQASystem:
    """
    Complete legal QA system combining VSA and AR.

    Now uses centralized VSA Bridge Layer for VSA operations.
    """

    def __init__(self, similarity_threshold: float = SIMILARITY_THRESHOLD):
        self.similarity_threshold = similarity_threshold
        self.documents: List[LegalDocument] = self._load_documents()
        self.rules: List[Rule] = self._load_rules()
        self.fact_encodings: List[FactEncoding] = []

    def _load_documents(self) -> List[LegalDocument]:
        """Load legal documents with pre-encoded hypervectors."""
        return [
            LegalDocument(
                doc_id="apache_2.0",
                title="Apache License 2.0",
                category="license",
                content="The Apache License 2.0 is a permissive free software license. "
                         "It allows users to use the software for any purpose, to distribute it, "
                         "to modify it, and to distribute modified versions under the terms of the license. "
                         "Key provisions: patent grant, redistribution rights, attribution requirement, "
                         "warranty disclaimer, and liability limitation.",
                hypervector=self._generate_document_hypervector(1)
            ),
            LegalDocument(
                doc_id="mit_license",
                title="MIT License",
                category="license",
                content="The MIT License is a permissive free software license. "
                         "It is very short and simple, allowing users to do almost anything with the software. "
                         "Key provisions: permission notice, attribution requirement, warranty disclaimer, "
                         "and liability limitation. Unlike Apache 2.0, it does not include an explicit patent grant.",
                hypervector=self._generate_document_hypervector(2)
            ),
            LegalDocument(
                doc_id="contract_requirements",
                title="Valid Contract Requirements",
                category="legal",
                content="For a contract to be valid, it must have: offer and acceptance, "
                         "consideration (something of value), capacity of parties, lawful purpose, "
                         "mutual assent (meeting of minds). Valid contracts can be "
                         "expressed or implied, written or oral, executed or executory.",
                hypervector=self._generate_document_hypervector(3)
            ),
            LegalDocument(
                doc_id="patent_protection",
                title="Patent Protection in Open Source",
                category="legal",
                content="Open source software typically does not include patent protection for end users. "
                         "However, some licenses (like Apache 2.0) include patent grants to "
                         "recipients. Users can still be subject to patent litigation from third parties.",
                hypervector=self._generate_document_hypervector(4)
            ),
        ]

    def _generate_document_hypervector(self, seed: int) -> HyperVector:
        """Generate a deterministic hypervector for a document."""
        import random
        random.seed(seed)
        return [random.choice([TRIT_NEG, TRIT_ZERO, TRIT_POS])
                for _ in range(VSA_DIMENSION)]

    def _load_rules(self) -> List[Rule]:
        """Load AR rules for legal reasoning."""
        return [
            Rule(
                if_predicate="license_type",
                if_value="apache_2.0",
                then_conclusion="has_patent_grant"
            ),
            Rule(
                if_predicate="license_type",
                if_value="mit",
                then_conclusion="no_patent_grant"
            ),
            Rule(
                if_predicate="has_patent_grant",
                if_value="yes",
                then_conclusion="requires_attribution"
            ),
            Rule(
                if_predicate="document_type",
                if_value="contract",
                then_conclusion="requires_consent"
            ),
            Rule(
                if_predicate="data_type",
                if_value="personal",
                then_conclusion="requires_consent"
            ),
            Rule(
                if_predicate="has_patent_grant",
                if_value="no",
                then_conclusion="implicit_patent"
            ),
        ]

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Tuple[float, LegalDocument]]:
        """
        Retrieve relevant documents using VSA similarity search.

        Now uses centralized VSA Bridge Layer.
        """
        # Encode query using centralized VSA Bridge
        query_fact = HornClause(
            name=hash(query),
            args=[TRIT_POS],
            arg_count=1
        )
        query_encoding = encode_fact(query_fact, self)

        # Build list of document encodings for similarity query
        doc_encodings = [
            encode_fact(HornClause(
                name=hash(doc.doc_id),
                args=[TRIT_POS],
                arg_count=1
            ), self)
            for doc in self.documents
        ]

        # Query using centralized VSA Bridge similarity_fact_query
        query_result = similarity_fact_query(query_encoding.hypervector, self, limit=MAX_FACTS)

        # Extract similar documents
        results = []
        for fact_enc in query_result.matches:
            # Find matching document
            for doc in self.documents:
                if doc.doc_id == str(fact_enc.original_fact.name):
                    results.append((fact_encodings[self.fact_encodings.index(fact_enc)] if self.fact_encodings.index(fact_enc) < len(self.fact_encodings) else fact_enc, doc))
                    if len(results) >= top_k:
                        break

        return results[:top_k]

    def extract_facts(self, documents: List[Tuple[float, LegalDocument]]) -> List[Fact]:
        """Extract facts from retrieved documents."""
        facts = []
        for _, doc in documents:
            f = Fact("context_source", doc.doc_id)
            f.source = doc.doc_id
            facts.append(f)

            # Extract simple keyword facts
            content_lower = doc.content.lower()
            if "contract" in content_lower:
                f = Fact("document_type", "contract")
                f.source = doc.doc_id
                facts.append(f)
            if "apache" in content_lower:
                f = Fact("license_type", "apache_2.0")
                f.source = doc.doc_id
                facts.append(f)
            if "mit" in content_lower:
                f = Fact("license_type", "mit")
                f.source = doc.doc_id
                facts.append(f)
            if "patent" in content_lower:
                f = Fact("has_patent_grant", "yes")
                f.source = doc.doc_id
                facts.append(f)
            if "personal data" in content_lower or "personal" in content_lower:
                f = Fact("data_type", "personal")
                f.source = doc.doc_id
                facts.append(f)

        return facts

    def answer_question(self, question: str) -> Dict:
        """
        Complete QA pipeline using centralized VSA Bridge.

        Pipeline:
        1. Encode query to hypervector (using VSA Bridge)
        2. Retrieve similar documents via similarity search (using VSA Bridge)
        3. Extract facts from retrieved context
        4. AR reasoning with bounded steps (≤10)
        5. Return answer with explanation and sources
        """
        # Step 1: Retrieve context (using VSA Bridge)
        retrieved = self.retrieve_context(question, top_k=3)

        # Step 2: Extract facts
        facts = self.extract_facts(retrieved)

        # Step 3: AR reasoning (bounded)
        answer = forward_chain(facts, self.rules, MAX_STEPS)

        # Format result
        return {
            "question": question,
            "answer": answer.answer,
            "confidence": answer.confidence,
            "explanation": self._format_explanation(answer),
            "sources": self._format_sources(retrieved),
            "steps_used": len(answer.trace),
            "step_limit": MAX_STEPS,
            "vsa_bridge_used": True  # Document VSA Bridge usage
        }

    def _format_explanation(self, answer: Answer) -> str:
        """Format reasoning explanation."""
        if not answer.trace:
            return "No reasoning steps performed."

        lines = ["Reasoning Trace:"]
        for step in answer.trace:
            lines.append(f"  Step {step.step_number}: {step.action}")
            lines.append(f"    {step.premise} → {step.conclusion}")

        return "\n".join(lines)

    def _format_sources(self, retrieved: List[Tuple[float, LegalDocument]]) -> List[Dict]:
        """Format retrieved sources."""
        return [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "similarity": sim,
                "category": doc.category
            }
            for sim, doc in retrieved
        ]


def forward_chain(facts: List[Fact], rules: List[Rule],
                   max_steps: int = MAX_STEPS) -> Answer:
    """
    Forward-chaining AR with bounded step limit.

    Simplified for legal QA demonstration.
    """
    trace: List[Step] = []
    steps = 0
    answer = "UNKNOWN"

    for rule in rules:
        if steps >= max_steps:
            break

        # Check if rule condition is satisfied
        condition_met = any(
            f.predicate == rule.if_predicate and f.value == rule.if_value
            for f in facts
        )

        if condition_met:
            steps += 1
            trace.append(Step(
                step_number=steps,
                action="apply_rule",
                premise=f"{rule.if_predicate}={rule.if_value}",
                conclusion=rule.then_conclusion
            ))
            answer = rule.then_conclusion

    confidence = 1.0 if steps <= max_steps // 2 else 0.5

    return Answer(
        answer=answer,
        confidence=confidence,
        trace=trace
    )


# ============================================================================
# Main: Example Usage
# ============================================================================

def main():
    """Run the legal QA example."""
    print("=" * 60)
    print("Legal Document QA - VSA Semantic Memory + AR")
    print("=" * 60)
    print()
    print("Note: Now uses centralized VSA Bridge Layer (examples/vsa_bridge.py)")
    print()

    # Initialize system
    qa = LegalQASystem(similarity_threshold=0.4)

    # Example questions
    questions = [
        "What does Apache 2.0 license include?",
        "What is required for a valid contract?",
        "Does open source software have patent protection?",
    ]

    for question in questions:
        print("-" * 60)
        print(f"Q: {question}")
        print()

        result = qa.answer_question(question)

        print(f"A: {result['answer']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print()
        print("Explanation:")
        print(result['explanation'])
        print()
        print("Retrieved Sources:")
        for source in result['sources']:
            print(f"  - [{source['doc_id']}] {source['title']} (similarity: {source['similarity']:.2f})")
        print()
        print(f"Steps used: {result['steps_used']}/{MAX_STEPS}")
        print(f"VSA Bridge used: {result['vsa_bridge_used']}")
        print()


if __name__ == "__main__":
    main()
