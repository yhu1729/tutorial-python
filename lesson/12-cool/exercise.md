# Exercises: cooling capstone

Use the existing functions in a scratch script, then read [solution.py](solution.py).

1. Simulate an object initially at the ambient temperature. Also simulate a
   hotter object with `rate=0`. Check the entire returned temperature arrays.
   Derive the expected constant solution in both cases. What does a zero
   horizon return, and why are there still `step_count+1` entries?
2. Simulate heating from `5 °C` toward `20 °C` with `rate=0.1 min^-1`, a
   ten-minute horizon and 40 steps. Compare with the analytic solution and
   verify monotone increase without overshoot. Explain why Euler lies above
   the exact temperature here, although it lies below it for a hot object.
3. Without changing `simulate_temperature`, iterate the temperature excess rule
   `excess = (1 - rate_step) * excess` four times from `excess=60` for
   `rate_step` values `0.5`, `1.0`, `1.5`, `2.0`, and `2.5`. Classify monotone
   decay, damped oscillation, undamped oscillation, and growing oscillation.
   Explain why our integrator rejects even the absolutely stable `1.5` case.
