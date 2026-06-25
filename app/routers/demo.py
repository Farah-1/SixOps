from __future__ import annotations

from fastapi import APIRouter, Query

from services.demo_engine import run_cpu_stress

router = APIRouter(prefix="/api/v1/demo", tags=["Backend Demo"])


@router.get("/status", summary="Demo API status")
def demo_status():
    return {
        "status": "ready",
        "layer": "backend-demo",
        "frontend_visible": False,
        "available_endpoints": {
            "stress": "/api/v1/demo/stress",
            "legacy_stress_alias": "/stress",
        },
        "message": "Demo controls are backend-only and hidden from the customer store UI.",
    }


@router.get("/stress", summary="Run backend CPU stress workload")
def stress(iterations: int = Query(default=8_000_000, ge=100_000, le=30_000_000)):
    result = run_cpu_stress(iterations)
    return {
        "status": "completed",
        "layer": "backend-demo",
        "workload": "cpu-stress",
        "iterations": result.iterations,
        "duration_ms": result.duration_ms,
        "result": result.result,
        "message": "Use this endpoint from curl, a load-generator pod, or demo scripts to trigger scaling tests.",
    }
