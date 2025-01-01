"""
==========================================================
 Stackpay Payments Management
----------------------------------------------------------
 This file contains the main entry point for the Payments
 Management System of the Stackpay project, including
 order-related API endpoints.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import requests
from config import *
from db import *
from fastapi import BackgroundTasks, HTTPException
from starlette.requests import Request

db = get_db_connection()


@app.get("/orders/")
def get_all_orders():
    """
    Fetch all order keys from the database.

    Returns:
        List[str]: A list of all order primary keys.
    """
    return OrderData.all_pks()


@app.get('/orders/{pk}')
def get_single_order(pk: str):
    """
    Fetch a single order by its primary key.

    Args:
        pk (str): The order primary key.

    Returns:
        Order: The order details.
    """
    try:
        return OrderData.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post('/orders/')
async def create_new_order(order_request: OrderDataRequest, background_tasks: BackgroundTasks):
    """
    Create a new order in the database.

    Args:
        order_request (OrderRequest): The order data.
        background_tasks (BackgroundTasks): Background tasks for processing.

    Returns:
        Order: The created order details.
    """
    try:
        print(order_request)
        req = requests.get(
            f'http://localhost:8000/products/{order_request.product_id}')
        req.raise_for_status()
        product = req.json()

        order = OrderData(
            product_id=order_request.product_id,
            price=product['price'],
            fee=0.2 * product['price'],
            total=1.2 * product['price'],
            quantity=order_request.quantity,
            status='pending'
        )
        order.save()
        background_tasks.add_task(process_order_completion, order)
        return order

    except requests.exceptions.RequestException as e:
        logger.error(f"Product fetch error: {e}")
        raise HTTPException(status_code=404, detail="Product not found")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def process_order_completion(order: OrderData):
    """
    Process the completion of an order after a delay.

    Args:
        order (Order): The order to be processed.
    """
    import time
    time.sleep(5)
    order.status = 'completed'
    order.save()
    db.xadd('order_completed', order.dict(), '*')
