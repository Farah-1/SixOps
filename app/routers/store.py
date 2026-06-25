from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from services.product_catalog import catalog_summary, get_product, list_products

router = APIRouter(prefix="/api/v1/store", tags=["Store"])


@router.get("/products", summary="List store products")
def products(
    category: str | None = Query(default=None, description="Optional category filter"),
    search: str | None = Query(default=None, description="Optional product search term"),
):
    results = list_products(category=category, search=search)
    return {
        "status": "success",
        "store": "GadgetNest",
        "summary": catalog_summary(),
        "count": len(results),
        "products": results,
    }


@router.get("/products/{product_id}", summary="Get product details")
def product_details(product_id: int):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status": "success",
        "product": product,
    }


@router.get("/cart/sample", summary="Show sample cart")
def cart_sample():
    return {
        "status": "success",
        "cart": [
            {"product": "NovaBook Pro 14", "quantity": 1, "unit_price": 1200},
            {"product": "SwiftClick Mouse", "quantity": 2, "unit_price": 40},
        ],
        "message": "Sample cart response for frontend and API testing.",
    }


@router.post("/checkout", summary="Simulate checkout")
def checkout():
    return {
        "status": "success",
        "order_id": "GN-DEMO-1001",
        "message": "GadgetNest order placed successfully.",
    }
