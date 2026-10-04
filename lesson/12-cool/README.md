# Lesson 12: Capstone — simulate, verify, export, and plot cooling

[Course home](../../README.md) · [Previous](../11-linear-algebra/README.md)

## Objectives

Combine functions, validation, arrays, files, plotting, and numerical analysis
into a complete scientific workflow. Verify an explicit time integrator against
an analytic solution and measure convergence over several refinements.
Everything in this lesson is synthetic; no experimental data is required.

## Run the workflow

From the project root:

```sh
uv run --locked python lesson/12-cool/example.py
```

Read [example.py](example.py) alongside this tutorial.
The run produces `output/12-cool/temperature.csv` and `temperature.png`.
Running it again replaces those two generated files.
The root output directory is ignored by Git.
The plot uses the `Agg` backend and works without a graphical desktop.

## State the physical model

Newton's cooling law is

```text
dT/dt = -k * (T - Ta),     T(0) = T0.
```

Temperature is in degrees Celsius, time in minutes, and `k` in inverse minutes.
A temperature difference has the same numerical value in Celsius and kelvin.
The ambient temperature `Ta` and coefficient `k` are constant here.

This model assumes one spatially uniform object temperature and a heat-transfer
rate proportional to the temperature difference. Real objects can have internal
gradients, changing ambient conditions, radiation, or temperature-dependent
properties. Agreement with this equation does not validate those assumptions.

For constant parameters, the analytic solution is

```text
T(t) = Ta + (T0 - Ta) * exp(-k*t).
```

The example uses `T0=80 °C`, `Ta=20 °C`, `k=0.1 min^-1`, and `t_end=10 min`.
At the endpoint, the excess temperature is `60/e` degrees Celsius.
The characteristic time is `1/k=10 min`.

## Discretize time with explicit Euler

Approximate the derivative by a forward difference:

```text
(T[n+1] - T[n])/dt = -k * (T[n] - Ta).
T[n+1] = Ta + (1 - k*dt) * (T[n] - Ta).
```

The right-hand side uses the existing state, so this method is explicit.
With `step_count` updates, there are `step_count+1` saved states including the initial
condition. The step is `horizon/step_count`.

```python
time_array = np.linspace(0.0, horizon, step_count + 1)
temperature_array = np.empty(step_count + 1, dtype=float)
temperature_array[0] = initial
```

`np.linspace` includes both endpoints and chooses evenly spaced times.
`np.empty` allocates an array without initializing its entries.
We must fill every entry before reading it; entry zero is set explicitly,
and each loop iteration fills the next one.
Using floating-point storage avoids truncating computed temperatures to integers.

The recurrence has two algebraically equivalent forms. With `alpha=k*dt`,
we evaluate `current + alpha*(ambient-current)` when `alpha<=0.5`, and
`ambient + (1-alpha)*(current-ambient)` otherwise. Each expression starts
from the nearer endpoint and adds the smaller correction. Reconstructing the
current temperature by subtracting and adding ambient can lose digits when
`alpha` is tiny, even making a heating step decrease slightly. The choice of
formula controls this cancellation without changing the Euler method.

## Make invalid input visible

The reusable function is

```python
time_array, temperature_array = simulate_temperature(initial, ambient, rate, horizon, step_count)
```

It returns two one-dimensional arrays of equal length.
Temperatures and times are finite real scalar inputs; rate and horizon must be
nonnegative. `step_count` must be a positive Python integer, not a Boolean.
`True` is a subclass of `int` in Python, so the explicit Boolean rejection matters.

`isinstance(value, Real)` uses the standard library's real-number classification.
The helper converts accepted scalars to floats and rejects infinities and NaNs.
It also rejects an unrepresentable initial temperature difference and a positive
horizon whose step underflows to zero. Invalid values raise informative errors.
There is no fallback to an empty array or fabricated temperatures.

When the rate, horizon, or initial temperature excess is zero, the simulation
is constant. `temperature_array.fill(initial)` assigns that value to every entry.
A zero horizon still returns `step_count+1` entries at time zero;
this preserves the return shape, although no physical time elapses.

## Stability and monotonicity are different requirements

Write the excess as `theta=T-Ta`. Euler multiplies it by `q=1-k*dt` each step.
For positive `k*dt`, decay requires `abs(q)<1`, equivalent to
`0<k*dt<2`. The bounded absolute-stability region includes `abs(q)=1`;
the endpoint `k*dt=2` gives undamped oscillations rather than relaxation.
For `k*dt>2`, the oscillations grow without bound in exact arithmetic.

For `1<k*dt<2`, the solution approaches equilibrium but switches sides on every
step. A cooling curve would overshoot below ambient, then rebound above it.
Our educational integrator enforces the stronger condition `0<=k*dt<=1`.
It therefore preserves monotone relaxation without crossing the ambient value.
At `k*dt=1`, Euler reaches ambient in one step, which is stable but inaccurate
as an approximation to the analytic transient.

