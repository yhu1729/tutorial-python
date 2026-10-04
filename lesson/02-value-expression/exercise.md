# Lesson 2 exercises

Use a saved script and run it with `uv run python path/to/your_file.py`.

## 1. Format an energy

Calculate the kinetic energy of a `2.0` kg object travelling at `3.0` m/s.
Use `**` for the square and an f-string to print three digits after the decimal
point, followed by `J`. Predict the value and the output representation.

## 2. Group samples

There are 17 samples and each full group holds 4. Use `//` and `%` to calculate
the number of full groups and the number of remaining samples. Explain why
ordinary division answers a different question.

## 3. Heat an ideal gas

At fixed amount of gas and volume, an ideal gas has `P_final / P_initial =
T_final / T_initial`. Starting from `100000.0` Pa at `250.0` K, calculate the
pressure at `300.0` K. Print two decimal places and a Boolean comparison to the
initial pressure. Explain why using Celsius in the ratio would be incorrect.

After attempting all three, read [solution.py](solution.py) and run:

```sh
uv run python lesson/02-value-expression/solution.py
```

Expected solution output:

<!-- check-output: solution.py -->
```text
1. Kinetic energy: 9.000 J
2. Full groups: 4
2. Remaining samples: 1
3. Final pressure: 120000.00 Pa
3. Above initial pressure: True
```
