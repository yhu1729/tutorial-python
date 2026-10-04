# Lesson 2: Values, expressions, and scientific formulas

[Course home](../../README.md) · [Previous](../01-run-python/README.md) · [Next: control flow](../03-control-flow/README.md)

## What you will learn

- Distinguish integers, floating-point numbers, strings, and Booleans.
- Translate a scientific formula into a Python expression.
- Use exponentiation, floor division, remainder, and comparisons.
- Format numerical output without changing the underlying calculation.

This lesson builds on assignment and `print` from lesson 1. Run its example from
the project root:

```sh
uv run python lesson/02-value-expression/example.py
```

## Values have types

A type determines what operations a value supports and what they mean.

| Type | Literal example | Use |
|---|---|---|
| `int` | `5` | Counts and discrete indices |
| `float` | `0.25` | Approximate real-valued measurements |
| `str` | `"trial A"` | Labels and other text |
| `bool` | `True` | A yes/no condition |

A literal is a value written directly in code. `True` and `False` start with
capital letters and have no quotes. `"True"` is instead a string.
Integers can grow beyond a fixed machine word in Python; floating-point values
have limited precision and range. On the course interpreter, floats use binary64
(IEEE 754 double precision), which keeps about 15 to 17 significant digits.

```python
sample_count = 5
mass_kg = 0.25
sample_name = "trial A"
calibration_valid = True
```

Assignment binds a name to a value; it does not permanently fix the name's type.
Avoid reusing a measurement name for unrelated text, even though Python allows
it. Consistent meaning makes mistakes easier to spot.

## Translate formulas deliberately

Kinetic energy is `E = (1/2) m v²`. In Python, write:

```python
kinetic_energy_j = 0.5 * mass_kg * speed_m_per_s**2
```

`**` raises a number to a power. `^` does not mean exponentiation in Python.
Powers bind more tightly than multiplication, so the speed is squared first.
Use parentheses whenever the intended grouping is not immediately clear.
For example, `(-2.0)**2` is `4.0`, whereas `-2.0**2` is `-4.0`.

Scientific notation uses `e`: `2.0e-3` means `2.0 * 10**(-3)`, or `0.002`.
It is useful for large and small SI quantities. Python does not accept a unit
suffix such as `2.0e-3 m3`; encode units in names and printed labels.

The ideal-gas law is `P = n R T / V`. The example uses `n = 0.1 mol`,
`T = 300 K`, `V = 0.002 m³`, and
`R = 8.31446261815324 J/(mol K)`. Substituting SI units gives pascals.
The assumptions of an ideal gas are part of the physical model; Python cannot
establish that a particular gas obeys them. Absolute temperature is required.

## Division and remainder

`/` performs ordinary division: `5 / 2` gives the float `2.5`.
`//` performs floor division: `5 // 2` gives the integer `2`.
With a float operand the result is a float: `5.0 // 2` gives `2.0`.
`%` gives the remainder: `5 % 2` gives `1`.
These last two are useful when allocating positive counts into whole groups.
For negative values, floor division rounds toward negative infinity, not zero:
`-5 // 2` is `-3`. For counts in this lesson we use nonnegative integers only.

## Strings and formatted output

You can combine two strings with `+`, as in `"trial " + "A"`. Adding a string
to a number is not a unit conversion and fails with `TypeError`. Use `print`
with separate arguments or an f-string when text must include a number.

An f-string has an `f` before the opening quote. Expressions inside `{...}`
are evaluated and inserted into the text:

```python
print(f"Kinetic energy: {kinetic_energy_j:.2f} J")
```

The colon introduces a format specification. `.2f` displays fixed-point notation
with two digits after the decimal point. `.3e` displays scientific notation with
three digits after the decimal point. A name inside braces with no specification
uses its default text representation. Formatting rounds the displayed text; it
does not increase the accuracy of the data or change the stored value.

## Comparisons and logic

`==` compares values for equality; `=` assigns a value. Comparisons produce a
Boolean. Other comparisons are `!=` (not equal), `<`, `<=`, `>`, and `>=`.
For example, `pressure_pa > 100000.0` asks whether pressure exceeds a threshold.
You can combine conditions with `and`, `or`, and `not`:

```python
within_limits = pressure_pa >= 10000.0 and pressure_pa <= 200000.0
print("Within limits:", within_limits)
```

Both sides must be true for `and`; at least one must be true for `or`.
`not` reverses a Boolean. A condition does not yet change execution: lesson 3
will use it to choose which statements to run.

## A first floating-point surprise

`0.1 + 0.2 == 0.3` is `False` on this interpreter. Many decimal fractions do
not have finite binary representations. Tiny rounding errors arise even in
simple arithmetic; exact equality can be inappropriate for computed floats.
This is different from measurement uncertainty or physical-model error.
Lesson 10 will study roundoff, cancellation, and justified tolerances.

## Expected output

<!-- check-output: example.py -->
```text
Sample: trial A; count: 5; calibrated: True
Kinetic energy: 18.00 J
Ideal-gas pressure: 124716.94 Pa
Pressure in scientific notation: 1.247e+05 Pa
Whole groups of two: 2
Leftover samples: 1
Pressure exceeds 100000 Pa: True
0.1 + 0.2 == 0.3: False
```

## Common mistakes

- `^2` does not square a value. Use `**2`.
- `"5"` is text, not an integer count. Quotation marks change the type.
- Printed decimal places do not certify significant figures or numerical accuracy.
- A formula copied with missing parentheses can execute and give the wrong result.
- Celsius cannot replace kelvin in the ideal-gas law.

## Practice and recap

Try [the three exercises](exercise.md), then read [solution.py](solution.py).

```sh
uv run python lesson/02-value-expression/solution.py
```

You can now express scientific formulas, reason about basic value types, format
results, and construct Boolean comparisons. Next, use those comparisons to
control execution and repeat calculations with loops.
