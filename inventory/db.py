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

from pydantic import BaseModel
from redis_om import HashModel, get_redis_connection


# Configure Redis connection
def get_db_connection():
    return get_redis_connection(
        host='localhost', port=6379, password=None, decode_responses=True
    )


redis_connection = get_db_connection()


class ProductDataRequest(BaseModel):
    """
    Pydantic model for validating product request data.

    Attributes:
        name (str): The name of the product.
        price (int): The price of the product.
        quantity (int): The quantity of the product.
    """
    name: str
    price: int
    quantity: int


class ProductData(HashModel):
    """
    Redis-OM model for storing product data.

    Attributes:
        name (str): The name of the product.
        price (int): The price of the product.
        quantity (int): The quantity of the product.
    """
    name: str
    price: int
    quantity: int

    class Meta:
        database = redis_connection
