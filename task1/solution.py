from functools import wraps
from inspect import signature
import unittest
def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        bound_args = sig.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            expected_type = func.__annotations__.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f"Argument '{name}' must be of type {expected_type.__name__}, got {type(value).__name__}")
        
        return func(*args, **kwargs)

    return wrapper


@strict
def add(a: int, b: int) -> int:
    return a + b

@strict
def greet(name: str, excited: bool) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"

@strict
def multiply(a: float, b: float) -> float:
    return a * b

class TestStrictDecorator(unittest.TestCase):
    def test_add_correct(self):
        self.assertEqual(add(5, 3), 5)

    def test_add_incorrect_type(self):
        with self.assertRaises(TypeError):
            add(2, "3")  # str вместо int

    def test_greet_correct(self):
        self.assertEqual(greet("Alice", True), "Hello, Alice!")

    def test_greet_wrong_bool(self):
        with self.assertRaises(TypeError):
            greet("Alice", "yes")  # str вместо bool

    def test_multiply_correct(self):
        self.assertAlmostEqual(multiply(2.5, 4.0), 10.0)

    def test_multiply_wrong_type(self):
        with self.assertRaises(TypeError):
            multiply(2.5, 1)  # int вместо float

    def test_missing_annotation_ignored(self):
        @strict
        def f(a, b: int):  # a без аннотации
            return b
        # тип a не проверяется, так что вызов пройдет
        self.assertEqual(f("any", 1), 1)

if __name__ == "__main__":
    unittest.main()
