import redis
from settings import NAME_REDIS_PROXY


def print_proxies():
    r = redis.Redis(host='localhost', port=6379, db=0)
    items = r.lrange(NAME_REDIS_PROXY, 0, -1)
    print(items)
    for item in items:
        print('REDIS_PROXY-', item.decode())


if __name__ == '__main__':
    print_proxies()
