# Lesson 9: Scientific plots with Matplotlib

[Course home](../../README.md) · [Previous](../08-numpy/README.md) · [Next: numerical error](../10-numerical-error/README.md)

## Objectives

Create a figure and axes, draw labeled curves and samples, distinguish scales
and sampling choices, and save an image reproducibly without a graphical desktop.

Matplotlib is the course's second external dependency. From the project root:

```sh
uv sync --locked
uv run python lesson/09-plot/example.py
```

## Build the data before the figure

We plot the analytic expression

$$a(t) = e^{-\gamma t}\cos(\omega t),\qquad
\gamma=0.2\;\mathrm{s}^{-1},\quad \omega=2\;\mathrm{rad/s}.$$

Here `a` is normalized, dimensionless amplitude. This is synthetic analytic
data: it has no measurement uncertainty and is not the output of an ODE solver.

```python
time_s = np.linspace(0.0, 10.0, 101)
envelope = np.exp(-0.2 * time_s)
amplitude = envelope * np.cos(2.0 * time_s)
```

`np.linspace(start, stop, count)` includes both endpoints by default: 101 samples
make 100 intervals of 0.1 s. `np.exp` and `np.cos` evaluate the exponential and
cosine elementwise. Cosine expects radians, not degrees. Each resulting array
has the same shape as the time array, so paired points line up correctly.

## Figure, axes, and backend

```python
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
```

A **figure** is the whole image; an **axes** object is a plotting region inside
it (the name is plural even for one region). `plt.subplots` returns both, and
tuple unpacking gives us `fig` and `ax`. `figsize` is width and height in inches.
We use methods on these objects so it is clear which plot we are changing.

A **backend** renders figures. `Agg` renders raster images without opening a
window; `savefig` still writes a vector format when the filename ends in `.pdf`
or `.svg`. Selecting the backend before importing `pyplot` is the conventional
and safest order; these examples always save files.
You can read the resulting PNG in any image viewer. No Jupyter or GUI toolkit
is needed for this course.

## Curves and samples

```python
ax.plot(time_s, amplitude, label="Damped oscillation")
ax.plot(time_s, envelope, linestyle="--", label="Positive envelope")
ax.scatter(time_s[::10], amplitude[::10], label="Every tenth sample", s=20)
```

`plot(x, y)` joins the sample pairs with line segments; it does not solve an
equation between them. `linestyle="--"` draws a dashed curve. `scatter` displays
separate points; `s` controls marker area in points squared. Both slices use
`::10` to select every tenth value, preserving the pairing of times and amplitudes.
You can also use `ax.plot(x, y, marker="o")` for a line with circular markers.

The oscillation period is approximately 3.14 s, so 0.1 s sampling displays this
particular curve smoothly. A fast oscillation sampled too coarsely could look
smooth yet be misleading. Increasing image resolution cannot recover information
missing from the samples. A plot is a diagnostic, not proof of numerical accuracy.

## Label the physical quantities

```python
ax.set_xlabel("Time (s)")
ax.set_ylabel("Normalized amplitude (dimensionless)")
ax.set_title("Analytic damped oscillation")
ax.grid(True, alpha=0.3)
ax.legend()
```

Labels name quantities and units. A title supplies model context; the legend
matches each `label` to its curve or points. `alpha` is opacity between 0 and 1,
so a light grid helps reading without obscuring the data. Matplotlib cycles
line colors automatically. Color alone may be hard to distinguish; markers
and line styles can help.

For this oscillation, negative amplitudes are physically part of the model.
Use a linear vertical axis. A logarithmic axis is useful for positive decay:

```python
ax.set_yscale("log")
```

This changes how vertical values are displayed; it does not modify the data.
Exponential decay appears straight on a semilog plot because its logarithm is
linear in time. Zero and negative values cannot appear on a standard logarithmic
axis. Decide whether a scale is meaningful before using it, and state the scale
when interpreting a slope.

## Save and release the figure

```python
output_dir = Path(__file__).resolve().parents[2] / "output" / "09-plot"
output_dir.mkdir(parents=True, exist_ok=True)
destination = output_dir / "oscillation.png"
fig.tight_layout()
fig.savefig(destination, dpi=150)
plt.close(fig)
```

Import `Path` from `pathlib` as in lesson 6. The path is anchored to the script's
location; `parents[2]` reaches the project root. The final two components choose
this lesson's output directory. `tight_layout` adjusts spacing to fit labels.
`dpi` controls image pixels per inch, so a 7 by 4 inch figure at 150 dpi is 1050
by 600 pixels. `savefig` selects PNG from the filename extension. Repeating the
script replaces its own image. `plt.close(fig)` releases Matplotlib's reference
to the figure so repeated plots do not accumulate in memory.

## Expected output

<!-- check-output: example.py -->
```text
Samples: 101
Saved: <project-root>/output/09-plot/oscillation.png
```

`<project-root>` represents your actual absolute project path, not literal text
printed by Python. Open that PNG: it should show the damped curve crossing zero,
a dashed positive envelope, and eleven sample markers. Check the legend and
units, then change the damping rate and regenerate the image.

## Common mistakes and recap

- Giving `plot` coordinate arrays of different lengths.
- Assuming a joined curve captures unsampled behavior.
- Labeling a normalized quantity with dimensional units.
- Saving before setting labels or adding the legend.
- Using a logarithmic axis for signed data or forgetting to close figures.

A useful scientific plot communicates provenance, quantities, units, scales,
and sampling. It can reveal problems, but analytic checks and refinement studies
are still needed to establish numerical behavior.

Try [three exercises](exercise.md), then inspect [worked solutions](solution.py).

[Next: numerical error](../10-numerical-error/README.md)
