"""Backend-only demo workloads used by Kubernetes scaling experiments."""
from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class StressResult:
    iterations: int
    result: int
    duration_ms: int


def run_cpu_stress(iterations: int = 8_000_000) -> StressResult:
    """Run a controlled CPU-heavy loop for demo traffic and HPA/optimizer tests."""
    start = time.perf_counter()
    total = 0
    for i in range(iterations):
        total += i * i
    duration_ms = int((time.perf_counter() - start) * 1000)
    return StressResult(iterations=iterations, result=total, duration_ms=duration_ms)
