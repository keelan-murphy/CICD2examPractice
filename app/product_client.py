import os
import httpx

# Default: same Codespace, port 8001. Docker later can change this env var.
PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL", "http://127.0.0.1:8001"
)


def fetch_product(product_id: int) -> dict:
    response = httpx.get(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}",
        timeout=3.0,
    )
    response.raise_for_status()  # 4xx/5xx → raise HTTPStatusError
    return response.json()


def get_product_fetcher():
    # FastAPI Depends(...) will call this and get fetch_product
    return fetch_product