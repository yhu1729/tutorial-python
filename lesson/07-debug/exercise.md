# Exercises: diagnosing errors and testing contracts

1. A calculation for 12 m over 3 s reports 0.25. It used
   `elapsed_s / distance_m`. Diagnose the error by tracking units and comparing
   against a hand calculation. Replace it with `safe_speed` and print 4.00 m/s.
2. Call `safe_speed` with a negative distance, zero elapsed time, and a NaN
   elapsed time. Catch only `ValueError` and print each diagnostic. Do not
   substitute a fabricated numerical answer after a rejection.
3. Create a `unittest.TestCase` class with two tests: a body at rest has zero
   mean speed over a positive interval; negative elapsed time raises
   `ValueError`. Use `assertEqual` and the `assertRaises` context manager.

Read [solution.py](solution.py) after attempting all three. Run with:

```sh
uv run python lesson/07-debug/solution.py
```
