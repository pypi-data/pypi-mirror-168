from functools import reduce
from typing import Any


def compose(*func):
    def compose_function(f, g):
        return lambda *args: g(f(*args))

    return reduce(compose_function, func)


class Result:
    def __init__(self, value: Any) -> None:
        self.__value = value
        self.is_ok: bool

    def unwrap(self):
        if not self.is_ok:
            raise ValueError(self.__value)
        return self.__value

    def unwrap_or_default(self, default: Any):
        if not self.is_ok:
            raise default
        return self.__value

    def expect(self, reason: str):
        """
        Describe the reason you expect the Result should be Ok.
        """
        if not self.is_ok:
            raise ValueError(reason)
        return self.__value


class Ok(Result):
    def __init__(self, value: Any) -> None:
        super().__init__(value)
        self.is_ok = True


class Err(Result):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.is_ok = False
