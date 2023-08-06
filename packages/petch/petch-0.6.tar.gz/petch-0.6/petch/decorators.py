import cProfile
import pstats
from time import time
from rich.console import Console
from rich.traceback import install
from rich.theme import Theme

console = Console(
    theme=Theme(
        {
            "info": "white",
            "warning": "yellow",
            "danger": "bold red",
            "debug": "green",
        }
    )
)
install()


def measure_time(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


def perform_profiling(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            result = func(*args, **kwargs)
            stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename="profiling.prof")
        return result

    return wrapper


def debug(func):
    def wrap(*args, **kwargs):
        console.log(func.__name__, log_locals=True, style="debug")
        results = func(*args, **kwargs)
        return results

    return wrap
