"""
==========================================================
 Stackpay Payments Management - Test Suite
----------------------------------------------------------
 This file contains the test suite for the Payments
 Management System of the Stackpay project.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import pytest
from db import OrderData, redis_connection
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """
    Setup and teardown for the test suite. This ensures that
    the Redis database is cleaned before and after the tests.
    """
    redis_connection.flushdb()
    yield
    redis_connection.flushdb()


def test_create_order():
    """
    Test the order creation endpoint.
    """
    response = client.post(
        "/orders",
        json={"product_id": "test_product", "quantity": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "test_product"
    assert data["quantity"] == 2
    assert data["status"] == "pending"


def test_get_all_orders():
    """
    Test the endpoint for fetching all orders.
    """
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0] == "1"  # Assuming the first order's pk is "1"


def test_get_single_order():
    """
    Test the endpoint for fetching a single order by primary key.
    """
    all_orders = client.get("/orders/").json()
    order_id = all_orders[0]
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "test_product"
    assert data["quantity"] == 2
    assert data["status"] == "pending"


def test_order_processing():
    """
    Test the background task for processing an order.
    """
    all_orders = client.get("/orders/").json()
    order_id = all_orders[0]

    # Simulate the background task running and completing the order
    order = OrderData.get(order_id)
    order.status = 'completed'
    order.save()

    # Fetch the order again to verify the status
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"


def test_order_not_found():
    """
    Test fetching an order that does not exist.
    """
    response = client.get("/orders/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
