# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['acache']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-acache',
    'version': '0.1.0',
    'description': 'Async cache',
    'long_description': '# acache: async cache for python\n\nThose are two implementations of async caches for python.\nA implementation of `lru_cache` and an implementation of a cache based on time.\n\n## Install\n\n```\n# from pip\npip3 install --user python-acache\n\n# from github\npip3 install git+https://github.com/Dimfred/acache.git\n```\n\n## Usage\n\n```python\nfrom acache import alru_cache, atime_cache\n\n# basic lru\n@alru_cache(maxsize=2)\nasync def i_am_cached(foo):\n    return foo\n\n# use with custom key function\n@alru_cache(maxsize=2, make_key=lambda x: type(x))\nasync def i_cache_based_on_the_input_type(foo)\n    return foo\n\nclass A:\n    pass\n\nres1 = await i_cache_based_on_the_input_type(A())\nres2 = await i_cache_based_on_the_input_type(A())\nassert id(res1) == id(res2) # TRUE\n\n# time cache\n@atime_cache(seconds=1)\nasync def cached_for_1_s(bar):\n    return bar\n\n\nres1 = await cached_for_1_s(1)\nres2 = await cached_for_1_s(2)\n\nassert res1 == res2\n\n# wait 1 second\n\nres3 = await cached_for_1_s(3)\nassert res1 != res3\n\n# key function also applies to the atime_cache\n```\n\n## Synopsis\n\n\n```python\ndef alru_cache(maxsize=32, make_key=None):\n    ...\n\ndef atime_cache(\n    weeks=0,\n    days=0,\n    hours=0,\n    minutes=0,\n    seconds=0,\n    milliseconds=0,\n    microseconds=0,\n    timedelta=None,\n    make_key=None,\n):\n    ...\n```\n',
    'author': 'Dmitrij Vinokour',
    'author_email': 'dimfred.1337@web.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dimfred/acache',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
