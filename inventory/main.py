from fastapi import FastAPI
from redis_om import HashModel, get_redis_connection

app = FastAPI()

redis = get_redis_connection(
    host='localhost', port=6379, password=None, decode_responses=True)


class Product(HashModel):
    name: str
    price: int
    quantity: int

    class Meta:
        database = redis

    @app.get('/products')
    def all():
        return []
