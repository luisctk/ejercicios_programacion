"""Exercise 3: User class with date_of_birth and an age property,
plus a decorator that requires the user to be an adult."""

from datetime import date
from functools import wraps


class User:
    def __init__(self, name, date_of_birth):
        self.name = name
        # date_of_birth is a date object, e.g. date(2005, 3, 14)
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        """Age calculated from the date of birth."""
        today = date.today()
        age = today.year - self.date_of_birth.year
        # If the birthday hasn't happened yet this year, subtract one
        birthday = (self.date_of_birth.month, self.date_of_birth.day)
        if (today.month, today.day) < birthday:
            age -= 1
        return age


def require_adult(func):
    """Find the User among the arguments and require them to be 18 or older."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = None
        for value in list(args) + list(kwargs.values()):
            if isinstance(value, User):
                user = value
                break
        if user is None:
            raise TypeError(
                f"'{func.__name__}' expected to receive a User as an argument."
            )
        if user.age < 18:
            raise PermissionError(
                f"Access denied: {user.name} is {user.age} years old "
                "and must be an adult (18+)."
            )
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    alice = User("Alice", date(1995, 11, 2))
    bob = User("Bob", date(2012, 5, 20))
    print(f"{alice.name} is {alice.age} years old.")
    print(f"{bob.name} is {bob.age} years old.")

    @require_adult
    def view_content(user):
        return f"{user.name} can view the content."

    print(view_content(alice))
    try:
        view_content(bob)
    except PermissionError as e:
        print("Caught error:", e)
