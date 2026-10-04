# Lesson 6: Paths, files, and CSV

[Course home](../../README.md) · [Previous](../05-function/README.md) · [Next: debugging](../07-debug/README.md)

## Objectives

Locate files reliably, manage file lifetimes, read structured data, convert
text to numbers, and save a reproducible result. You will also meet explicit
input checks; the next lesson develops exceptions and tests in detail.

## Paths are objects

A relative path such as `input/measurement.csv` starts at the process's current
working directory. That directory depends on where you ran the command.
Use `pathlib`, part of the standard library, to anchor data to the script:

```python
from pathlib import Path

lesson_directory = Path(__file__).resolve().parent
input_path = lesson_directory / "input" / "measurement.csv"
```

`__file__` is the script's filename, supplied by Python. `Path(...)` constructs
a path object. `.resolve()` obtains its absolute, resolved path; `.parent`
selects the containing directory. `/` joins path components when its left
operand is a `Path`. It does not divide numbers in this expression.
Interactive prompts do not necessarily define `__file__`; this code belongs
in a saved script.

For this lesson's script, `.parents[0]` is its lesson folder, `.parents[1]`
is `lesson`, and `.parents[2]` is the project root. Generated files go under
that root's `output/06-file` folder. You can move the whole project without
editing machine-specific absolute filenames.

## Open and close a resource deliberately

```python
with input_path.open("r", encoding="utf-8", newline="") as stream:
    text = stream.read()
print(text)
```

`"r"` means read; `"w"` means write, replacing an existing file's contents.
`encoding="utf-8"` states how bytes represent text.
`with` is a **context manager**. The indented body uses the open stream;
leaving the body closes it, including when an error interrupts reading.
`.read()` loads the complete file; for large files, iterate through records
instead. We use `newline=""` for CSV so the CSV module handles newlines.

Missing files raise `FileNotFoundError`; insufficient permissions raise
`PermissionError`. Those errors are useful diagnoses and are not hidden.
Writing with `"w"` is intentional here: running an example twice replaces its
generated output, while leaving the source dataset unchanged.

## CSV rows begin as text

CSV means comma-separated values. Our [synthetic dataset](input/README.md)
contains time in seconds and position in metres, with header:

```text
time_s,position_m
0,1
1,3
```

Use a parser rather than manually splitting on commas; CSV permits quoted
fields and separators within quoted text.

```python
import csv

with input_path.open("r", encoding="utf-8", newline="") as stream:
    reader = csv.DictReader(stream, strict=True)
    for row in reader:
        time_s = float(row["time_s"])
        position_m = float(row["position_m"])
```

`DictReader` reads the header and yields each later row as a dictionary.
Its field values are strings: `"3"` becomes the number `3.0` through `float`.
`.fieldnames` holds the parsed header. A numeric-looking string is still text
until converted; do not concatenate it into a scientific calculation.
`strict=True` makes the parser raise `csv.Error` for malformed quoting, such as
an unterminated quoted field. Valid quoted numeric fields still work.

The complete reader appends `(time_s, position_m)` tuples to a list.
`for time_s, position_m in measurement_list` later **unpacks** each two-element
tuple into two local names.

## Check inputs at the boundary

[example.py](example.py) deliberately requires exactly the documented header,
two fields per row, at least one measurement, and finite numeric values.
Empty data cannot define a mean; `nan` and `inf` would contaminate arithmetic.
`math.isfinite(value)` checks that a number is neither NaN nor infinity.
`not` negates a Boolean; `or` accepts either failure condition.

`raise ValueError("message")` stops the calculation with a meaningful error
when a value violates the contract. Around `float(...)`, a narrow
`try` / `except ValueError as error` adds the line number. `raise ... from error`
preserves the original cause. `DictReader` skips completely blank lines, but
no row containing data is quietly discarded.
The complete reader also catches `csv.Error` during header parsing and data-row
iteration, then raises `ValueError` identifying which part could not be parsed.
Exception chaining preserves the parser's more detailed diagnostic.
The next lesson explains how to interpret and test these errors.

`reader.line_num` is the file line on which the current record ends. It stays
correct after skipped blank lines, so an error message points to the line to
fix in an editor. After a syntax error it still names the last good line.
The header error also shows the header that was found. A file saved as
"CSV UTF-8" by some spreadsheet programs starts with an invisible byte order
mark, which appears as `'\ufefftime_s'` in that message.
Extra fields appear under a `None` key in `DictReader`; missing fields have
`None` values, which the reader rejects. `row.values()` accesses all values.
The `in` operator checks membership in a collection.

## Save structured output

```python
output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["count", "mean_position_m"])
    writer.writerow([5, "5.000"])
```

`.mkdir` creates a directory; `parents=True` creates missing ancestors and
`exist_ok=True` permits a folder already present. These are keyword arguments.
`writerow` writes one record. Formatting before writing makes the example's
decimal precision explicit; retaining only three decimals may lose useful
precision for another application.

## Run and inspect

From the project root:

```sh
uv run python lesson/06-file/example.py
```

Expected output:

<!-- check-output: example.py -->
```text
Read 5 measurements
t=0.0 s, x=1.0 m
t=1.0 s, x=3.0 m
t=2.0 s, x=5.0 m
t=3.0 s, x=7.0 m
t=4.0 s, x=9.0 m
Saved output/06-file/summary.csv
```

Open the saved CSV in a text editor: it contains `count,mean_position_m` and
`5,5.000`. The generated folder is ignored by Git.

## Common mistakes

- A relative path accidentally depends on where you run the script.
- Writing with `"w"` to the input path destroys its previous contents.
- CSV values require conversion before arithmetic.
- An empty dataset cannot be averaged; reject it before division.
- Replacing a parsing error with zero invents a measurement.

## Practice and recap

Attempt [three exercises](exercise.md), then read [solution.py](solution.py).
Run `uv run python lesson/06-file/solution.py` from the project root.
It prints mean position 5.000 m, writes the centimetre conversion, and selects
the rows at 3 and 4 s. Reliable file workflows define paths, encoding, units,
format, resource lifetime, and invalid-input behavior explicitly.
