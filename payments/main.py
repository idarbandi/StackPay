import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel, get_redis_connection
from starlette.requests import request

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

    @app.post('/orders')
    async def create(requests: Request):
        body = await request.json()

        req = request.get('http://localhost:8000/products/%s' % body['id'])
        
        return req.json()
