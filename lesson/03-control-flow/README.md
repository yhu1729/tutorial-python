# Lesson 3: Conditions, loops, and accumulation

[Course home](../../README.md) · [Previous](../02-value-expression/README.md) · [Next: collections](../04-collection/README.md)

## What you will learn

- Choose instructions using `if`, `elif`, and `else`.
- Repeat a calculation with `for` and `range`.
- Track an accumulated sum without overwriting earlier contributions.
- Sample a mathematical function and approximate its integral.

Here a mathematical function is a formula such as `y = x²`. You do not need
a Python function definition yet; lesson 5 introduces reusable functions.
Run this lesson's example from the project root:

```sh
uv run python lesson/03-control-flow/example.py
```

## Choose a branch

A Boolean comparison from lesson 2 can control which statements execute:

```python
temperature_c = 20.0
if temperature_c < 0.0:
    print("Below range")
elif temperature_c <= 100.0:
    print("Within range")
else:
    print("Above range")
```

The colon ends the branch header. The four spaces on the next line indent its
body: the instructions belonging to that branch. Indentation is part of Python
syntax, not decoration. Use spaces consistently, rather than mixing tabs and
spaces. Returning to the earlier indentation level ends the body.

Python checks branches in order. `if` checks the first condition; `elif` means
"else if" and checks another condition only when earlier ones were false.
`else` runs when none of the preceding conditions were true.
Only one branch in this chain runs. Several separate `if` statements can instead
run several bodies, so they do not always mean the same thing.

In this example, 0 and 100 belong to the middle branch. Boundary behavior should
be a deliberate choice. Try values immediately below and at each boundary.

## Repeat with a `for` loop

```python
for index in range(4):
    print(index)
print("Finished")
```

This prints 0, 1, 2, 3, each on its own line, then `Finished`. A `for` statement
assigns each value from its iterable to a name and executes the indented body.
An iterable supplies values one at a time; `range` supplies integers.
The unindented last line runs once after the loop is complete.

`range(stop)` starts at 0 and stops *before* `stop`. `range(start, stop)` starts
at `start`. `range(start, stop, step)` also specifies the integer increment:
`range(2, 7, 2)` supplies 2, 4, 6. The arguments must be integers, and the
increment cannot be zero. `range(0)` supplies no values, so its body never runs.

For four intervals there are five sample points: both endpoints and three
interior points. That is why the example uses `range(interval_count + 1)`.
Compute a coordinate as `left_endpoint + index * step`; the integer index
makes the number of iterations explicit.

## Keep a running total

```python
total = 0.0
for index in range(4):
    total = total + index
print(total)
```

This prints `6.0`. The accumulator `total` starts outside the loop. Each update
uses its old value plus the new contribution, then assigns the result back to
the same name. An assignment can therefore use the name it is updating.
Moving `total = 0.0` inside the body resets the sum every iteration and loses
earlier contributions. Writing `total = index` also loses them.

`total += index` is a shorter update often seen in Python. For the numbers in
this lesson it has the same effect as `total = total + index`. The example uses
the longer form so that the data flow is visible.

## Sample and integrate a function

The example samples `y = x**2` on `[0, 1]` with spacing `h = 1/4`.
Each iteration calculates one `x`, one `y`, and a weight. The branch is inside
the loop, so its indentation is one level deeper than the loop header.

The composite trapezoidal rule is
`I_h = h * (y_0/2 + y_1 + ... + y_(N-1) + y_N/2)`.
Endpoint values appear in one trapezoid each; interior values appear in two,
which explains the half endpoint weights. A weighted sum stores these terms.
After the loop, multiplication by `step` produces the integral estimate.

For this polynomial, the analytic integral is `1/3`. The example prints the
absolute error using the built-in `abs`, which returns a number's magnitude:
`abs(estimate - reference)`. The numerical quadrature has discretization error
even when every instruction is correct. Agreement with a reference is numerical
verification of this calculation, not evidence of a physical model's validity.

Try 8, 16, and 32 intervals. Observe multiple refinements before making a
convergence claim. Lesson 10 will separate discretization and roundoff error.

## Another loop: `while`

A `while` loop repeats while a condition remains true:

```python
count = 0
while count < 3:
    print(count)
    count = count + 1
```

This prints 0, 1, 2. Python rechecks the condition before every iteration.
Without the update, the condition would remain true forever. Prefer `for` when
the iteration count is known; it avoids having to update a counter manually.
If you accidentally start an endless loop in a terminal, Ctrl+C interrupts it.

## Expected output

<!-- check-output: example.py -->
```text
x       y       position
0.00    0.0000  left endpoint
0.25    0.0625  interior
0.50    0.2500  interior
0.75    0.5625  interior
1.00    1.0000  right endpoint
Trapezoidal integral: 0.343750
Analytic integral: 0.333333
Absolute error: 0.010417
```

## Common mistakes

- A missing colon or inconsistent indentation causes a syntax error.
- `range(N)` includes only N integers, from 0 through N−1.
- Resetting the accumulator inside a loop discards previous contributions.
- Printing the final answer inside the loop prints incomplete running estimates.
- `interval_count = 0` makes the step calculation divide by zero. This fixed
  example assumes a positive integer count; later lessons validate inputs.

## Practice and recap

Try [the three exercises](exercise.md), then read [solution.py](solution.py).

```sh
uv run python lesson/03-control-flow/solution.py
```

You can now branch, repeat, accumulate, and compare a discretization with an
analytic result. Next, store several measurements together instead of keeping
only the current value and a running total.