A stable calculation can still have large discretization error.
Choose a finer grid for accuracy, not merely to satisfy the allowed range.
If the object starts colder than ambient, the same equation models heating,
and the same monotonicity condition applies.
In the tests and solutions, `np.diff(temperature_array)` subtracts each entry from
the next. All nonpositive differences establish sampled monotone cooling;
all nonnegative differences establish sampled monotone heating.

## Evaluate the analytic reference

`exact_temperature` accepts a scalar or an array of nonnegative times.
`np.empty_like(time_array)` allocates a result with the time array's shape;
every entry is assigned before it is returned.
`np.ndindex(time_array.shape)` iterates over index tuples; for a vector these are
`(0,)`, `(1,)`, and so on. A scalar array has the single index `()`.
This permits a scalar endpoint check and an entire reference curve with one function.

With `z=rate*time`, the analytic solution is evaluated from the initial value
when `z<=log(2)`:

```text
initial + (ambient-initial) * (-expm1(-z)).
```

[`math.expm1(x)`](https://docs.python.org/3/library/math.html#math.expm1)
computes `exp(x)-1` accurately even for small `x`. It retains the small change
when `exp(-z)` would round to one. For larger `z`, we use the original
ambient-centered expression with `math.exp(-z)`. Retaining this decay directly
matters when a large initial excess still has a measurable remainder:
`1-exp(-z)` may already round to one.

The scalar multiplication avoids NumPy overflow warnings when a very large
positive rate-time product tends to infinity: its exponential decay is zero.
Time zero, zero rate, and equilibrium preserve the stored initial value directly.

## Export results and save a figure

`Path(__file__).resolve().parents[2]` locates the project root from this script,
independent of the terminal's working directory. `mkdir(..., exist_ok=True)`
creates the output directory and allows it to already exist.
CSV writing uses the context manager and encoding introduced in lesson 6.
`zip(time_array, temperature_array, exact)` walks through matching entries together.

The CSV header records units:

```text
time_min,euler_C,analytic_C,absolute_error_C
```

There are 41 data rows for the 40-step run. The initial error is zero.
The figure compares both curves and labels the axes with units.
`plt.close(figure)` releases the figure after saving it; this matters when
a workflow creates many figures.

## Measure convergence at one physical endpoint

The program repeats the simulation with 20, 40, 80, 160, and 320 steps.
All runs end at ten minutes and use the same physical parameters.
It measures `abs(T_numerical(10)-T_exact(10))` rather than comparing array
positions that might represent different physical times.

For this problem, Euler has an exact discrete excess of
`60*(1-1/n)**n` at ten minutes. Expanding its logarithm gives

```text
terminal_error = (60/e) * [1/(2n) + 5/(24n²) + O(n^-3)].
```

The leading error is proportional to `1/n`, hence to `dt`: first order.
Halving `dt` should approximately halve the error.
Several successive ratios near two support the trend.
`math.log2(previous_error/error)` expresses the same evidence as observed order.
There is no nonlinear or linear solver error here; temporal discretization
dominates this grid study, with floating-point roundoff also present.

## Expected results

The 40-step result is approximately `41.793946 °C`; the analytic endpoint is
`42.072766 °C`. Euler cools faster than the exact model for this monotone grid.
The terminal errors decrease from about `0.564 °C` at 20 steps to
`0.0345 °C` at 320 steps. The successive ratios approach two and the observed
orders approach one. Last digits may vary with floating-point libraries.
The saved plot shows two nearby curves; a visually close overlay alone would
not establish convergence or a quantitative accuracy target.

## Verify and interpret

Run the focused tests:

```sh
uv run --locked python -m unittest discover -s lesson/12-cool -p 'test_*.py' -v
```

They check initial values, endpoint times, cooling and heating monotonicity,
the limiting step, equilibrium, zero rate, zero horizon, invalid inputs,
the independent analytic reference, and five-mesh convergence.
Cancellation regressions cover both evaluation branches, tiny heating and
cooling increments, different temperature scales, a result crossing zero,
1024 accumulated small steps, and long-time decay.
They use independent 100-digit `Decimal` references for the stored inputs.
The rounding allowance is four machine epsilons times the result's magnitude
plus its distance to the nearer endpoint, because each formula starts from
that endpoint. Unlike a bound relative to the result alone, it stays
meaningful when the result is near zero, yet it still rejects the earlier
evaluation order that lost small changes.
The convergence bounds come from the expansion above rather than arbitrarily
relaxing a test tolerance. Rounding allowances for tiny differences are separate.

Software checks establish the implemented input/output behavior.
The analytic comparison verifies the integrator for this equation.
Neither shows that a real object's temperatures obey this model.

## Common mistakes and recap

Common mistakes are mixing seconds and minutes, using `step_count` saved values
instead of `step_count+1`, assuming stability means accuracy, and interpreting
an oscillating Euler curve as real temperature oscillation.
Record parameters, units, equations, and error metrics with simulation results.

You now have a reproducible workflow from model to discretization, verification,
CSV output, and figure. Attempt the [three exercises](exercise.md), then run
`uv run --locked python lesson/12-cool/solution.py`.
