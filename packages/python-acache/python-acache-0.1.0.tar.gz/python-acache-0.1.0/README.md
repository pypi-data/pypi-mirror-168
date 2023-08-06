# acache: async cache for python

Those are two implementations of async caches for python.
A implementation of `lru_cache` and an implementation of a cache based on time.

## Install

```
# from pip
pip3 install --user python-acache

# from github
pip3 install git+https://github.com/Dimfred/acache.git
```

## Usage

```python
from acache import alru_cache, atime_cache

# basic lru
@alru_cache(maxsize=2)
async def i_am_cached(foo):
    return foo

# use with custom key function
@alru_cache(maxsize=2, make_key=lambda x: type(x))
async def i_cache_based_on_the_input_type(foo)
    return foo

class A:
    pass

res1 = await i_cache_based_on_the_input_type(A())
res2 = await i_cache_based_on_the_input_type(A())
assert id(res1) == id(res2) # TRUE

# time cache
@atime_cache(seconds=1)
async def cached_for_1_s(bar):
    return bar


res1 = await cached_for_1_s(1)
res2 = await cached_for_1_s(2)

assert res1 == res2

# wait 1 second

res3 = await cached_for_1_s(3)
assert res1 != res3

# key function also applies to the atime_cache
```

## Synopsis


```python
def alru_cache(maxsize=32, make_key=None):
    ...

def atime_cache(
    weeks=0,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    milliseconds=0,
    microseconds=0,
    timedelta=None,
    make_key=None,
):
    ...
```
