import logging
import time

import requests
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel, NotFoundError, get_redis_connection
from starlette.requests import Request

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
    host='localhost', port=6379, password=None, decode_responses=True
)

# Pydantic model for request validation


class OrderRequest(BaseModel):
    product_id: str
    quantity: int

# Redis-OM model for storage


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, complete, refunded

    class Meta:
        database = redis


@app.get("/orders/")
def get_all():
    return Order.all_pks()


@app.get('/orders/{pk}')
def get_order(pk: str):
    try:
        return Order.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post('/orders')
async def create_order(request: OrderRequest, background_tasks: BackgroundTasks):
    try:
        req = requests.get(
            f'http://localhost:8000/products/{request.product_id}')
        req.raise_for_status()
        product = req.json()

        order = Order(
            product_id=request.product_id,
            price=product['price'],
            fee=0.2 * product['price'],
            total=1.2 * product['price'],
            quantity=request.quantity,
            status='pending'
        )
        order.save()
        background_tasks.add_task(order_created, order)
        return order

    except requests.exceptions.RequestException as e:
        logger.error(f"Product fetch error: {e}")
        raise HTTPException(status_code=404, detail="Product not found")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def order_created(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
