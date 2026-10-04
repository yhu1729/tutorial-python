# Exercises: files and CSV

Create a practice script beside `example.py`. Import its `read_measurement_list`
function; use the supplied dataset and leave the original unchanged.

1. Read the data and compute the mean position with a loop and `len`.
   Print the answer to three decimal places, with units. Predict it first
   from the symmetry of the five samples.
2. Create `output/06-file/position_cm.csv` using a context manager and
   `csv.writer`. Write columns `time_s,position_cm`, converting metres to
   centimetres. Use one decimal place for both fields.
3. Print only measurements with position strictly greater than 5 m.
   How many rows satisfy the condition? Explain why the row at 5 m is excluded.

Read [solution.py](solution.py) after attempting all three. Run with:

```sh
uv run python lesson/06-file/solution.py
```
