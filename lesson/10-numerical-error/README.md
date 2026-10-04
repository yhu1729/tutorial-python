# Lesson 10: Numerical error — when correct code gives approximate numbers

[Course home](../../README.md) · [Previous](../09-plot/README.md) · [Next: linear algebra](../11-linear-algebra/README.md)

## Objectives

By the end, you can distinguish floating-point roundoff from approximation
error, compare values with justified tolerances, and measure finite-difference
convergence against a known derivative.

You already know functions, loops, exceptions, and the `math` module.
This lesson adds several tools for reasoning about numerical results.
No NumPy is needed for this experiment.

## Run the experiment

From the project root, run:

```sh
uv run --locked python lesson/10-numerical-error/example.py
```

Open [example.py](example.py) beside this tutorial.
Read `main()` first, then the derivative function it calls.
The program writes only terminal output.

## Decimal notation and binary representation

The mathematical numbers 0.1, 0.2, and 0.3 have finite decimal expansions.
Their binary expansions repeat, so a typical Python `float` stores rounded
approximations. Arithmetic then rounds the computed result again.
Try predicting this expression before running it:

```python
print(0.1 + 0.2 == 0.3)
```

It prints `False`. Printing `0.1 + 0.2` exposes the familiar extra digits.
The equality operator compares the stored numbers; it does not infer your
physical or mathematical intent.

Scientific notation `1e-12` means `1 × 10**(-12)`.
It is useful for quantities spanning many orders of magnitude.
It does not make a value exact.

## Comparisons require a scale

`math.isclose(a, b, rel_tol=..., abs_tol=...)` returns a Boolean.
Its comparison is equivalent to:

```text
abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
```

The `max` function selects the larger value.
A relative tolerance is dimensionless; an absolute tolerance has the same
units as the compared quantity.
Near zero, a relative tolerance alone is usually insufficient.
For example, an error of `1e-12` is never relatively small compared to zero.

```python
math.isclose(1e-12, 0.0, rel_tol=1e-9, abs_tol=2e-12)
```

This returns `True` because the absolute bound applies.
Choose the bound from measurement uncertainty, rounding analysis, or a known
algorithmic error scale. Do not keep increasing a tolerance until a test passes.
The decimal example uses `rel_tol=1e-15` to allow a few rounding units at that
scale; this tolerance is not a universal scientific accuracy requirement.

## Addition order and cancellation

Consider this sequence of operations:

```python
total = 0.0
for value in [1e16, 1.0, -1e16]:
    total += value
```

The small contribution disappears when added to the large value.
The final total is zero even though the exact sum is one.
`+=` reassigns the total after each addition, so each iteration rounds.

`math.fsum` uses a more accurate summation algorithm:

```python
math.fsum([1e16, 1.0, -1e16])
```

This returns `1.0`. It cannot recover accuracy already lost while computing
the input values. On the course's Python 3.14, built-in `sum` also compensates
for float rounding, so `sum([1e16, 1.0, -1e16])` returns `1.0` as well.
We use an explicit loop to make the individual rounding steps visible.

Cancellation also occurs when subtracting nearby approximations.
If `a` and `b` each carry small absolute errors, the difference `a-b` can have
a large relative error when the true difference is tiny.
This is why algebraically equivalent formulas need not be numerically equivalent.

## Approximate a derivative

For a differentiable function, the central difference is

```text
D_h f(x) = [f(x+h) - f(x-h)] / (2h).
```

For `f(x)=sin(x)`, the exact derivative is `cos(x)`.
This analytic result provides an independent reference.
Python's sine and cosine arguments use radians.

The function `central_difference_sin(x, step)` accepts a finite point and
a finite positive step. It rejects a step so small that `x+step == x` or
`x-step == x` in floating-point arithmetic.
It also rejects sample points or a doubled step that overflow the float range.
`math.isfinite` excludes both infinities and NaNs.
The keyword `not` reverses a Boolean test.

The function returns a scalar derivative approximation.
The expression `abs(approximation - exact)` measures absolute error.
That number contains discretization error and floating-point error together.

## Derive the expected order

Taylor expansion around `x` cancels the even powers in the numerator:

```text
D_h f(x) = f'(x) + h² f'''(x)/6 + O(h⁴).
```

For sine, a trigonometric identity gives an even more direct result:

```text
D_h sin(x) = cos(x) * sin(h)/h.
error ≈ abs(cos(x)) * h²/6.
```

When this leading term dominates, halving `h` reduces the error by four.
An observed order is `log2(error_coarse/error_fine)`.
This estimates an asymptotic trend, rather than proving an order by itself.
Study several consecutive refinements at fixed `x` and with the same metric.

The example tracks `previous_error`, initially `None`.
`None` marks the absence of a previous row; `is None` tests that sentinel.
The first row has no ratio. Later rows divide the previous error by the new one.
The expression `"-" if previous_error is None else formatted_ratio` selects
one value: Python evaluates the condition first, then only the chosen branch.
It is a compact conditional expression, rather than a complete `if` statement.
The format `:.6e` prints six decimal places in scientific notation.

## Expected output and interpretation

The first part prints:

```text
0.1 + 0.2 == 0.3: False
isclose: True
Loop sum: 0.0; fsum: 1.0
step       absolute error   previous/current
 0.2000    3.594818e-03     -
 0.1000    9.000537e-04     3.994
 0.0500    2.250978e-04     3.999
 0.0250    5.627973e-05     4.000
 0.0125    1.407026e-05     4.000
```

The tiny-step experiment then stops improving.
On the validated interpreter, the error at `1e-6` is about `2.8e-11`, but
at `1e-12` it is about `1.2e-5`. Last digits depend on the platform math library.
Subtracting nearby sine values and dividing by a tiny step amplifies roundoff.
A rough error model is `C*h² + D*epsilon/h`; the two terms compete.
An appropriate step balances them rather than tending blindly toward zero.

## Verification and limits

Run the independent mathematical and invalid-input checks:

```sh
uv run --locked python -m unittest discover -s lesson/10-numerical-error -p 'test_*.py' -v
```

The refinement test compares against the Taylor coefficient at three points,
including five step sizes each. It allows the known next-order correction
and a small rounding allowance. It does not require identical last digits.
We deliberately do not assert a particular tiny-step error on every platform.

## Common mistakes and recap

- Treating more printed digits as evidence of more accuracy.
- Using exact equality for values that have been rounded independently.
- Choosing an absolute tolerance without specifying units.
- Assuming that a smaller finite-difference step always improves accuracy.
- Checking only two grids and calling the ratio a proven convergence order.

Roundoff comes from finite arithmetic; truncation comes from approximating
the mathematics. Accurate summation, stable formulas, justified tolerances,
and analytic references help distinguish and control them.
Work through the [three exercises](exercise.md), then run
`uv run --locked python lesson/10-numerical-error/solution.py`.
API details: [Python math documentation](https://docs.python.org/3/library/math.html).
