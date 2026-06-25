from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from services.optimizer_engine import recommend_replicas

router = APIRouter(prefix="/api/v1/optimizer", tags=["Optimizer"])


@router.get("/replica-recommendation", summary="Recommend replica count")
def replica_recommendation(
    current_replicas: int = Query(default=2, ge=1, le=20),
    total_cpu_millicores: int = Query(default=900, ge=0),
    target_cpu_per_replica: int = Query(default=500, ge=100),
    min_replicas: int = Query(default=2, ge=1),
    max_replicas: int = Query(default=6, ge=1),
    cost_per_replica_per_hour: float = Query(default=0.10, ge=0),
):
    try:
        recommendation = recommend_replicas(
            current_replicas=current_replicas,
            total_cpu_millicores=total_cpu_millicores,
            target_cpu_per_replica=target_cpu_per_replica,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            cost_per_replica_per_hour=cost_per_replica_per_hour,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "success",
        "layer": "backend-aiops",
        "decision": recommendation.action,
        "current_replicas": recommendation.current_replicas,
        "recommended_replicas": recommendation.recommended_replicas,
        "total_cpu_millicores": recommendation.total_cpu_millicores,
        "target_cpu_per_replica": recommendation.target_cpu_per_replica,
        "limits": {
            "min_replicas": recommendation.min_replicas,
            "max_replicas": recommendation.max_replicas,
        },
        "cost": {
            "current_per_hour": recommendation.estimated_current_cost_per_hour,
            "recommended_per_hour": recommendation.estimated_recommended_cost_per_hour,
            "saving_per_hour": recommendation.estimated_saving_per_hour,
        },
        "note": "Backend-only recommendation. The frontend remains a clean online store.",
    }
