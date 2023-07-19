#!/usr/bin/env python3
"""exercise
"""
import redis
import uuid
from typing import Any, Callable, Union


class Cache:
    """Represents an object for storing data in a Redis data storage
    """
    def __init__(self) -> None:
        """initializes a redis object"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in a Redis data storage and returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """take a key string argument and an optional Callable argument
        named fn. This callable will be used to convert the data back
        to the desired format.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            value = fn(value)
            return value
        elif fn is None:
            return value
        else:
            fn_dict = {
                    'int': 'get_int',
                    'str': 'get_str'
            }

            return eval(self.fn_dict.get(fn)(value))

    def get_str(self, value: str) -> str:
        """converts value back to string from redis store"""
        return value.decode('utf-8')

    def get_int(self, value: int) -> int:
        """converts value back to int from redis store"""
        return int(value)
