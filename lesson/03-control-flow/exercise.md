# Lesson 3 exercises

Use only previously introduced syntax. Save a script and run it with
`uv run python path/to/your_file.py`.

## 1. Classify a value

Use `if`, `elif`, and `else` to label a temperature as `below range` for values
below 0 °C, `within range` from 0 through 100 °C inclusive, or `above range`
for values above 100 °C. Print the result for 20 °C, then change the input and
rerun at -1, 0, 100, and 101 °C. This is a numerical classification rule, not
a claim about phase transitions at arbitrary pressure.

## 2. Accumulate a sum

Use `range` and a `for` loop to add the integers from 1 through 10. Initialize
the accumulator before the loop. Compare the result with `10 * 11 / 2`.
Explain why `range(1, 10)` would miss one term.

## 3. Integrate a straight line

Adapt the example to integrate `y = x` on `[0, 1]` with four intervals. Retain
half weights for both endpoints. Compare against the analytic integral, 0.5.
Explain why trapezoids fit this function exactly in real arithmetic. Then try
eight intervals and compare with the behavior of `y = x**2`.

After attempting all three, read [solution.py](solution.py) and run:

```sh
uv run python lesson/03-control-flow/solution.py
```

Expected solution output for the first inputs in each exercise:

<!-- check-output: solution.py -->
```text
1. Category: within range
2. Sum: 55
2. Formula 10 * 11 / 2: 55.0
3. Integral of x on [0, 1]: 0.500000
3. Absolute error: 0.000000
```
