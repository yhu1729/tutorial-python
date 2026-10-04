# Lesson 11: Linear systems and instrument calibration

[Course home](../../README.md) · [Previous](../10-numerical-error/README.md) · [Next: cooling capstone](../12-cool/README.md)

## Objectives

Solve a small system, fit a line to observations, inspect residuals, and
distinguish an accurate algorithm from a well-conditioned mathematical problem.
You know NumPy arrays, shapes, broadcasting, and numerical tolerances.
This lesson adds matrix multiplication and the linear algebra submodule.

## Run the examples

From the project root:

```sh
uv run --locked python lesson/11-linear-algebra/example.py
```

Read [example.py](example.py). The script generates all observations explicitly;
it reads no files and writes only terminal output.
Our synthetic observations are not experimental evidence.

## Translate equations into arrays

The equations

```text
3*x + y = 9
x + 2*y = 8
```

have the matrix form `A @ solution = b`:

```python
matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
right_hand_side = np.array([9.0, 8.0])
```

Each inner list is a row, so `matrix.shape` is `(2, 2)`.
The right-hand side has shape `(2,)`, a vector rather than a column matrix.
`np.linalg` is NumPy's linear algebra submodule, available through `np`.

```python
solution = np.linalg.solve(matrix, right_hand_side)
```

This solves a square system directly. We do not explicitly compute an inverse.
Inversion would add work and introduce another rounding stage.
If elimination meets an exactly zero pivot, NumPy raises
`np.linalg.LinAlgError`. Rounding usually prevents an exact zero, though:
for the singular matrix `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]`, `np.linalg.solve`
returns entries near `3e15` without any error. Our function therefore also
checks the condition number (explained below) and raises `LinAlgError` when
it reaches `1/eps`, about `4.5e15`, where `eps = np.finfo(float).eps` is the
gap between `1.0` and the next float. At that point rounding alone can change
every digit of the answer, so the function refuses rather than returning a
plausible but unsupported answer.

## Matrix multiplication and residuals

The `@` operator performs matrix multiplication:

```python
residual = matrix @ solution - right_hand_side
```

The `*` operator performs elementwise multiplication and may broadcast.
It does not encode the sum over columns needed for a matrix-vector product.
Check shapes before interpreting results.

`np.linalg.norm(residual)` computes the Euclidean norm for this vector.
A zero residual means the stored equations are exactly satisfied in the
performed arithmetic; a small residual measures equation agreement.
It does not, by itself, guarantee a small error in the solution.

## Define a small input contract

`solve_system` accepts a nonempty square matrix and a matching vector.
`np.asarray(value, dtype=float)` converts array-like input to floating-point
array form; it can reuse an existing matching array rather than always copying.
Our functions do not modify the caller's arrays.

`array.ndim` counts axes; `array.size` counts all elements.
We reject incorrect shapes and nonfinite entries before calling a solver.
`np.isfinite(array)` returns a Boolean array, and `np.all(...)` reduces that
array to one Boolean. A NaN in observations is not a missing value policy.
If you need missing-data handling, specify that policy separately.

## Fit an overdetermined system

Suppose a force sensor approximately follows

```text
force_N = slope_N_per_m * displacement_m + intercept_N.
```

Five observations cannot generally satisfy two coefficients exactly.
Choose coefficients that minimize the squared residual norm instead:

```text
minimize ||force - design @ coefficient_array||².
```

The design matrix contains the displacement and constant columns:

```python
design = np.column_stack((displacement_array, np.ones(displacement_array.size)))
```

`np.ones(n)` creates `n` floating-point ones.
`np.column_stack` places equal-length vectors beside each other as columns.
The tuple inside the call contains the two vectors.
For five observations, the resulting shape is `(5, 2)`.
Coefficient zero is the slope; coefficient one is the intercept.

```python
coefficient_array, _, rank, _ = np.linalg.lstsq(design, force_array, rcond=None)
```

