"""
==========================================================
 Stackpay Payment Consumer
----------------------------------------------------------
 This file contains the consumer logic for the Stackpay
 project, which listens for refund orders and updates the
 order status accordingly.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import time

from db import OrderData, get_db_connection

redis = get_db_connection()

# Stream key and consumer group
stream_key = 'refund_order'
consumer_group = 'payment_group'

# Create the consumer group if it doesn't exist
try:
    redis.xgroup_create(stream_key, consumer_group)
except Exception as e:
    print('Group Already Exists')


def process_refund_orders():
    """
    Process refund orders by listening to the Redis stream
    and updating the order status.

    This function runs in an infinite loop, continually
    checking for new messages in the Redis stream.
    """
    while True:
        try:
            results = redis.xreadgroup(
                consumer_group, stream_key, {stream_key: '>'}, None)
            if results:
                for result in results:
                    obj = result[1][0][1]
                    order = OrderData.get(obj['product_id'])
                    if order:
                        order.status = 'refunded'
                        order.save()
                    else:
                        redis.xadd('refund_order', obj, '*')

        except Exception as e:
            print(f"Error processing refund order: {str(e)}")
        time.sleep(1)


if __name__ == '__main__':
    process_refund_orders()
