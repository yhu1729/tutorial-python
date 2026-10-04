# Lesson 1 exercises

Work in a new Python file of your own. Use only assignment, arithmetic, comments,
and `print` from this lesson. Run your file from the project root with
`uv run python path/to/your_file.py`, replacing the path with your actual filename.

## 1. Convert a length

Assign `42.0` to `length_cm`, convert it to metres in `length_m`, and print the
result with its unit. Predict the answer before running the program.

## 2. Reverse a temperature conversion

Convert `300.0` kelvin to degrees Celsius. Use a separate variable for the result.
Check the result by doing the conversion back on paper. Explain why subtracting
273.15 is appropriate, rather than dividing by it.

## 3. Calculate a speed

A marker travels `2400.0` millimetres in `12.0` seconds. Store both input values,
convert the distance to metres, calculate the average speed in metres per second,
and print a labelled result. Explain what goes wrong if you omit the conversion.

After attempting all three, read [solution.py](solution.py). Run it with:

```sh
uv run python lesson/01-run-python/solution.py
```

Expected solution output:

<!-- check-output: solution.py -->
```text
1. Length (m): 0.42
2. Temperature (C): 26.850000000000023
3. Average speed (m/s): 0.19999999999999998
```

The last two results are very close to 26.85 and 0.2. The extra digits come
from floating-point representation, not from incorrect conversion formulas.
Lesson 2 introduces this effect and how to format readable output.
