# Lesson 4 exercises

Save a script and run it with `uv run python path/to/your_file.py`.

## 1. Summarize measurements

Store lengths `[1.0, 1.5, 2.0, 2.5]` in metres in a list. Use a loop and
`len` to calculate their arithmetic mean. Print two decimal places and the
unit. Print a slice containing the middle two values. Explain its start and
stop indices. State why your mean calculation needs a nonempty list.

## 2. Represent a record

Make a tuple `(2.0, 3.0, 4.0)` for a probe's x, y, z coordinates in metres.
Make a dictionary with keys `name`, `temperature_c`, and `unit`, containing
`"probe B"`, `23.0`, and `"deg C"`. Update only the temperature to `24.0`.
Print the vertical coordinate and updated record. Explain why a string key
and an integer index serve different roles.

## 3. Predict aliases and copies

Start with a list `[10.0, 20.0, 30.0]`. Assign it to a second name, and make
an independent copy with `.copy()`. Through the second name, replace index 1
with `99.0`. Append `40.0` to the copy. Predict all three lists before printing
them. Explain which operations changed the original and why. Limit the example
to a flat list of numbers; nested containers have additional sharing behavior.

After attempting all three, read [solution.py](solution.py) and run:

```sh
uv run python lesson/04-collection/solution.py
```

Expected solution output:

<!-- check-output: solution.py -->
```text
1. Mean length: 1.75 m
1. Middle pair: [1.5, 2.0]
2. Vertical coordinate (m): 4.0
2. Updated record: {'name': 'probe B', 'temperature_c': 24.0, 'unit': 'deg C'}
3. Original: [10.0, 99.0, 30.0]
3. Alias: [10.0, 99.0, 30.0]
3. Independent: [10.0, 20.0, 30.0, 40.0]
```
