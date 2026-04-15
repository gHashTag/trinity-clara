#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Licensed under Apache License 2.0 —
# http://www.apache.org/licenses/LICENSE-2.0
"""
Example 3: Autonomous Driving with RL + VSA + Safety Constraints
================================================================

Composition: RL Policy Network → VSA Encoding → Rule Engine → Guardrails

This example demonstrates autonomous driving decision-making with:
1. RL policy network for action selection
2. VSA encoding for state-action representation
3. Rule engine for safety constraint checking
4. Guardrails for allow/block decisions

Uses centralized VSA Bridge Layer (specs/ar/vsa_bridge.t27)

Safety-critical system with bounded rationality and explicit safety checks.

Author: T27 Trinity S³AI Project
Reference: examples/vsa_bridge.py
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Callable
import math
import sys
import os

# Add parent directory to path for VSA Bridge import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vsa_bridge import (
    VSA_DIMENSION, TRIT_NEG, TRIT_ZERO, TRIT_POS, Trit,
    HyperVector, HornClause, FactEncoding, encode_fact
)


# ============================================================================
# RL Policy Network (simulated)
# ============================================================================

Action = str


@dataclass
class RLState:
    """State representation for RL policy network."""
    ego_velocity: float  # m/s
    ego_acceleration: float  # m/s²
    distance_to_front: float  # m
    front_vehicle_velocity: float  # m/s
    distance_to_rear: float  # m
    rear_vehicle_velocity: float  # m/s
    lane_position: float  # -1=left, 0=center, +1=right
    road_curvature: float  # Curvature of road
    weather_condition: float  # 0=dry, 0.2=light_rain, 0.5=heavy_rain, 0.8=snow
    traffic_density: float  # 0=light, 0.3=medium, 0.6=heavy


@dataclass
class RLPolicyNetwork:
    """
    Simulated RL policy network.

    In production, this would be a trained neural network.
    """

    def select_action(self, state: RLState) -> Tuple[Action, float]:
        """
        Select action based on current state.

        Returns: (action, confidence)
        """
        # Simple rule-based simulation
        # In production, this would be a neural network forward pass
        if state.distance_to_front < 15.0:
            # Vehicle ahead - maintain or reduce speed
            if state.ego_velocity > 15.0:
                return "decelerate", 0.9
            elif state.ego_velocity < 10.0:
                return "accelerate", 0.8
            else:
                return "maintain", 0.9
        elif 15.0 <= state.distance_to_front < 25.0:
            # Moderate distance - check lane
            if state.lane_position != 0.0:
                return "change_lane", 0.7
            else:
                return "maintain", 0.8
        else:
            # Safe following distance
            if state.ego_velocity < 20.0:
                return "accelerate", 0.6
            else:
                return "maintain", 0.8


# ============================================================================
# Safety Constraints
# ============================================================================

@dataclass
class SafetyConstraint:
    """A safety constraint with check function."""
    name: str
    check_fn: Callable[[RLState, Action], bool]
    is_blocking: bool = True


class SafetyRuleEngine:
    """
    Rule engine for safety constraint checking.

    All safety constraints must be satisfied for action to proceed.
    """

    def __init__(self):
        self.constraints = self._load_constraints()

    def _load_constraints(self) -> List[SafetyConstraint]:
        """Load safety constraints for autonomous driving."""
        return [
            SafetyConstraint(
                name="minimum_following_distance",
                check_fn=lambda s, a: self._check_following_distance(s, a),
                is_blocking=True
            ),
            SafetyConstraint(
                name="safe_lane_change",
                check_fn=lambda s, a: self._check_lane_change(s, a),
                is_blocking=True
            ),
            SafetyConstraint(
                name="velocity_limit",
                check_fn=lambda s, a: self._check_velocity_limit(s, a),
                is_blocking=True
            ),
            SafetyConstraint(
                name="weather_adaptation",
                check_fn=lambda s, a: self._check_weather_adaptation(s, a),
                is_blocking=False  # Warning only
            ),
        ]

    def _check_following_distance(self, state: RLState, action: Action) -> bool:
        """Ensure safe following distance."""
        if action == "accelerate":
            # 2-second rule minimum
            min_distance = state.ego_velocity * 2.0
            return state.distance_to_front >= min_distance
        return True

    def _check_lane_change(self, state: RLState, action: Action) -> bool:
        """Ensure lane change is safe."""
        if "lane" in action:
            # Check rear vehicle distance
            return state.distance_to_rear > 15
        return True

    def _check_velocity_limit(self, state: RLState, action: Action) -> bool:
        """Ensure velocity is within safe limits."""
        speed_limit = 30.0  # m/s (~108 km/h)
        if action == "accelerate":
            return state.ego_velocity < speed_limit
        return True

    def _check_weather_adaptation(self, state: RLState, action: Action) -> bool:
        """Warn about weather adaptation."""
        if state.weather_condition > 0.7 and action == "accelerate":
            return False  # Warning: reduce speed in wet conditions
        return True

    def check_constraints(self, state: RLState, action: Action) -> Tuple[bool, List[str]]:
        """
        Check all safety constraints.

        Returns: (all_satisfied, list_of_failed_constraints)
        """
        failed = []
        warnings = []

        for constraint in self.constraints:
            if not constraint.check_fn(state, action):
                if constraint.is_blocking:
                    failed.append(constraint.name)
                else:
                    warnings.append(constraint.name)

        all_satisfied = len(failed) == 0
        return all_satisfied, failed


# ============================================================================
# VSA State Encoding (using centralized VSA Bridge)
# ============================================================================

class VSAStateEncoder:
    """
    Encode RL state-action pairs to hypervectors.

    Uses centralized VSA Bridge Layer for encoding operations.
    """

    def encode_state(self, state: RLState) -> FactEncoding:
        """Encode state to hypervector using VSA Bridge."""
        # Create HornClause from state
        state_fact = HornClause(
            name=1,  # Hash for "state"
            args=[
                TRIT_POS if state.ego_velocity > 15 else TRIT_ZERO,
                TRIT_POS if state.distance_to_front < 25 else TRIT_NEG,
                TRIT_POS if state.weather_condition < 0.5 else TRIT_ZERO,
                TRIT_POS if state.lane_position == 0 else TRIT_ZERO,
                TRIT_POS if state.road_curvature > 0.1 else TRIT_NEG,
            ],
            arg_count=6
        )
        return encode_fact(state_fact, self)

    def encode_action(self, action: Action) -> FactEncoding:
        """Encode action to hypervector using VSA Bridge."""
        action_fact = HornClause(
            name=hash(action),
            args=[TRIT_POS],
            arg_count=1
        )
        return encode_fact(action_fact, self)


# ============================================================================
# Guardrails (from specs/ar/composition.t27)
# ============================================================================

class Guardrails:
    """
    Guardrails system for final allow/block decision.

    Safety-critical: blocks unsafe actions regardless of RL confidence.
    """

    MAX_STEPS = 10  # Bounded rationality

    def __init__(self, safety_engine: SafetyRuleEngine):
        self.safety_engine = safety_engine
        self.emergency_brake_threshold = 0.3  # Distance in meters

    def allow_or_block(self, state: RLState, action: Action,
                   rl_confidence: float) -> Tuple[bool, str]:
        """
        Make final allow/block decision.

        Returns: (allowed, reason)
        """
        # Emergency check
        if state.distance_to_front < self.emergency_brake_threshold:
            if action != "emergency_brake":
                return False, "EMERGENCY: Front vehicle too close"

        # Safety constraints
        safe, failed = self.safety_engine.check_constraints(state, action)
        if not safe:
            return False, f"BLOCKED: {', '.join(failed)}"

        # Allow action
        return True, f"ALLOWED: {action} (confidence: {rl_confidence:.2f})"


# ============================================================================
# Autonomous Driving System (Composition)
# ============================================================================

class AutonomousDrivingSystem:
    """
    Complete autonomous driving pipeline.

    Uses centralized VSA Bridge Layer for VSA operations.
    """

    def __init__(self):
        self.rl_policy = RLPolicyNetwork()
        self.safety_engine = SafetyRuleEngine()
        self.vsa_encoder = VSAStateEncoder()
        self.guardrails = Guardrails(self.safety_engine)

    def decide(self, state: RLState) -> Dict:
        """
        Make driving decision with full safety pipeline.

        Pipeline:
        1. RL policy selects action
        2. VSA encodes state-action pair (using VSA Bridge)
        3. Rule engine checks safety constraints
        4. Guardrails makes final allow/block decision

        Returns: Decision dict with action, allowed, reason, confidence
        """
        # Step 1: RL policy
        action, rl_confidence = self.rl_policy.select_action(state)

        # Step 2: VSA encoding (using VSA Bridge)
        state_encoding = self.vsa_encoder.encode_state(state)

        # Step 3: Safety rule checking
        safe, failed = self.safety_engine.check_constraints(state, action)

        # Step 4: Guardrails decision
        allowed, reason = self.guardrails.allow_or_block(
            state, action, rl_confidence
        )

        return {
            "state_summary": self._summarize_state(state),
            "rl_action": action,
            "rl_confidence": rl_confidence,
            "safety_constraints_satisfied": safe,
            "failed_constraints": failed,
            "allowed": allowed,
            "final_reason": reason,
            "vsa_encoded": len(state_encoding.hypervector) == VSA_DIM,
            "vsa_bridge_used": True  # Document VSA Bridge usage
        }

    def _summarize_state(self, state: RLState) -> str:
        """Summarize state for logging."""
        return (
            f"v={state.ego_velocity:.1f}m/s, "
            f"d_front={state.distance_to_front:.1f}m, "
            f"lane={int(state.lane_position)}, "
            f"weather={state.weather_condition:.1f}"
        )


# ============================================================================
# Main: Example Usage
# ============================================================================

def main():
    """Run the autonomous driving example."""
    print("=" * 60)
    print("Autonomous Driving - RL + VSA + Safety Rules + Guardrails")
    print("=" * 60)
    print()
    print("Note: Now uses centralized VSA Bridge Layer (examples/vsa_bridge.py)")
    print()

    # Initialize system
    ads = AutonomousDrivingSystem()

    # Test scenarios
    scenarios = [
        RLState(
            ego_velocity=20.0,
            ego_acceleration=0.0,
            distance_to_front=50.0,
            front_vehicle_velocity=18.0,
            distance_to_rear=30.0,
            rear_vehicle_velocity=22.0,
            lane_position=0.0,
            road_curvature=0.0,
            weather_condition=0.2,
            traffic_density=0.3
        ),
        RLState(
            ego_velocity=25.0,
            ego_acceleration=1.0,
            distance_to_front=15.0,  # Too close!
            front_vehicle_velocity=20.0,
            distance_to_rear=40.0,
            rear_vehicle_velocity=25.0,
            lane_position=0.0,
            road_curvature=0.0,
            weather_condition=0.5,
            traffic_density=0.5
        ),
        RLState(
            ego_velocity=15.0,
            ego_acceleration=0.0,
            distance_to_front=40.0,
            front_vehicle_velocity=12.0,
            distance_to_rear=20.0,
            rear_vehicle_velocity=18.0,
            lane_position=0.0,
            road_curvature=0.0,
            weather_condition=0.8,  # Wet conditions
            traffic_density=0.4
        ),
        RLState(
            ego_velocity=10.0,
            ego_acceleration=-2.0,
            distance_to_front=8.0,  # Too close for lane change!
            front_vehicle_velocity=12.0,
            distance_to_rear=5.0,
            rear_vehicle_velocity=15.0,
            lane_position=0.0,
            road_curvature=0.0,
            weather_condition=0.3,
            traffic_density=0.6
        ),
    ]

    for i, state in enumerate(scenarios, 1):
        print("-" * 60)
        print(f"Scenario {i}:")
        print(f"  State: {ads._summarize_state(state)}")
        print()

        decision = ads.decide(state)

        print(f"  RL Action: {decision['rl_action']}")
        print(f"  RL Confidence: {decision['rl_confidence']:.2f}")
        print(f"  Safety Constraints Satisfied: {decision['safety_constraints_satisfied']}")
        if decision['failed_constraints']:
            print(f"  Failed Constraints: {decision['failed_constraints']}")
        print(f"  VSA Encoded: {decision['vsa_encoded']} ({VSA_DIM}-dim)")
        print()
        print(f"  FINAL DECISION: {decision['final_reason']}")
        print()
        print(f"VSA Bridge used: {decision['vsa_bridge_used']}")
        print()

    print("=" * 60)
    print("Safety-Critical System: All decisions verified by guardrails")
    print("=" * 60)


if __name__ == "__main__":
    main()
