from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/aiops", tags=["AIOps"])


@router.get("/status", summary="AIOps backend status")
def aiops_status():
    return {
        "status": "ready",
        "layer": "backend-aiops",
        "frontend_visible": False,
        "modules": {
            "optimizer_manager": "optimizer/optimizer_manager.py",
            "replica_recommender": "optimizer/replica_cost_recommender.py",
            "prometheus_queries": "monitoring/prometheus_queries.md",
            "rag_notes": "rag/hpa_explanation.md",
        },
        "api_groups": {
            "demo": "/api/v1/demo",
            "optimizer": "/api/v1/optimizer",
            "docs": "/docs",
        },
        "message": "AIOps and demo features are separated from the customer-facing store frontend.",
    }
