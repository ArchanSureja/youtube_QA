#  Uses semantic similarity to find the best matching chunks.
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CACHE_EXPIRATION_SECONDS = 3600  



def get_cached_answer(key):
    """
    Retrieves cached answer from Redis using the given key.
    """
    return redis_client.get(key)


def set_cached_answer(key, value, expiration= CACHE_EXPIRATION_SECONDS):
    """
    Stores an answer in Redis under the given key with optional expiration.
    """
    redis_client.setex(key, expiration, value)
