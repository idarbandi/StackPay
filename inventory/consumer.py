"""
==========================================================
 Stackpay Consumer
----------------------------------------------------------
 This file contains the consumer logic for the Stackpay
 project, which listens for completed orders and updates
 the inventory accordingly.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import time

from db import ProductData, redis_connection

redis = redis_connection

# Stream key and consumer group
stream_key = 'order_completed'
consumer_group = 'inventory_group'

# Create the consumer group if it doesn't exist
try:
    redis.xgroup_create(stream_key, consumer_group)
except Exception as e:
    print('Group Already Exists')

# Function to process completed orders


def process_completed_orders():
    while True:
        try:
            results = redis.xreadgroup(consumer_group, stream_key, {
                                       stream_key: '>'}, None)
            if results:
                for result in results:
                    obj = result[1][0][1]
                    product = Product.get(obj['product_id'])
                    if product:
                        product.quantity += int(obj["quantity"])
                        product.save()
                    else:
                        redis.xadd('refund_order', obj, '*')

        except Exception as e:
            print(f"Error processing order: {str(e)}")
        time.sleep(1)


if __name__ == '__main__':
    process_completed_orders()
