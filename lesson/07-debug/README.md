# Lesson 7: Tracebacks, exceptions, debugging, and tests

[Course home](../../README.md) · [Previous](../06-file/README.md) · [Next: NumPy](../08-numpy/README.md)

## Objectives

Read an error report, check a scientific calculation systematically, enforce
an input contract, and run automated checks with standard-library `unittest`.
The runnable scripts succeed; intentionally broken snippets appear only here.

## Start at the bottom of a traceback

Suppose a saved script contains this deliberately broken code:

```python
def speed(distance_m, elapsed_s):
    return distance_m / elapsed_s

print(speed(12.0, 0.0))
```

Its error report resembles:

```text
Traceback (most recent call last):
  File "practice.py", line 4, in <module>
    print(speed(12.0, 0.0))
          ~~~~~^^^^^^^^^^^
  File "practice.py", line 2, in speed
    return distance_m / elapsed_s
           ~~~~~~~~~~~^~~~~~~~~~~
ZeroDivisionError: division by zero
```

Python prints the full path of your file where this shows `practice.py`.
The `~` and `^` markers underline the expression that was running.
The last line gives the exception type and message. Read upwards to locate
the failing operation, then its caller. The frames describe the sequence of
function calls; they do not mean that every displayed line has a bug.
`SyntaxError` instead means Python could not parse the source, so no ordinary
execution occurred. A missing colon or inconsistent indentation can cause it.

## An exception communicates a failed operation

An **exception** is a Python object representing an error. Raising one exits
the current calculation unless a caller handles it. A deliberate check can
replace a cryptic failure with the contract that was violated:

```python
if elapsed_s <= 0.0:
    raise ValueError("elapsed_s must be positive")
```

`ValueError` means a value is unsuitable for the calculation. In
[example.py](example.py), `safe_speed` accepts finite real-valued distance
greater than or equal to zero and finite elapsed time strictly above zero.
It returns distance divided by time, in m/s. Strings are outside this contract.
`math.isfinite` rejects NaN and infinity. Testing only `value < 0` would miss
NaN because its ordered comparisons are false.

Even finite inputs can produce an unrepresentably large quotient. This
function checks the result and raises `OverflowError` rather than returning
infinity. It does not claim to preserve tiny quotients that underflow to zero.
Lesson 10 explores floating-point limitations more deeply.

Handle an anticipated error close to where you can make a useful decision:

```python
try:
    speed_m_s = safe_speed(12.0, 0.0)
except ValueError as error:
    print(f"Rejected input: {error}")
```

The `try` body is attempted. If it raises `ValueError`, the matching `except`
body runs and binds the diagnostic to `error`. Other exception types continue
to propagate. A blanket `except Exception` can conceal programmer mistakes;
catch only the failure you intend to handle. An invalid observation should
not silently become speed zero, which describes a valid body at rest.

## Debug logic as well as crashes

A program can run successfully and still be wrong. If 12 m over 3 s produces
0.25, inspect the equation: time divided by distance has units s/m.
Distance divided by time gives 4 m/s. Work with a small known example first.

1. Write the expected result and assumptions before changing the code.
2. Reproduce the failure with the smallest input that exposes it.
3. Inspect the inputs and intermediate quantities, including their units.
4. Compare against a hand calculation or analytic reference.
5. Fix the cause and preserve the example as a regression test.

A temporary `print` can reveal a value. For interactive inspection, Python's
standard-library debugger can start with `uv run python -m pdb
lesson/07-debug/example.py` (enter that as one terminal command).
At its prompt, `n` executes the next line, `s` steps into a function,
`p elapsed_s` displays a variable, `c` continues, and `q` quits.
Inspect variables only after the execution has reached a scope defining them.

## Let unittest repeat your checks

Tests run calculations and compare their outcomes with expectations.
`unittest` ships with Python; no new dependency is needed:

```python
import unittest
from example import safe_speed

class SpeedTest(unittest.TestCase):
    def test_known_speed(self):
        self.assertEqual(safe_speed(12.0, 3.0), 4.0)

    def test_zero_time_rejected(self):
        with self.assertRaises(ValueError):
            safe_speed(12.0, 0.0)
```

`class` defines a type of object. This class inherits test-running behavior
from `unittest.TestCase`, named in parentheses. Functions inside a class are
**methods**; `self` refers to the particular test object. Python supplies it
when calling the method. This is enough class knowledge to write tests now.
Methods beginning with `test_` are discovered automatically.
`self.assertEqual` records a failure if values differ.
`with self.assertRaises(ValueError)` passes only when the body raises that
exception, so an expected rejection is a successful test.

The full [test file](test_example.py) covers known and fractional speeds,
zero distance, scaling, invalid inputs, and an overflowing result.
It uses `self.subTest(...)` to report which member of an input loop failed.
`assertRaisesRegex` also checks a diagnostic's relevant wording.
`math.isclose` allows a relative tolerance for nonexact floating-point values.
For example, `safe_speed(0.3, 0.1)` returns `2.9999999999999996` because the
inputs are rounded; `1e-15` allows a few binary64 rounding units for this
short calculation.
Exact equality is appropriate for exactly representable values such as 4.0.

From the root, run discovery in this lesson's directory:

```sh
uv run python -m unittest discover -s lesson/07-debug -p 'test_*.py' -v
```

`-m` runs a Python module. `discover` finds test files, `-s` selects the
starting directory, `-p` selects filenames, and `-v` prints each test name.
Seven tests should pass. The ending reports `Ran 7 tests` and `OK`; elapsed
time varies. To check the previous lesson's CSV contract, change `-s` to
`lesson/06-file`. That file uses `tempfile.TemporaryDirectory()` as a
context manager: tests create isolated files and automatically remove them.

## Run the example

```sh
uv run python lesson/07-debug/example.py
```

Expected output:

<!-- check-output: example.py -->
```text
Mean speed: 4.00 m/s
Rejected input: elapsed_s must be finite and positive
```

## Common mistakes

- Fixing the last visible caller instead of the incorrect operation.
- Catching every exception and continuing with a fabricated answer.
- Testing only ordinary inputs and missing the contract boundaries.
- Treating a passing regression as proof that a physical model is valid.
- Using exact float equality when mathematical values require rounding.

## Practice and recap

Attempt [three exercises](exercise.md), then run
`uv run python lesson/07-debug/solution.py` and inspect [its code](solution.py).
It prints corrected speed 4.00 m/s, three rejected-input diagnostics, and
runs two passing tests. `unittest` writes its summary to the error stream,
so terminal ordering can differ from ordinary printed output.
Contracts, meaningful exceptions, and repeatable tests make calculations
easier to trust; mathematical and physical validation still require evidence.
