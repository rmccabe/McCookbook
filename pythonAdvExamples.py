"""
Demonstrates 20 more Python concepts with extra explanations:

1) List Comprehensions
2) Dictionary Comprehensions
3) Set Comprehensions
4) enumerate()
5) zip()
6) Ternary Operator
7) globals() and locals()
8) map() and filter()
9) reduce() (requires functools)
10) lambda Functions
11) if __name__ == "__main__"
12) *args and **kwargs
13) Property Decorators
14) Custom Decorators
15) Generator Functions (yield)
16) Generator Expressions
17) Custom Context Manager
18) Dataclasses
19) Named Tuples
20) f-strings

Run via:
    python advanced_concepts_demo.py
"""

# (9) reduce() comes from the functools module
import functools

# (19) Named Tuples: We can create 'record-like' tuples with field names
from collections import namedtuple

# (18) Dataclasses: Introduced in Python 3.7+, simplifies class creation
from dataclasses import dataclass


# --- 19) NAMED TUPLES ---
# namedtuple is a factory function for creating tuple subclasses with named fields
Point = namedtuple("Point", ["x", "y"])


# --- 18) DATACLASSES ---
# A dataclass auto-generates __init__, __repr__, etc. based on class fields
@dataclass
class Person:
    # Type hints (name: str, age: int) are used by dataclasses to create __init__
    name: str
    age: int


