import time

from main import Product, redis

from inventory.main import redis

key = 'order_completed'
group = 'inventory_group'

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
                product = Product.get(obj['product_id'])
                if product:
                    product.quantity = product.quantity + int(obj["quantity"])
                    product.save()
                else:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
