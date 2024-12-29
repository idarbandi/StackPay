import time

from main import Order, redis

key = 'refund_order'
group = 'payment_group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group Already Exists')


while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['product_id'])
                if order:
                    order.status = 'refunded'
                    order.save()
                else:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
