# Lesson 5: Functions and modules

[Course home](../../README.md) · [Previous](../04-collection/README.md) · [Next: files](../06-file/README.md)

## Objectives

Define reusable calculations, distinguish parameters from arguments, return
results, and import a function without running a demonstration.
You already know variables, arithmetic, loops, and collections.

## A function is a named calculation

Repeated formulas are difficult to maintain: fixing one copy does not fix the
others. Give the calculation a name and state its inputs explicitly:

```python
def position_at_time(initial_position_m, velocity_m_s, elapsed_s):
    return initial_position_m + velocity_m_s * elapsed_s

position_m = position_at_time(1.0, 2.0, 3.0)
print(position_m)
```

`def` defines a function. Its name follows `def`; parentheses contain
**parameters**, local names for the inputs. A colon starts the indented body.
Defining a function does not perform its calculation. Calling it does.
The values `1.0`, `2.0`, and `3.0` are **arguments** supplied by the caller.
They bind to the parameters in that order. The output above is `7.0`.

`return` sends a value to the caller and ends this call. Assignment stores
that returned value in `position_m`. You can use it in further calculations.
The parameter names exist inside the function; they are not variables in the
caller. Another call creates another set of local bindings.

Our function implements $x(t)=x_0+vt$ and returns position.
The names encode SI units: metres, metres per second, seconds.
Python does not check dimensional consistency; supplying minutes would give
a mathematically executable but physically incorrect answer.

## Returning and printing have different jobs

```python
def double(value):
    return 2 * value

print(double(3) + 1)
```

This prints `7`. A function that only prints its answer cannot be used this
way: without `return`, it returns `None`, Python's value for “no result.”
Keep reusable calculations separate from display decisions such as precision
and units. The caller chooses whether to print, save, or compare the result.

## Import standard-library mathematics

A **module** is a file containing Python definitions. The standard library
ships useful modules with Python; `math` provides scalar mathematical functions:

```python
import math

print(math.sqrt(4.0))
print(math.pi)
```

The dot selects a name inside the module. The first `print` displays `2.0`;
the second displays `3.141592653589793`.
`math.sqrt` computes a square root; `math.pi` is a floating-point approximation
to π. Importing a module gives access to its names without copying code.

For a small-angle pendulum, $P=2\pi\sqrt{L/g}$:

```python
def pendulum_period(length_m, gravity_m_s2=9.81):
    """Return the small-angle period in seconds."""
    return 2.0 * math.pi * math.sqrt(length_m / gravity_m_s2)
```

The triple-quoted first string is a **docstring**: documentation attached to
the function. `gravity_m_s2=9.81` defines a **default argument**.
Omitting gravity uses that value; specifying a keyword makes intent clear:

```python
earth_s = pendulum_period(1.0)
moon_s = pendulum_period(1.0, gravity_m_s2=1.62)
```

Positional arguments must come before keyword arguments:
`pendulum_period(gravity_m_s2=1.62, 1.0)` is a `SyntaxError`.
Here the mathematical contract requires positive, finite length and gravity.
This first version assumes the caller honors that contract; lesson 7 teaches
explicit runtime checks and exceptions. The small-angle and constant-gravity
assumptions belong to the physical model, not the programming language.

## Organize a script for reuse

[example.py](example.py) defines the calculations and a `main()` function
that prints a demonstration. Its final two lines are:

```python
if __name__ == "__main__":
    main()
```

Python supplies `__name__`. Running a file directly sets it to the string
`"__main__"`; importing that file sets it to its module name, `"example"`.
This **main guard** runs the demonstration only when the file is the program.
Comparison with `==` checks equality; it does not assign a value.

A practice file in this same lesson folder can use:

```python
from example import position_at_time

print(position_at_time(1.0, 2.0, 3.0))
```

`from ... import ...` binds just that function name. Run the practice file by
its path as a script; Python searches the script's folder for `example.py`.
The earlier demonstration does not run during import because of the guard.
Importing also lets Python save a compiled copy of `example.py` in a
`__pycache__` folder beside it. That folder is safe to ignore or delete.
Avoid naming practice files `math.py`: that can hide the standard module.

## Run the example

From the project root:

```sh
uv run python lesson/05-function/example.py
```

Expected output:

<!-- check-output: example.py -->
```text
Position after 3.0 s: 7.00 m
Pendulum period: 2.006 s
Lunar pendulum period: 4.937 s
```

The formatting `:.3f` prints three decimal places, without changing the stored
value. The smaller gravitational acceleration increases the period.

## Common mistakes

- Forgetting `return` produces `None` instead of the computed answer.
- Forgetting parentheses refers to a function rather than calling it.
- Changing argument order changes the calculation; keyword arguments clarify it.
- Missing indentation or a colon prevents Python from parsing the function.
- A plausible numerical result does not establish correct units or model assumptions.

## Practice and recap

Attempt [three exercises](exercise.md) before opening
[worked solutions](solution.py). Run solutions with:

```sh
uv run python lesson/05-function/solution.py
```

The solutions print 9.00 J, a period ratio of 2.461, and positions 1, 3, 5,
and 7 m. A function turns explicit inputs into a reusable result. A module
stores definitions, and a main guard separates reuse from demonstration.
