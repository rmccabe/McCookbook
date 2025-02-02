#!/usr/bin/env python3
"""
all_syntax_demo.py

A single script showcasing a variety of Python syntax and features,
including some 'tricky to remember' examples that can appear in interviews.

Usage:
    python all_syntax_demo.py
"""

import sys
import math


# ------------------------------------------------------------------------------
# 1) Multiple Assignment, Tuple Unpacking, Extended Unpacking
# ------------------------------------------------------------------------------
def multiple_assignment_demo():
    print("\n--- Multiple Assignment, Tuple Unpacking, Extended Unpacking ---")

    # Basic multiple assignment
    x, y = 10, 20
    print(f"x={x}, y={y}")

    # Swapping values in Python (no temporary variable needed)
    x, y = y, x
    print(f"Swapped x={x}, y={y}")

    # Extended unpacking: grabbing the first, the last, and everything else
    data = [1, 2, 3, 4, 5, 6]
    first, *middle, last = data
    print(f"first={first}, middle={middle}, last={last}")


# ------------------------------------------------------------------------------
# 2) Ternary Operator, Walrus Operator (:=), and Chained Comparisons
# ------------------------------------------------------------------------------
def operator_demo():
    print("\n--- Ternary Operator, Walrus Operator, and Chained Comparisons ---")

    # Ternary operator
    age = 17
    status = "Adult" if age >= 18 else "Minor"
    print(f"Ternary operator: age={age}, status={status}")

    # Walrus operator (Python 3.8+): assignment within an expression
    # We'll find any even number in a list
    nums = [1, 3, 5, 8, 9]
    if (even := [n for n in nums if n % 2 == 0]):
        print(f"Walrus found even number(s): {even}")

    # Chained comparisons
    value = 15
    print(f"Chained comparison: 10 < value < 20 = {10 < value < 20}")


# ------------------------------------------------------------------------------
# 3) For-Else Statement
#    The 'else' clause on a 'for' loop executes only if the loop never breaks.
# ------------------------------------------------------------------------------
def for_else_demo():
    print("\n--- For-Else Statement ---")
    items = [2, 4, 6, 8]
    target = 5
    for item in items:
        if item == target:
            print(f"Found the target {target}, breaking...")
            break
    else:
        print(f"Target {target} was not found (else block executed).")


# ------------------------------------------------------------------------------
# 4) *args, **kwargs, and Type Hints
# ------------------------------------------------------------------------------
def varargs_demo(a: int, b: int, *args: float, **kwargs: str) -> int:
    """
    Demonstrates:
    - positional arguments with type hints,
    - variable positional arguments (*args),
    - variable keyword arguments (**kwargs),
    - a return type hint.
    """
    print("\n--- *args, **kwargs, and Type Hints ---")
    print(f"a={a}, b={b}")
    print(f"Additional *args: {args}")
    print(f"Additional **kwargs: {kwargs}")
    return a + b


# ------------------------------------------------------------------------------
# 5) Custom Context Manager with 'with' and Class
# ------------------------------------------------------------------------------
class FileDummy:
    """
    Custom context manager that simulates writing to a file.
    Handy for demonstration of __enter__ and __exit__ magic methods.
    """
    def __init__(self, filename):
        self.filename = filename
        self.file_obj = None

    def __enter__(self):
        print(f"\n--- Entering context: {self.filename} ---")
        self.file_obj = open(self.filename, "w")
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"--- Exiting context: {self.filename} ---")
        self.file_obj.close()


# ------------------------------------------------------------------------------
# 6) Decorators (Functions Wrapping Functions)
# ------------------------------------------------------------------------------
def uppercase_decorator(func):
    """Simple decorator that converts the result of func() to uppercase."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper

@uppercase_decorator
def greet(name):
    return f"Hello, {name}"


# ------------------------------------------------------------------------------
# 7) Generator Functions, 'yield', and 'yield from'
# ------------------------------------------------------------------------------
def countdown(n):
    """A simple countdown generator."""
    while n > 0:
        yield n
        n -= 1

def nested_generator():
    """Generator that yields from another generator."""
    yield from countdown(3)  # 'yield from' delegates iteration to 'countdown'

# ------------------------------------------------------------------------------
# 8) Class with Property, Classmethod, and Staticmethod
# ------------------------------------------------------------------------------
class Circle:
    """Example class to demonstrate property, classmethod, staticmethod, etc."""
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self):
        """Getter property for radius."""
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = value

    @property
    def area(self):
        """Read-only property that computes area on the fly."""
        return math.pi * (self._radius ** 2)

    @classmethod
    def unit_circle(cls):
        """Alternative constructor method for a 'unit circle'."""
        return cls(1.0)

    @staticmethod
    def circle_description():
        """Static method, no 'self' or 'cls' reference."""
        return "A circle is the set of all points in a plane at a given distance from a center point."


# ------------------------------------------------------------------------------
# 9) Del Statement, Pass, and 'is' vs '=='
# ------------------------------------------------------------------------------
def syntax_extras_demo():
    print("\n--- Del Statement, Pass, 'is' vs '==' ---")
    
    # pass statement: placeholder where code is needed but not yet implemented
    for i in range(2):
        if i == 0:
            pass  # do nothing
        else:
            print("Inside else block with pass used above.")
    
    # 'is' vs '=='
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(f"a == b? {a == b}")  # True because contents are same
    print(f"a is b? {a is b}")  # False because they are different objects
    
    # del statement
    temp_var = 42
    print(f"temp_var before del: {temp_var}")
    del temp_var
    # print(temp_var)  # would raise NameError if we uncomment


# ------------------------------------------------------------------------------
# 10) Advanced Slicing with Negative Steps
# ------------------------------------------------------------------------------
def slicing_demo():
    print("\n--- Advanced Slicing ---")
    nums = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Negative step to reverse the list
    reversed_nums = nums[::-1]
    # Slicing a portion with step
    every_second_item = nums[::2]
    print(f"Original: {nums}")
    print(f"Reversed with [::-1]: {reversed_nums}")
    print(f"Every second item with [::2]: {every_second_item}")


# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------
def main():
    print("=== Python Syntax and Features Demo ===")

    multiple_assignment_demo()
    operator_demo()
    for_else_demo()

    result = varargs_demo(3, 5, 7.0, 9.5, key="value", flag="True")
    print(f"Return value (3+5): {result}")

    # Use the custom context manager
    with FileDummy("dummy.txt") as f:
        f.write("Hello, context manager!\n")

    # Demonstrate decorator usage
    print("\n--- Decorators Demo ---")
    print(greet("Alice"))

    # Generator usage
    print("\n--- Generator Functions ---")
    print("Countdown from 3:")
    for val in countdown(3):
        print(val)
    print("Yield from nested generator:")
    for val in nested_generator():
        print(val)

    # Class usage
    print("\n--- Class with property, classmethod, staticmethod ---")
    c = Circle(2.5)
    print(f"Circle radius = {c.radius}, area = {c.area:.2f}")
    c.radius = 3.5
    print(f"New radius = {c.radius}, area = {c.area:.2f}")

    unit = Circle.unit_circle()
    print(f"Unit circle radius = {unit.radius}, area = {unit.area:.2f}")
    print(f"Circle description (static): {Circle.circle_description()}")

    # Syntax extras
    syntax_extras_demo()

    # Advanced slicing
    slicing_demo()

    # Show sys.exit (commented out to avoid interrupting the script)
    # sys.exit("Exiting via sys.exit() demonstration")


if __name__ == "__main__":
    main()
