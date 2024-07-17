#!/usr/bin/env python3
"""Redis class"""
import redis
import uuid
from typing import Union, Optional, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method"""
    key = method.__qualname__
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class that uses Redis to store data and count method calls."""
    def __init__(self):
        """Initialize the Cache class and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache with a randomly generated key.

        Args:
            data: The data to be stored, can str, bytes, int, or float.

        Returns:
            The key under which the data is stored.
        """
        random = str(uuid.uuid4())
        self._redis.set(random, data)
        return random

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Retrieve data from the cache by key and optionally apply
           a transformation function.

        Args:
            key: The key for the data to retrieve.
            fn: Optional; A function to apply to the retrieved data.

        Returns:
            The retrieved data, optionally transformed by fn,
            or None if key is not found.
        """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve data as a string from the cache by key"""
        return self._redis.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        """Retrieve data as an integer from the cache by key"""
        return int(self._redis.get(key).decode('utf-8'))
