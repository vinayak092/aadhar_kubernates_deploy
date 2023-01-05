import redis
REDIS_HOST = "my-release-redis-master.default.svc.cluster.local"
REDIS_PORT = 6379
REDIS_DB = 10
REDIS_PASSWORD = "9CcVSjiGPD"
REDIS_DB_CONV = "0"
REDIS_DB_1 = 5
red_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_1, password=REDIS_PASSWORD, decode_responses=True,charset="utf-8")
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True,charset="utf-8")
def store_into_redis(customer_data):
    print("")
    for row in customer_data:
        red_customers.hmset(row['phone_number'],row)
        print("storeed")
    return True
def fetch_data(phone_number):
    data=red_customers.hgetall(phone_number)
    return data

def detect_camapin(sender):
    data=red.hget("cz","5")
    return data


