from typing import Any, Callable
from betterlist import BetterList


class BetterDict(dict):
    """
    This Dict Class allows you todo javascript styled continuous operation.
    ex.
    x = BetterDict({'a':1,'b':2,'c':3,'d':4})
    y = x.filter_key(func1).filter_value(func2).map_key(func3).foreach_value(print)
    """

    @property
    def keys_list(self):
        return BetterList(self.keys())

    @property
    def values_list(self):
        return BetterList(self.values())

    @property
    def length(self):
        return len(self)

    def sort(self, func: Callable = lambda x: x[1]):
        return BetterDict(sorted(self.items(), key=func))

    def max(self, n_largest: int = 1, func: Callable = lambda x: x[1]):
        """
        BetterDict({"a":1,"b":2,"c":3,"d":4})
        Return key list that looks like this
        ['d', 'c']
        """
        return BetterList(self.sort(func).keys_list[-n_largest:][::-1])

    def min(self, n_smallest: int = 1, func: Callable = lambda x: x[1]):
        """
        BetterDict({"a":1,"b":2,"c":3,"d":4})
        Return key list that looks like this
        ['a', 'b']
        """
        return BetterList(self.sort(func).keys_list[:n_smallest])

    def foreach(self, func: Callable):
        for key, value in self.items():
            func(key, value)

    def foreach_key(self, func: Callable):
        for key, _ in self.items():
            func(key)

    def foreach_value(self, func: Callable):
        for _, value in self.items():
            func(value)

    def filter_key(self, func: Callable):
        return BetterDict({key: value for key, value in self.items() if func(key)})

    def filter_out_key(self, func: Callable):
        return BetterDict({key: value for key, value in self.items() if not func(key)})

    def filter_value(self, func: Callable):
        return BetterDict({key: value for key, value in self.items() if func(value)})

    def filter_out_value(self, func: Callable):
        return BetterDict(
            {key: value for key, value in self.items() if not func(value)}
        )

    def map(self, func: Callable):
        return BetterDict({key: func(key, value) for key, value in self.items()})

    def map_key(self, func: Callable):
        return BetterDict({func(key): value for key, value in self.items()})

    def map_value(self, func: Callable):
        return BetterDict({key: func(value) for key, value in self.items()})

    def reduce_key(self, func: Callable):
        return self.keys_list.reduce(func)

    def reduce_value(self, func: Callable):
        return self.values_list.reduce(func)