# --- 17) CUSTOM CONTEXT MANAGER ---
class FileEcho:
    """
    Demonstrates creating a custom context manager with __enter__ and __exit__ methods.
    Usage:
        with FileEcho("filename.txt") as fe:
            fe.write_and_echo("Hello!")
    This automatically opens the file in __enter__, and closes it in __exit__.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.file_obj = None

    def __enter__(self):
        # __enter__ should return the resource to manage (here, self)
        self.file_obj = open(self.filename, "w")
        return self

    def write_and_echo(self, text: str):
        # We both write to file and print to console
        print(f"[FileEcho] writing: {text}")
        self.file_obj.write(text + "\n")

    def __exit__(self, exc_type, exc_val, exc_tb):
        # __exit__ is called at the end of the 'with' block, even if exceptions occur
        self.file_obj.close()
        print("[FileEcho] File closed.")


# --- 13) PROPERTY DECORATORS ---
class Rectangle:
    """
    Demonstrates @property (getter) and @setter usage.
    This pattern helps control how attributes are accessed and modified.
    """

    def __init__(self, width, height):
        # The actual data is stored in private attributes (by convention, using an underscore).
        self._width = width
        self._height = height

    @property
    def width(self):
        """
        By using @property, we can access `width` as if it's a normal attribute,
        but under the hood, it calls this method.
        """
        return self._width

    @width.setter
    def width(self, value):
        # This setter is called when we do something like `rect.width = 10`
        if value < 0:
            raise ValueError("Width cannot be negative.")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value < 0:
            raise ValueError("Height cannot be negative.")
        self._height = value

    @property
    def area(self):
        """Example of a read-only property (no setter) that calculates area on the fly."""
        return self._width * self._height


# --- 14) CUSTOM DECORATORS ---
def emphasize(func):
    """
    A simple function decorator that intercepts the return value of the decorated function,
    transforms it, and returns the modified result.
    """
    def wrapper(*args, **kwargs):
        # Call the original function
        result = func(*args, **kwargs)
        # Transform its return value
        return f"!!! {str(result).upper()} !!!"
    return wrapper


@emphasize
def greeting(name):
    """Example function that will be 'wrapped' by the emphasize() decorator."""
    return f"Hello, {name}"


# --- 15) GENERATOR FUNCTIONS (yield) ---
def countdown(n):
    """
    Demonstrates using 'yield' to create a generator.
    Each call to 'next()' (or iteration) resumes where it left off.
    """
    while n > 0:
        yield n
        n -= 1


# --- 16) GENERATOR EXPRESSIONS ---
def squares_up_to(n):
    """
    Returns a generator expression that yields squares of numbers up to n.
    This is similar to a list comprehension, but doesn't create the list in memory all at once.
    """
    return (i * i for i in range(n + 1))


def demo_advanced_concepts():
    """
    Main function that demonstrates all 20 concepts in a logical sequence with print statements.
    """

    print("=== 1) List Comprehensions ===")
    # Creates a list of squares for numbers 0 to 5
    # Syntax: [expression for item in iterable if condition]
    squares_list = [x*x for x in range(6)]
    print("List of squares:", squares_list)

    print("\n=== 2) Dictionary Comprehensions ===")
    # Similar to list comprehension, but for dict key-value pairs
    # Syntax: {key_expr: value_expr for item in iterable}
    squares_dict = {x: x*x for x in range(6)}
    print("Dict of squares:", squares_dict)

    print("\n=== 3) Set Comprehensions ===")
    # Similar syntax, but creates a set (unique values only)
    fruits = ["apple", "banana", "cherry", "banana"]  # 'banana' repeated
    fruit_lengths = {len(fruit) for fruit in fruits}
    print("Set of fruit name lengths:", fruit_lengths)

    print("\n=== 4) enumerate() ===")
    # enumerate() attaches an index to each item in an iterable
    for index, fruit in enumerate(fruits):
        print(f"Index {index}: {fruit}")

    print("\n=== 5) zip() ===")
    # zip() combines multiple iterables element-wise
    numbers = [100, 200, 300]
    letters = ["A", "B", "C"]
    for num, let in zip(numbers, letters):
        print(f"Zipped pair: {num} and {let}")

    print("\n=== 6) Ternary Operator ===")
    # Syntax: value_if_true if condition else value_if_false
    age = 20
    status = "Adult" if age >= 18 else "Minor"
    print(f"Ternary operator result (age=20): {status}")

    print("\n=== 7) globals() and locals() ===")
    # globals() returns a dict of the global symbol table
    # locals() returns a dict of the local symbol table in the current scope
    local_var = "I'm local"
    print("Globals keys:", list(globals().keys())[:5], "... (truncated)")  
    print("Locals keys:", list(locals().keys()), "\n(Note: exact contents can vary)")

    print("\n=== 8) map() and filter() ===")
    # map(function, iterable) applies a function to every item of the iterable
    # filter(function, iterable) keeps items where function(item) is True
    nums = [1, 2, 3, 4, 5]
    doubled = list(map(lambda x: x*2, nums))    # multiply each item by 2
    evens = list(filter(lambda x: x % 2 == 0, nums))  # keep only even numbers
    print("Original:", nums)
    print("Doubled (map):", doubled)
    print("Even only (filter):", evens)

    print("\n=== 9) reduce() ===")
    # reduce(function, sequence, initial) repeatedly applies the function to items in sequence
    sum_all = functools.reduce(lambda acc, x: acc + x, nums, 0)
    print("Sum with reduce:", sum_all)

    print("\n=== 10) lambda Functions ===")
    # Anonymous inline functions often used with map, filter, or for short operations
    add = lambda a, b: a + b
    print("Lambda add(3,5):", add(3, 5))

    print("\n=== 12) *args and **kwargs ===")
    # *args: captures positional arguments as a tuple
    # **kwargs: captures keyword arguments as a dictionary
    def show_args_kwargs(*args, **kwargs):
        print("args:", args)
        print("kwargs:", kwargs)

    show_args_kwargs(10, 20, key="value", flag=True)

    print("\n=== 13) Property Decorators ===")
    rect = Rectangle(3, 4)
    print("Initial area:", rect.area)
    # Using the setter for width
    rect.width = 5
    print("New width:", rect.width)
    print("Updated area:", rect.area)

    print("\n=== 14) Custom Decorators ===")
    # greeting() was decorated with @emphasize
    print(greeting("Alice"))

    print("\n=== 15) Generator Functions (yield) ===")
    for val in countdown(3):
        print("countdown value:", val)

    print("\n=== 16) Generator Expressions ===")
    squares_gen = squares_up_to(5)  # returns a generator, not a list
    for sqr in squares_gen:
        print("square from gen:", sqr)

    print("\n=== 17) Custom Context Manager ===")
    # Demonstrates automatically opening & closing a file
    # Creates or overwrites 'echo_output.txt'
    with FileEcho("echo_output.txt") as fe:
        fe.write_and_echo("Hello from custom context manager!")

    print("\n=== 18) Dataclasses ===")
    # Instantiating our Person dataclass
    person = Person("Bob", 30)
    # Dataclasses automatically provide a __repr__ that includes field values
    print("Dataclass Person:", person)

    print("\n=== 19) Named Tuples ===")
    p = Point(2, 3)
    print("Point namedtuple:", p, "(x =", p.x, ", y =", p.y, ")")

    print("\n=== 20) f-strings ===")
    # f-strings (Python 3.6+) allow easy variable interpolation
    name = "Eve"
    # You can embed expressions directly inside {}
    print(f"Hello, {name}. You are {person.age + 5} in 5 years.")

    print("\n=== Demo complete ===")


# --- 11) IF __NAME__ == "__MAIN__" ---
# Common Python idiom that ensures this code only runs if the script
# is invoked directly (and not imported as a module in another script).
if __name__ == "__main__":
    demo_advanced_concepts()
