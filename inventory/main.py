import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel, get_redis_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Redis connection
redis = get_redis_connection(
    host='localhost', port=6379, password=None, decode_responses=True)

# Pydantic model for request validation


class ProductRequest(BaseModel):
    name: str
    price: int
    quantity: int

# Redis-OM model for storage


class Product(HashModel):
    name: str
    price: int
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all():
    logger.info("Fetching all product keys")
    try:
        return [format(pk) for pk in Product.all_pks()]
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Error fetching products")


def format(pk: str):
    product = Product.get(pk=pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.get('/products/{pk}')
def single(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)


@app.post('/products/')
async def create(product_request: ProductRequest):
    try:
        logger.info(f"Creating product: {product_request}")
        product = Product(**product_request.dict())
        return product.save()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