`lstsq` returns four results. We unpack them into names; `_` is a conventional
name for a result we do not need. It has no special language behavior.
`rcond=None` selects NumPy's default criterion for identifying numerical rank.
Rank two is required to identify both coefficients with this design.
If every displacement is identical, the two columns are dependent and fail
that requirement; repeating some positions among others is fine.
Nearly dependent columns can also be numerically unidentifiable.

Textbooks often write least squares as the normal equations
`Dᵀ D c = Dᵀ F` for design matrix `D`. They give the same coefficients in exact
arithmetic, but forming `Dᵀ D` squares the condition number. In exercise 3,
`cond(D)` is about `7e11` and `cond(Dᵀ D)` about `5e23`, far beyond `1/eps`.
`lstsq` works with `D` directly (through a singular value decomposition), so
prefer it to solving the normal equations.

Compute the residual vector ourselves, so it has the same meaning for every
valid input. The extra residual-summary output of `lstsq` can be empty in
some shapes or rank cases; it is not a substitute for explicit diagnostics.

## Synthetic data and provenance

The script uses displacement `[0, 1, 2, 3, 4]` metres and the exact law
`force=3*displacement+2` newtons.
It adds fixed offsets `[0.02, -0.04, 0.04, -0.04, 0.02]` newtons.
These values were chosen for teaching; there is no random seed or external source.

The offsets sum to zero and their dot product with displacement is zero.
They are therefore orthogonal to both design columns, so exact least squares
recovers the original slope and intercept despite a nonzero residual.
This deliberately simple case makes both coefficients and residuals verifiable.
It is not a general claim that noise leaves coefficients unchanged.

## Conditioning is sensitivity

The matrix condition number measures how sensitive a solution can be to
relative perturbations in the inputs. The example uses `np.linalg.cond`.
For the default Euclidean norm, it is the largest singular value divided
by the smallest. A large value identifies a potentially sensitive problem.

Consider rows `[1, 1]` and `[1, 1+1e-8]`.
They are almost dependent. A right-hand side perturbation of `1e-8` can
produce an order-one solution change, even with a tiny residual.
This sensitivity is a property of the equations.
Using a reliable solver cannot supply information the equations lack.

For any perturbation in `b`, a standard bound is
`relative_solution_error <= cond(A) * relative_rhs_error` with `A` fixed.
The bound describes a worst case, not every perturbation direction.
Measurement uncertainty should be interpreted together with conditioning.

## Expected output

The validated example prints values like:

```text
System solution: x=2.000000, y=3.000000
System residual norm: 0.000e+00
Calibration: slope=3.000000 N/m, intercept=2.000000 N
Calibration residual norm: 0.074833 N
System condition number: 2.618034
Sensitive condition number: 4.000e+08
Solution change from a 1e-8 RHS perturbation: 1.414214
```

The exact last digits and tiny residuals may vary with the numerical library.
Six printed decimals do not establish six-decimal physical accuracy.
Coefficient units differ from residual units and must remain explicit.

## Verification, mistakes, and recap

Run:

```sh
uv run --locked python -m unittest discover -s lesson/11-linear-algebra -p 'test_*.py' -v
```

Tests verify known system values, an independently constructed calibration,
orthogonality of fitted residuals, exactly and numerically singular systems,
and invalid observations.
For these small, modest-condition systems, tolerances are at rounding scale.
They do not represent acceptable experimental uncertainty.

Common mistakes include using `*` for matrix multiplication, explicitly
inverting a matrix, fitting a single repeated position without checking rank, and
equating a small residual with a uniquely accurate solution.
Changing units or centering coordinates can improve scaling; always transform
coefficients and their units back correctly.

A solve enforces square equations; a fit minimizes inconsistency across
observations. Residuals diagnose agreement, while conditioning diagnoses
sensitivity. Neither validates the physical sensor model by itself.

Attempt the [three exercises](exercise.md), then run
`uv run --locked python lesson/11-linear-algebra/solution.py`.
API details: [solve](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html)
and [lstsq](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html).
