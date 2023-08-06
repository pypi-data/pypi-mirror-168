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

## Alternatives

`https://pypi.org/project/async-cache/`

The difference in my package is that if you call a function with the same args, from different threads the second one will not return a value until the first one is completed, s.t. the value gets definitely cached.
Additionally, I allow overwriting the key generation function, so you can pick your own.
Also my naming is different, and maybe more pythonic (whatever).

## Usage

```python
from acache import alru_cache, attl_cache

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
@attl_cache(seconds=1)
async def cached_for_1_s(bar):
    return bar


res1 = await cached_for_1_s(1)
res2 = await cached_for_1_s(2)

assert res1 == res2

# wait 1 second

res3 = await cached_for_1_s(3)
assert res1 != res3

# key function also applies to the attl_cache
```

## Synopsis


```python
def alru_cache(self, maxsize: int = 128, make_key=None):
    ...

def attl_cache(
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
    ...
```
