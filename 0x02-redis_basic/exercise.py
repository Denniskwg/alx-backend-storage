#!/usr/bin/env python3
"""exercise
"""
import redis
import uuid
from typing import Any, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """counts the number of tomes fn is called"""
    @wraps(method)
    def increment(self, *args, **kwargs) -> Any:
        """increments the value in key method.__qualname__"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        method(self, *args, **kwargs)
    return increment


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular
    function
    """
    @wraps(method)
    def history(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs
        and output
        """
        inputs = "{}:inputs".format(method.__qualname__)
        outputs = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, output)
        return output
    return history


class Cache:
    """Represents an object for storing data in a Redis data storage
    """
    def __init__(self) -> None:
        """initializes a redis object"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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
