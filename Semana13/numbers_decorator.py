"""Exercise 2: decorator that validates that all parameters are numbers."""

from functools import wraps


def numbers_only(func):
    """Check that every argument is an int or float; otherwise raise TypeError."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        values = list(args) + list(kwargs.values())
        for value in values:
            # In Python, bool is a subclass of int, so it is excluded explicitly
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(
                    f"'{func.__name__}' only accepts numbers, "
                    f"but received {value!r} (type {type(value).__name__})."
                )
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    @numbers_only
    def multiply(a, b):
        return a * b

    print(multiply(4, 2.5))
    try:
        multiply(4, "2")
    except TypeError as e:
        print("Caught error:", e)
