"""
==========================================================
 Stackpay Database Configuration
----------------------------------------------------------
 This file contains the database configuration settings for
 the Stackpay project, including Redis connection and data
 models.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import logging
import time
from pydantic import BaseModel
from redis_om import HashModel, NotFoundError, get_redis_connection

# Configure Redis connection
def get_db_connection():
    return get_redis_connection(
        host='localhost', port=6379, password=None, decode_responses=True
    )

redis_connection = get_db_connection()

class OrderDataRequest(BaseModel):
    """
    Pydantic model for validating order request data.

    Attributes:
        product_id (str): The ID of the product being ordered.
        quantity (int): The quantity of the product being ordered.
    """
    product_id: str
    quantity: int

class OrderData(HashModel):
    """
    Redis-OM model for storing order data.

    Attributes:
        product_id (str): The ID of the product being ordered.
        price (float): The price of the product.
        fee (float): The fee associated with the order.
        total (float): The total cost of the order.
        quantity (int): The quantity of the product being ordered.
        status (str): The status of the order (e.g., pending, complete, refunded).
    """
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, complete, refunded

    class Meta:
        database = redis_connection
