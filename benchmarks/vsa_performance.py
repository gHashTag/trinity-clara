#!/usr/bin/env python3
"""
VSA Performance Benchmarks for CLARA (PA-25-07-02)
================================================

Measures performance of VSA core operations:
- bind/unbind operations
- bundle2/bundle3 operations
- similarity metrics (cosine, hamming, dot_product)
- permute operations

Uses Python timeit for accurate timing.

Performance targets from specs/vsa/core.t27:
- bind >1M ops/sec (target: <1000ns per 1024-dim bind)
- bundle2 >500K ops/sec (target: <2000ns per 1024-dim bundle2)
- cosine >200K ops/sec (target: <5000ns per 1024-dim cosine)

Author: T27 Trinity Ternary Project
SPDX-License-Identifier: Apache-2.0
"""

import json
import timeit
import statistics
import math
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Callable
from datetime import datetime, timezone
from pathlib import Path


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


def hamming_similarity(a: List[Trit], b: List[Trit], length: int = VSA_DIM) -> float:
    """Hamming similarity normalized to [0, 1]."""
    dist = hamming_distance(a, b, length)
    return 1.0 - (dist / length)


def dot_product(a: List[Trit], b: List[Trit], length: int = VSA_DIM) -> int:
    """Dot product of two hypervectors."""
    return sum(a[i] * b[i] for i in range(length))


def vector_norm(v: List[Trit], length: int = VSA_DIM) -> float:
    """L2 norm of hypervector (count of non-zero elements)."""
    return math.sqrt(sum(1 for i in range(length) if v[i] != TRIT_ZERO))


# ============================================================================
# Benchmark Configuration
# ============================================================================

@dataclass
class BenchmarkConfig:
    """Configuration for benchmark runs."""
    dimension: int = VSA_DIM
    iterations: int = 10000
    warmup_iterations: int = 100
    num_runs: int = 5
    targets: Dict[str, float] = field(default_factory=lambda: {
        'bind_ns': 1000.0,          # 1M ops/sec = <1000ns
        'unbind_ns': 1000.0,         # Same as bind
        'bundle2_ns': 2000.0,         # 500K ops/sec = <2000ns
        'bundle3_ns': 1500.0,          # From specs/vsa/ops.t27
        'cosine_ns': 5000.0,           # 200K ops/sec = <5000ns
        'hamming_distance_ns': 1000.0,  # 1M ops/sec
        'dot_product_ns': 1000.0,       # 1M ops/sec
        'permute_ns': 500.0,           # From specs/vsa/ops.t27
    })


@dataclass
class BenchmarkResult:
    """Result of a single benchmark."""
    name: str
    dimension: int
    mean_time_ns: float
    std_time_ns: float
    min_time_ns: float
    max_time_ns: float
    ops_per_sec: float
    target_ns: float
    target_met: bool
    iterations: int


# ============================================================================
# Benchmark Runner
# ============================================================================

