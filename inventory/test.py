"""
==========================================================
 Stackpay Inventory Management - Test Suite
----------------------------------------------------------
 This file contains the test suite for the Inventory
 Management System of the Stackpay project.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from db import redis, ProductData

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """
    Setup and teardown for the test suite. This ensures that
    the Redis database is cleaned before and after the tests.
    """
    redis.flushdb()
    yield
    redis.flushdb()

def test_create_product():
    """
    Test the product creation endpoint.
    """
    response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 100, "quantity": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 100
    assert data["quantity"] == 10

def test_get_all_products():
    """
    Test the endpoint for fetching all products.
    """
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test Product"

def test_get_single_product():
    """
    Test the endpoint for fetching a single product by primary key.
    """
    all_products = client.get("/products").json()
    product_id = all_products[0]["id"]
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"

def test_delete_product():
    """
    Test the endpoint for deleting a product by primary key.
    """
    all_products = client.get("/products").json()
    product_id = all_products[0]["id"]
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == 1

    # Confirm deletion
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
