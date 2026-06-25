"""Backward-compatible endpoints for the older frontend/scripts."""
from __future__ import annotations

from fastapi import APIRouter

from services.demo_engine import run_cpu_stress
from services.optimizer_engine import recommend_replicas
from services.product_catalog import list_products

router = APIRouter(include_in_schema=False)


@router.get("/products")
def products_alias():
    return {"status": "success", "store": "GadgetNest", "products": list_products()}


@router.get("/cart")
def cart_alias():
    return {
        "status": "success",
        "cart": [
            {"product": "NovaBook Pro 14", "quantity": 1},
            {"product": "SwiftClick Mouse", "quantity": 2},
        ],
    }


@router.get("/checkout")
def checkout_alias():
    return {"status": "success", "message": "GadgetNest order placed successfully"}


@router.get("/stress")
def stress_alias():
    result = run_cpu_stress()
    return {
        "status": "stress completed",
        "layer": "backend-demo",
        "duration_ms": result.duration_ms,
        "result": result.result,
        "new_endpoint": "/api/v1/demo/stress",
    }


@router.get("/api/demo/stress")
def old_demo_stress_alias():
    result = run_cpu_stress()
    return {
        "status": "completed",
        "layer": "backend-demo",
        "duration_ms": result.duration_ms,
        "result": result.result,
        "new_endpoint": "/api/v1/demo/stress",
    }


@router.get("/api/aiops/status")
def old_aiops_status_alias():
    return {
        "status": "ready",
        "new_endpoint": "/api/v1/aiops/status",
    }


@router.get("/api/optimizer/replica-recommendation")
def old_optimizer_alias(
    current_replicas: int = 2,
    total_cpu_millicores: int = 900,
    target_cpu_per_replica: int = 500,
    min_replicas: int = 2,
    max_replicas: int = 6,
):
    recommendation = recommend_replicas(
        current_replicas=current_replicas,
        total_cpu_millicores=total_cpu_millicores,
        target_cpu_per_replica=target_cpu_per_replica,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
    )
    return {
        "status": "success",
        "new_endpoint": "/api/v1/optimizer/replica-recommendation",
        "action": recommendation.action,
        "current_replicas": recommendation.current_replicas,
        "recommended_replicas": recommendation.recommended_replicas,
    }
