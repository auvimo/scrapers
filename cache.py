import redis

class Cache:
    """Simple caching class"""

    def __init__(self, host='localhost', port=6379, expire_time=300):
        """Create the Redis Connection object and set an expiration date for cache in seconds"""
        self.redis_client = redis.StrictRedis(host=host, port=port, decode_responses=True)
        self.expire_time = expire_time

    def get(self, key):
        """Get a specific object value using key"""
        cached_data = self.redis_client.get(key)
        if cached_data:
            return cached_data
        return None

    def set(self, key, data):
        """Set a specific object value to a key"""
        self.redis_client.setex(key, self.expire_time, data)