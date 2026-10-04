# Lesson 09 exercises

Save each figure in `output/09-plot/` using the path pattern from the example.
Include units, a title, and a legend where needed. Close each figure after saving.

## 1. Constant-speed motion

Plot times `[0, 1, 2, 3]` seconds against distances `[0, 3, 6, 9]` metres. Draw a
line with circular markers. Save `motion.png`. Explain what the line between
samples assumes and identify the speed from the graph.

## 2. Exponential decay on a logarithmic axis

Create 101 times between 0 and 50 seconds with `np.linspace`. Calculate
`np.exp(-0.1 * time_s)`. Plot on a logarithmic vertical axis using
`ax.set_yscale("log")`, and save `decay.png`. Explain why the curve is straight
on this axis and why its slope is not read as an ordinary linear-axis slope.

## 3. Compare two models

On one set of axes, plot `np.exp(-rate * time_s)` for rates 0.1 and 0.3 s⁻¹ over
0–10 s. Use a loop, distinct labeled lines, and a legend. Save `rate.png`.
State which model decays faster and what both predict at zero time. These are
analytic models, not a numerical simulation or experimental measurements.

After trying the exercises, inspect [solution.py](solution.py) and run:

```sh
uv run python lesson/09-plot/solution.py
```
