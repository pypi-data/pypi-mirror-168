import asyncio
from functools import wraps

from . import key
from .cache import Cache


class alru_cache:
    def __init__(self, maxsize: int = 128, make_key=None):
        self.cache = Cache(maxsize)
        if make_key is None:
            self.make_key = key.make_key
        else:
            self.make_key = make_key

    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            key = self.make_key(*args, **kwargs)

            if key not in self.cache:
                lock = asyncio.Lock()
                self.cache[key] = [lock, None]

                async with lock:
                    val = await f(*args, **kwargs)
                    self.cache[key] = [lock, val]

                    return val
            else:
                lock, val = self.cache[key]
                async with lock:
                    val = self.cache[key][1]
                    self.cache.move_to_end(key)

                    return val

        return wrapper
