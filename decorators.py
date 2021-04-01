import functools
import redis as r
import json
import datetime


def count_function_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        return func(*args, **kwargs)

    wrapper.count = 0

    return wrapper


def cache_function(expiry_time):
    redis_client = r.Redis(host='localhost', port=6379, db=0)
    expiry_time = datetime.timedelta(seconds=expiry_time * 60)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = ""
            key = f"{func.__name__}."
            arguments = hash(args)
            k_arguments = hash(frozenset(kwargs.items()))
            key += str(arguments) + str(k_arguments)
            # print(key)

            if redis_client.get(key) is None:
                result = func(*args, **kwargs)

                redis_client.set(key, result)
                redis_client.expire(key, expiry_time)
            else:
                print("Getting result from cache!")
                result = json.loads(redis_client.get(key))
            return result
        return wrapper
    return decorator