class VSABenchmarkRunner:
    """
    Runs VSA performance benchmarks using timeit.
    """

    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.results: List[BenchmarkResult] = []
        # Pre-generate test vectors (enough for all iterations)
        num_vectors = config.iterations
        self.vectors_a = [generate_random_hv(i * 2, config.dimension) for i in range(num_vectors)]
        self.vectors_b = [generate_random_hv(i * 2 + 1, config.dimension) for i in range(num_vectors)]
        self.vectors_c = [generate_random_hv(i * 3 + 2, config.dimension) for i in range(num_vectors)]

    def _benchmark(self, name: str, operation: Callable,
                 target_key: str) -> BenchmarkResult:
        """
        Run benchmark for a given operation.

        Uses timeit to measure execution time across multiple runs.
        """
        target_ns = self.config.targets[target_key]

        # Warmup
        for i in range(self.config.warmup_iterations):
            idx = i % len(self.vectors_a)
            operation(self.vectors_a[idx], self.vectors_b[idx], self.vectors_c[idx])

        # Actual benchmark runs - use time.perf_counter for direct timing
        times = []
        va, vb, vc = self.vectors_a, self.vectors_b, self.vectors_c
        iters = self.config.iterations

        for run in range(self.config.num_runs):
            # Measure time directly with time.perf_counter
            import time
            start = time.perf_counter()
            for i in range(iters):
                operation(va[i], vb[i], vc[i])
            elapsed = time.perf_counter() - start

            avg_ns = (elapsed / iters) * 1e9
            times.append(avg_ns)

        # Calculate statistics
        mean_ns = statistics.mean(times)
        std_ns = statistics.stdev(times) if len(times) > 1 else 0.0
        min_ns = min(times)
        max_ns = max(times)

        ops_per_sec = 1.0 / (mean_ns / 1e9) if mean_ns > 0 else 0.0
        target_met = mean_ns <= target_ns

        result = BenchmarkResult(
            name=name,
            dimension=self.config.dimension,
            mean_time_ns=mean_ns,
            std_time_ns=std_ns,
            min_time_ns=min_ns,
            max_time_ns=max_ns,
            ops_per_sec=ops_per_sec,
            target_ns=target_ns,
            target_met=target_met,
            iterations=self.config.iterations
        )

        self.results.append(result)
        return result

    # Individual benchmark operations

    def _bench_bind(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> List[Trit]:
        return bind(a, b, self.config.dimension)

    def _bench_unbind(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> List[Trit]:
        bound = bind(a, b, self.config.dimension)
        return unbind(bound, b, self.config.dimension)

    def _bench_bundle2(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> List[Trit]:
        return bundle2(a, b, self.config.dimension)

    def _bench_bundle3(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> List[Trit]:
        return bundle3(a, b, c, self.config.dimension)

    def _bench_cosine(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> float:
        return cosine_similarity(a, b, self.config.dimension)

    def _bench_hamming_distance(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> int:
        return hamming_distance(a, b, self.config.dimension)

    def _bench_hamming_similarity(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> float:
        return hamming_similarity(a, b, self.config.dimension)

    def _bench_dot_product(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> int:
        return dot_product(a, b, self.config.dimension)

    def _bench_permute(self, a: List[Trit], b: List[Trit], c: List[Trit]) -> List[Trit]:
        return permute(a, self.config.dimension, shift=1)

    # Run all benchmarks

    def run_all_benchmarks(self) -> List[BenchmarkResult]:
        """Run all VSA operation benchmarks."""
        print("=" * 70)
        print("VSA Performance Benchmarks")
        print("=" * 70)
        print(f"Dimension: {self.config.dimension}")
        print(f"Iterations per run: {self.config.iterations}")
        print(f"Number of runs: {self.config.num_runs}")
        print()

        benchmarks = [
            ("bind", self._bench_bind, 'bind_ns'),
            ("unbind", self._bench_unbind, 'unbind_ns'),
            ("bundle2", self._bench_bundle2, 'bundle2_ns'),
            ("bundle3", self._bench_bundle3, 'bundle3_ns'),
            ("cosine_similarity", self._bench_cosine, 'cosine_ns'),
            ("hamming_distance", self._bench_hamming_distance, 'hamming_distance_ns'),
            ("hamming_similarity", self._bench_hamming_similarity, 'hamming_distance_ns'),
            ("dot_product", self._bench_dot_product, 'dot_product_ns'),
            ("permute", self._bench_permute, 'permute_ns'),
        ]

        for name, operation, target_key in benchmarks:
            result = self._benchmark(name, operation, target_key)
            self._print_result(result)

        return self.results

    def _print_result(self, result: BenchmarkResult):
        """Print benchmark result in formatted table."""
        status = "PASS" if result.target_met else "FAIL"
        status_color = "\033[92m" if result.target_met else "\033[91m"
        reset = "\033[0m"

        print(f"{result.name:25s} "
              f"{result.mean_time_ns:>8.0f}ns  "
              f"{result.ops_per_sec:>10.0f} ops/s  "
              f"{status_color}{status}{reset} "
              f"(target: {result.target_ns}ns)")

    def get_summary(self) -> Dict:
        """Get summary of all benchmark results."""
        total_passed = sum(1 for r in self.results if r.target_met)
        total_tests = len(self.results)

        return {
            'dimension': self.config.dimension,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_tests': total_tests,
            'passed': total_passed,
            'failed': total_tests - total_passed,
            'results': [
                {
                    'name': r.name,
                    'mean_time_ns': round(r.mean_time_ns, 2),
                    'std_time_ns': round(r.std_time_ns, 2),
                    'min_time_ns': round(r.min_time_ns, 2),
                    'max_time_ns': round(r.max_time_ns, 2),
                    'ops_per_sec': round(r.ops_per_sec, 2),
                    'target_ns': r.target_ns,
                    'target_met': r.target_met,
                }
                for r in self.results
            ]
        }


# ============================================================================
# Results Exporter
# ============================================================================

def export_results(results: Dict, output_path: str):
    """Export benchmark results to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print()
    print(f"Results exported to: {output_path}")


def print_summary(results: Dict):
    """Print summary of benchmark results."""
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Dimension:          {results['dimension']}")
    print(f"Total benchmarks:  {results['total_tests']}")
    print(f"Passed:            {results['passed']} ({results['passed']/results['total_tests']*100:.1f}%)")
    print(f"Failed:            {results['failed']} ({results['failed']/results['total_tests']*100:.1f}%)")
    print()
    print("Performance Targets (from specs/vsa/core.t27):")
    print("  bind >1M ops/sec       (<1000ns per 1024-dim operation)")
    print("  bundle2 >500K ops/sec   (<2000ns per 1024-dim operation)")
    print("  cosine >200K ops/sec    (<5000ns per 1024-dim operation)")
    print()


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Run VSA performance benchmarks."""
    # Configure benchmarks
    config = BenchmarkConfig(
        dimension=VSA_DIM,
        iterations=10000,
        warmup_iterations=100,
        num_runs=5
    )

    # Run benchmarks
    runner = VSABenchmarkRunner(config)
    runner.run_all_benchmarks()
    results_dict = runner.get_summary()

    # Export results
    output_path = Path(__file__).parent.parent / "test_vectors" / "ta2" / "vsa_bench_results.json"
    export_results(results_dict, str(output_path))

    # Print summary
    print_summary(results_dict)

    # Exit with appropriate code
    import sys
    sys.exit(0 if results_dict['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
