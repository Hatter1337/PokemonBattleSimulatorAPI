from abc import ABC, abstractmethod


class Cache(ABC):

    @abstractmethod
    def set(self, key, value, ttl=None):
        """
        Save or overwrite a value in the cache with an optional TTL.

        Args:
            key (str): The cache key under which the value is stored.
            value (str or dict): The value to be stored.
            ttl (int, optional): The time-to-live (TTL) in seconds. If provided,
                the item will expire and be deleted after this duration.

        """

    @abstractmethod
    def get(self, key):
        """
        Retrieve a value from the cache.

        Args:
            key (str): The cache key.

        Returns:
            The retrieved value, or None if the key does not exist.
            If the value was stored as a JSON string, it will be returned as a dict.

        """
