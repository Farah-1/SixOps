"""Product catalog data and store helpers for GadgetNest.

Keeping the catalog outside the API router makes the backend easier to read,
test, and extend later with a database.
"""
from __future__ import annotations

from typing import Any

PRODUCTS: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "NovaBook Pro 14",
        "category": "Laptops",
        "price": 1200,
        "old_price": 1450,
        "rating": 4.9,
        "stock": 8,
        "tag": "Best Seller",
        "icon": "💻",
        "badge": "Top Pick",
        "color": "violet",
        "description": "Powerful laptop for study, work, streaming, and multitasking.",
    },
    {
        "id": 2,
        "name": "Pulse Wireless Headphones",
        "category": "Audio",
        "price": 150,
        "old_price": 220,
        "rating": 4.7,
        "stock": 15,
        "tag": "Hot Deal",
        "icon": "🎧",
        "badge": "Noise Canceling",
        "color": "cyan",
        "description": "Noise cancelling headphones for music, calls, and focused work.",
    },
    {
        "id": 3,
        "name": "MechaFlow Keyboard",
        "category": "Accessories",
        "price": 80,
        "old_price": 110,
        "rating": 4.8,
        "stock": 24,
        "tag": "New Arrival",
        "icon": "⌨️",
        "badge": "RGB Edition",
        "color": "green",
        "description": "Mechanical keyboard with smooth typing, RGB lighting, and premium switches.",
    },
    {
        "id": 4,
        "name": "SwiftClick Mouse",
        "category": "Accessories",
        "price": 40,
        "old_price": 60,
        "rating": 4.6,
        "stock": 31,
        "tag": "Limited",
        "icon": "🖱️",
        "badge": "Ultra Light",
        "color": "orange",
        "description": "Lightweight mouse with precise movement for gaming, studying, and work.",
    },
    {
        "id": 5,
        "name": "FitPulse Smart Watch",
        "category": "Wearables",
        "price": 210,
        "old_price": 280,
        "rating": 4.5,
        "stock": 11,
        "tag": "Smart Pick",
        "icon": "⌚",
        "badge": "Alert Ready",
        "color": "pink",
        "description": "Track fitness, calls, notifications, and daily activity from your wrist.",
    },
    {
        "id": 6,
        "name": "DeskPort Docking Station",
        "category": "Office",
        "price": 130,
        "old_price": 190,
        "rating": 4.7,
        "stock": 19,
        "tag": "Save 32%",
        "icon": "🔌",
        "badge": "8-in-1 Hub",
        "color": "blue",
        "description": "Connect screens, laptop, keyboard, mouse, and accessories in one clean setup.",
    },
    {
        "id": 7,
        "name": "PixelView 4K Monitor",
        "category": "Office",
        "price": 390,
        "old_price": 520,
        "rating": 4.9,
        "stock": 7,
        "tag": "Flash Sale",
        "icon": "🖥️",
        "badge": "4K Display",
        "color": "cyan",
        "description": "A crisp 4K screen for movies, gaming, productivity, and clean desk setups.",
    },
    {
        "id": 8,
        "name": "GuardCam Security Kit",
        "category": "Smart Home",
        "price": 260,
        "old_price": 340,
        "rating": 4.4,
        "stock": 13,
        "tag": "Trending",
        "icon": "📷",
        "badge": "Smart Alerts",
        "color": "violet",
        "description": "A smart home camera kit with night vision, mobile alerts, and easy setup.",
    },
]


def list_products(category: str | None = None, search: str | None = None) -> list[dict[str, Any]]:
    """Return products with optional category and search filtering."""
    results = PRODUCTS

    if category:
        wanted = category.strip().lower()
        results = [item for item in results if item["category"].lower() == wanted]

    if search:
        term = search.strip().lower()
        results = [
            item for item in results
            if term in item["name"].lower()
            or term in item["category"].lower()
            or term in item["description"].lower()
        ]

    return results


def get_product(product_id: int) -> dict[str, Any] | None:
    """Return one product by id."""
    return next((item for item in PRODUCTS if item["id"] == product_id), None)


def catalog_summary() -> dict[str, Any]:
    """Small business-friendly summary for dashboards and docs."""
    categories = sorted({item["category"] for item in PRODUCTS})
    total_stock = sum(item["stock"] for item in PRODUCTS)
    avg_rating = round(sum(item["rating"] for item in PRODUCTS) / len(PRODUCTS), 2)
    return {
        "products_count": len(PRODUCTS),
        "categories": categories,
        "total_stock": total_stock,
        "average_rating": avg_rating,
    }
