import json

from rediscluster import RedisCluster

from cache.abstract import Cache


class RedisCacheClient(Cache):
    """
    Cache client for Redis.

    """

    def __init__(self, startup_nodes, password=None):
        """
        Initializes the Redis cache client.

        Args:
            startup_nodes (list): List of nodes to connect to.
            password (str, optional): Password for the Redis cluster.

        """
        self.client = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True,
            password=password,
            ssl=True,
            skip_full_coverage_check=True,
        )

    def set(self, key, value, ttl=None):
        """
        Save or overwrite a value in the cache with an optional TTL.

        Args:
            key (str): The cache key under which the value is stored.
            value (str or dict): The value to be stored.
            ttl (int, optional): The time-to-live (TTL) in seconds. If provided,
                the item will expire and be deleted after this duration.

        """
        value_to_store = json.dumps(value) if isinstance(value, dict) else value

        if ttl:
            self.client.setex(key, ttl, value_to_store)
        else:
            self.client.set(key, value_to_store)

    def get(self, key):
        """
        Retrieve a value from the cache.

        Args:
            key (str): The cache key.

        Returns:
            The retrieved value, or None if the key does not exist.
            If the value was stored as a JSON string, it will be returned as a dict.

        """
        value = self.client.get(key)

        try:
            return json.loads(value) if value else None
        except json.JSONDecodeError:
            return value
