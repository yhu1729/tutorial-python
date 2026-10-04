# Lesson 08 exercises

Use only the tools introduced so far. Predict shapes and values before running.

## 1. Vectorized motion

Create a floating-point array of times `[0, 0.5, 1]` seconds. With initial position
1 m and speed 4 m/s, calculate positions without a Python loop. Select positions
at least 3 m and calculate the mean of the selected positions. State the units.

## 2. A grid of masses

Use densities `[1, 2, 3]` kg/m³ and volumes `[0.1, 0.2]` m³. Broadcast them into a
mass grid with density along rows and volume along columns. Print its shape and
sum the masses over volumes for each density. Explain why `axis=1` gives three
results, and why summing this array has meaning only if its columns represent
separate objects rather than alternative measurements of one object.

## 3. Who owns the data?

Create measurements `[10, 20, 30, 40]` as floats. Take a basic slice with every
second element, and make a full independent copy. Change the slice's first value
to -10 and the copy's first value to 999. Print all three arrays. Explain which
changes reached the original and why.

After attempting all three, read [solution.py](solution.py) and run:

```sh
uv run python lesson/08-numpy/solution.py
```
