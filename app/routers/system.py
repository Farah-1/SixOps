from __future__ import annotations

from fastapi import APIRouter

from services.product_catalog import catalog_summary

router = APIRouter(tags=["System"])


@router.get("/health", summary="Service health")
def health():
    return {
        "status": "healthy",
        "service": "gadgetnest-backend",
        "version": "2.0.0",
        "store_summary": catalog_summary(),
    }


@router.get("/api/v1/backend", summary="Backend overview")
def backend_overview():
    return {
        "status": "ready",
        "service": "GadgetNest Backend API",
        "frontend": "Customer store UI is served from /",
        "docs": "/docs",
        "api_groups": {
            "store": "/api/v1/store",
            "aiops": "/api/v1/aiops",
            "demo": "/api/v1/demo",
            "optimizer": "/api/v1/optimizer",
        },
        "legacy_aliases": ["/products", "/cart", "/checkout", "/stress"],
    }
