

# Demonstrates 20 fundamental Python commands/statements/functions
# in a single script with simulated user input.

import math as m          # (15) Using 'as' to alias a module
from math import pi       # (14) from ... import

x = 2

print("Hello World" + str(x))

def greet(name):          # (11) def: defining a function
    """Greet a user and return the length of the name."""
    print(f"Hello, {name}!")
    return len(name)      # (12) return: returns a value

class Animal:             # (19) class: define a new class
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

def main():
    # (1) print() and (2) input() - but we'll simulate input
    simulated_user_input = "Alice"
    print("Simulated user entered:", simulated_user_input)

    # (3) if, elif, else
    age = 20
    if age < 18:
        print("Minor")
    elif age == 18:
        print("Just became an adult")
    else:
        print("Adult")

    # (4) for loop
    for i in range(3):
        print(f"for-loop iteration {i}")

    # (5) while loop
    count = 0
    while count < 3:
        print(f"while-loop count: {count}")
        count += 1
        # (6) break
        if count == 2:
            print("Breaking out of while loop early...")
            break

    # (7) continue
    for i in range(5):
        if i == 2:
            continue
        print(f"Value of i (skipping 2): {i}")

    # (8) pass
    # Used as a placeholder where code will eventually go
    if True:
        pass  # No operation performed here

    # (9) range() and (10) len()
    numbers = list(range(5))
    print("numbers:", numbers)
    print("length of numbers:", len(numbers))

    # Using the greet() function (which uses def and return)
    name_length = greet(simulated_user_input)
    print("The length of the name is:", name_length)

    # (13) import (done at the top), (14) from..import pi (done at the top), (15) import .. as
    print("Square root of 16 (using 'm' alias):", m.sqrt(16))
    print("Pi constant from 'from math import pi':", pi)

    # (16) try / except
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Caught a ZeroDivisionError")

    # (17) finally
    try:
        file = open("nonexistent.txt", "r")
    except FileNotFoundError:
        print("File not found!")
    finally:
        print("Executed the 'finally' block")

    # (18) with
    # Will fail if data.txt isn't present, but demonstrates usage
    try:
        with open("data.txt", "r") as f:
            content = f.read()
            print("File content:", content)
    except FileNotFoundError:
        print("data.txt not found; skipping read.")

    # (19) class is defined above (Animal)
    dog = Animal("Dog")
    dog.speak()

    # (20) help() and dir()
    print("dir(str):", dir(str))
    # Uncomment the line below if you want to see the help text (it's quite long!)
    # help(print)

if __name__ == "__main__":
    main()
