"""Exercise 1: decorator that prints the parameters and the return value."""

from functools import wraps


def log_call(func):
    """Print the parameters a function was called with and what it returned."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling '{func.__name__}'")
        print(f"  Positional arguments: {args}")
        print(f"  Keyword arguments:    {kwargs}")
        result = func(*args, **kwargs)
        print(f"  Return value: {result}")
        return result
    return wrapper


if __name__ == "__main__":
    @log_call
    def add(a, b):
        return a + b

    add(3, b=5)
