"""Replica recommendation logic for the backend API.

This is deliberately separate from the router so the project looks like a real
AIOps backend and the scaling decision can be reused by CLI scripts later.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ReplicaRecommendation:
    current_replicas: int
    recommended_replicas: int
    action: str
    total_cpu_millicores: int
    target_cpu_per_replica: int
    min_replicas: int
    max_replicas: int
    estimated_current_cost_per_hour: float
    estimated_recommended_cost_per_hour: float
    estimated_saving_per_hour: float


def recommend_replicas(
    *,
    current_replicas: int,
    total_cpu_millicores: int,
    target_cpu_per_replica: int = 500,
    min_replicas: int = 2,
    max_replicas: int = 6,
    cost_per_replica_per_hour: float = 0.10,
) -> ReplicaRecommendation:
    """Return a cost-aware replica recommendation.

    The decision supports both scale up and scale down. This avoids the old demo
    issue where the optimizer only reduced replicas and never increased them.
    """
    if min_replicas > max_replicas:
        raise ValueError("min_replicas cannot be greater than max_replicas")

    raw_needed = math.ceil(total_cpu_millicores / target_cpu_per_replica) if total_cpu_millicores else min_replicas
    recommended = max(min_replicas, min(max_replicas, raw_needed))

    if recommended > current_replicas:
        action = "scale_up"
    elif recommended < current_replicas:
        action = "scale_down"
    else:
        action = "keep_current"

    current_cost = round(current_replicas * cost_per_replica_per_hour, 3)
    recommended_cost = round(recommended * cost_per_replica_per_hour, 3)
    saving = round(current_cost - recommended_cost, 3)

    return ReplicaRecommendation(
        current_replicas=current_replicas,
        recommended_replicas=recommended,
        action=action,
        total_cpu_millicores=total_cpu_millicores,
        target_cpu_per_replica=target_cpu_per_replica,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        estimated_current_cost_per_hour=current_cost,
        estimated_recommended_cost_per_hour=recommended_cost,
        estimated_saving_per_hour=saving,
    )
