"""
==========================================================
 Stackpay Inventory Management
----------------------------------------------------------
 This file contains the main entry point for the Inventory
 Management System of the Stackpay project, including
 product-related API endpoints.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

from config import *
from db import *
from fastapi import HTTPException

db = get_db_connection()


@app.get('/products')
def get_all_products():
    """
    Fetch all product keys from the database.

    Returns:
        List[dict]: A list of all product details.
    """
    logger.info("Fetching all product keys")
    try:
        return [format_product(pk) for pk in ProductData.all_pks()]
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Error fetching products")


def format_product(pk: str):
    """
    Format the product information for output.

    Args:
        pk (str): The product primary key.

    Returns:
        dict: The formatted product details.
    """
    product = ProductData.get(pk=pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.get('/products/{pk}')
def get_single_product(pk: str):
    """
    Fetch a single product by its primary key.

    Args:
        pk (str): The product primary key.

    Returns:
        dict: The product details.
    """
    return ProductData.get(pk)


@app.delete('/products/{pk}')
def delete_product(pk: str):
    """
    Delete a product by its primary key.

    Args:
        pk (str): The product primary key.

    Returns:
        int: The number of deleted products.
    """
    return ProductData.delete(pk)


@app.post('/products/')
async def create_product(product_request: ProductDataRequest):
    """
    Create a new product in the database.

    Args:
        product_request (ProductRequest): The product data.

    Returns:
        dict: The created product details.
    """
    try:
        logger.info(f"Creating product: {product_request}")
        product = ProductData(**product_request.dict())
        return product.save()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
