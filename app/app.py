from fastapi import FastAPI
import time

app = FastAPI(title="Online Store App")


products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Keyboard", "price": 80},
    {"id": 4, "name": "Mouse", "price": 40},
]


@app.get("/")
def home():
    return {
        "message": "Welcome to the Online Store",
        "endpoints": ["/products", "/cart", "/checkout", "/health", "/stress"]
    }


@app.get("/products")
def get_products():
    return {
        "status": "success",
        "products": products
    }


@app.get("/cart")
def get_cart():
    return {
        "status": "success",
        "cart": [
            {"product": "Laptop", "quantity": 1},
            {"product": "Mouse", "quantity": 2}
        ]
    }


@app.get("/checkout")
def checkout():
    return {
        "status": "success",
        "message": "Order placed successfully"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "online-store"
    }


@app.get("/stress")
def stress():
    """
    This endpoint creates CPU load.
    We use it only for HPA demo.
    """
    total = 0
    for i in range(8_000_000):
        total += i * i

    return {
        "status": "stress completed",
        "result": total
    }
