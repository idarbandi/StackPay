import logging
import time

import requests
from fastapi import FastAPI, HTTPException
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel, get_redis_connection
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
    host='localhost', port=6379, password=None, decode_responses=True)

# Pydantic model for request validation


class Order(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, complete, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_tasks=BackgroundTasks):
    body = await request.json()

    req = request.get('http://localhost:8000/products/%s' % body['id'])
    if not req:
        return {
            '404 Not Found'
        }
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_created, order)
    return order


def order_created(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
