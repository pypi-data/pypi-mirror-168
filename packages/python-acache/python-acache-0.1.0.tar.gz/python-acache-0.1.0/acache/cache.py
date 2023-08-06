from collections import OrderedDict


class Cache(OrderedDict):
    def __init__(self, maxsize: int, *args, **kwargs):
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        if self.maxsize and len(self) > self.maxsize:
            del self[next(iter(self))]
