import time

from main import Product, redis

key = 'order_completed'
group = 'inventory_group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group Already Exists')


while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        print(results)
    except Exception as e:
        return {
            'message': str(e)
        }
    time.sleep(1)
