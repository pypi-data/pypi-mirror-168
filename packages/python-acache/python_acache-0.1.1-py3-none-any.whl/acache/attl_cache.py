import asyncio
import datetime as dt
from functools import wraps

from . import key
from .cache import Cache


class attl_cache:
    def __init__(
        self,
        weeks=0,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        milliseconds=0,
        microseconds=0,
        maxsize=128,
        make_key=None,
    ):
        self.cache = Cache(maxsize)
        self.ttl = dt.timedelta(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
        )
        if make_key is None:
            self.make_key = key.make_key
        else:
            self.make_key = make_key

    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            key = self.make_key(*args, **kwargs)

            if key not in self.cache:
                self.cache[key] = (
                    asyncio.Lock(),
                    dt.datetime(year=1970, month=1, day=1),
                    None,
                )

            lock, expiration_time, val = self.cache[key]
            async with lock:
                if dt.datetime.now() > expiration_time:
                    val = await f(*args, **kwargs)
                    self.cache[key] = lock, dt.datetime.now() + self.ttl, val

            return val

        return wrapper
