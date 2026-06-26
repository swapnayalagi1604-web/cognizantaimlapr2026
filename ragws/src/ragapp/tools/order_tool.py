# tools.py
from dotenv import load_dotenv
import requests
from langchain.tools import tool
import os
env_path = os.path.join(os.path.dirname(__file__),'..','.env')
load_dotenv(env_path)
BASE_URL = os.getenv("order_api_url")


@tool
def search_products(title: str) -> str:
    """Search products by title."""
    url = f"{BASE_URL}/products/?title={title}"
    return requests.get(url).text


@tool
def get_product(product_id: int) -> str:
    """Get product details by product id."""
    url = f"{BASE_URL}/products/{product_id}"
    return requests.get(url).text


@tool
def list_categories() -> str:
    """List all product categories."""
    url = f"{BASE_URL}/categories"
    return requests.get(url).text


@tool
def create_product(title: str, price: int, description: str, categoryId: int, image_url: str) -> str:
    """Create a new product in Platzi Fake Store API."""
    payload = {
        "title": title,
        "price": price,
        "description": description,
        "categoryId": categoryId,
        "images": [image_url]
    }
    return requests.post(f"{BASE_URL}/products/", json=payload).text