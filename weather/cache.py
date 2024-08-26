from redis import Redis

from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

class Redis:
    def __init__(self):
        self._redis = None
        
    def init_redis(self, is_testing=False):
        if is_testing:
            from fakeredis import FakeStrictRedis
            self._redis = FakeStrictRedis(decode_responses=True)
        else:
            self._redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
            
            
    def __getattr__(self, name):
        return getattr(self._redis, name)

redis = Redis()