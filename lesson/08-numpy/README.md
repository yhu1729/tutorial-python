# Lesson 8: NumPy arrays

[Course home](../../README.md) · [Previous](../07-debug/README.md) · [Next: plotting](../09-plot/README.md)

## Objectives

Create arrays with explicit shapes and numeric types, replace element-by-element
loops with array expressions, predict broadcasting, and distinguish data shared
by a view from data owned by a copy.

NumPy is an external library: it is installed in the course environment rather
than included in Python itself. From the project root:

```sh
uv sync --locked
uv run python lesson/08-numpy/example.py
```

## Arrays are different from lists

```python
import numpy as np

time_s = np.array([0, 1, 2, 3], dtype=float)
position_m = 2.0 + 3.0 * time_s
```

`import numpy as np` imports the module and gives it the conventional short name
`np`. `np.array` builds a numerical array from a list. `dtype=float` requests
floating-point storage (normally binary64 for this usage); `dtype` means the
type of each array element. An array's elements share one storage type, unlike
the general Python list from lesson 4.

With a list, `[1, 2] * 2` repeats the list. With an array, multiplying by 2 scales
each value. The position expression evaluates the affine law `x = x₀ + vt` at
every time. Units are carried by our variable names and reasoning; NumPy does
not automatically check dimensional consistency.

`position_m.shape` is `(4,)`: a tuple describing a one-dimensional array of four
elements. The comma marks a one-element tuple. `position_m.ndim` is 1, and
`position_m.size` is 4. A `(4,)` vector is neither a `(4, 1)` column array nor a
`(1, 4)` row array. These shapes behave differently in array operations.

Python integers have arbitrary precision, but NumPy integers have fixed widths.
Overflow and unintended integer truncation are possible. Use floating arrays
for these physical calculations; do not assume this removes roundoff error.

## Selecting values

```python
mask = position_m > 6.0
selected_m = position_m[mask]
```

A comparison produces a Boolean array: here `[False, False, True, True]`.
Indexing with it selects matching values. This is a **mask**. For combined array
conditions use parentheses and `&` (elementwise AND), for example
`(position_m > 6) & (position_m < 10)`. Python's scalar `and` does not combine
arrays. Use `np.any(mask)` or `np.all(mask)` when you need one Boolean decision.

Ordinary indices and slices still work: `position_m[0]`, `position_m[-1]`, and
`position_m[:2]`. Empty selections are possible; averaging an empty array is not
a meaningful measurement. Check the selection's `size` before averaging data
whose selection is not guaranteed to be nonempty.

## Broadcasting: write down the shapes first

Compute `d = ½at²` for two accelerations and four times:

```python
acceleration_m_s2 = np.array([1.0, 2.0])
distance_m = 0.5 * acceleration_m_s2[:, None] * time_s[None, :] ** 2
```

Inside an array index, `:` selects all elements on that axis and `None` inserts
a length-one axis. The operands have shapes `(2, 1)` and `(1, 4)`. NumPy compares
dimensions from the right: two dimensions are compatible when they are equal
or one of them is 1. Missing leading dimensions act as length-one dimensions.
The result has shape `(2, 4)`; rows label accelerations and columns label times.
This implicit expansion is **broadcasting**. The two input vectors themselves
need not be copied into full grids, but the result still allocates a full grid.

A `(2,)` vector and a `(4,)` vector cannot be multiplied elementwise: their last
dimensions disagree. A `(4, 1)` array and a `(4,)` array produce a `(4, 4)` result,
which may be legal but unintended. Always predict the result shape before using
a physical formula. `*` means elementwise multiplication; matrix multiplication
uses `@`, introduced in lesson 11.

## Reductions and axes

```python
mean_distance_m = distance_m.mean(axis=1)
```

`.mean(...)` is an array method, just as `.append(...)` was a list method.
`axis=1` collapses the columns, leaving one mean for each row. `axis=0` collapses
the rows, leaving one mean for each time. Omitting `axis` averages every element.
`.sum(...)` follows the same axis convention. Labeling axes is part of the model:
the computer cannot know whether such an average is scientifically meaningful.

## Views, copies, and mutation

```python
first_two = position_m[:2]
independent = position_m.copy()
first_two[0] = -1.0
independent[1] = 100.0
```

Basic slicing of an array always returns a **view** that shares storage with
the original. Editing `first_two` changes `position_m`. `.copy()` creates
independent data, so editing `independent` does not affect the original. This
differs from slicing a Python list, which creates a new list (though its elements
can still refer to shared objects). NumPy Boolean and integer-array indexing
produce copies when used to retrieve data. `position_m[mask] = 0`, however,
is an assignment into the original array; it changes the selected elements.

## Expected output

<!-- check-output: example.py -->
```text
Position (m): [ 2.  5.  8. 11.]
Shape: (4,) dtype: float64
Positions above 6 m: [ 8. 11.]
Distance grid (m):
[[0.  0.5 2.  4.5]
 [0.  1.  4.  9. ]]
Mean over time for each acceleration (m): [1.75 3.5 ]
Original after editing a view: [-1.  5.  8. 11.]
Independent copy: [  2. 100.   8.  11.]
```

Array printing can vary in spacing across versions; numerical values and shapes
are the important part. The -1 here intentionally demonstrates mutation, rather
than representing a new physical calculation.

## Common mistakes

- Applying Python list repetition rules to array multiplication.
- Confusing the array's number of elements with its number of axes.
- Broadcasting a vector into an unintended square grid.
- Editing a view while expecting the original to stay unchanged.
- Expecting array division by zero to behave exactly like Python scalar division:
  NumPy can warn and produce nonfinite values. Numerical diagnostics matter.

## Recap and practice

Before running an array expression, state its shapes, storage type, units, and
which outputs own independent data. Use vectorization when it clarifies the
calculation, while accounting for the memory needed by the results.

Try [three exercises](exercise.md), then inspect [worked solutions](solution.py).

[Next: plotting](../09-plot/README.md)
