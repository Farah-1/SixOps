"""OpenAPI metadata and backend constants."""

APP_TITLE = "GadgetNest Backend API"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = """
Professional backend for the GadgetNest online electronics store.

The public frontend is customer-facing only. AIOps, stress demo, health checks,
and replica optimizer logic are kept behind backend API groups.
"""

TAGS_METADATA = [
    {
        "name": "Store",
        "description": "Customer store APIs: products, cart sample, and checkout simulation.",
    },
    {
        "name": "Backend Demo",
        "description": "Backend-only stress endpoints used for Kubernetes scaling demos.",
    },
    {
        "name": "AIOps",
        "description": "AIOps status and backend module overview.",
    },
    {
        "name": "Optimizer",
        "description": "Cost-aware replica recommendation APIs.",
    },
    {
        "name": "System",
        "description": "Health and backend overview endpoints.",
    },
]
