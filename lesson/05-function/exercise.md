# Exercises: functions and modules

Use only positive pendulum lengths and accelerations in this lesson.
Write your answers in a separate practice file beside `example.py`.

1. Define `kinetic_energy(mass_kg, speed_m_s)` using $E=mv^2/2$.
   Return the energy rather than printing it inside the function.
   Call it for 2 kg at 3 m/s and print the result with units.
2. Import `pendulum_period` from `example`. Compute the period of a 1 m
   pendulum on Earth (default gravity) and the Moon (1.62 m/s²).
   Print their ratio and compare with `math.sqrt(9.81 / 1.62)`.
3. Import `position_at_time` from `example`. Use a loop to print positions
   at 0, 1, 2, and 3 seconds for initial position 1 m and velocity 2 m/s.
   Explain why importing `example` does not print its demonstration.

After attempting all three, read [solution.py](solution.py). Run it with:

```sh
uv run python lesson/05-function/solution.py
```

Expected solution output:

<!-- check-output: solution.py -->
```text
1. Kinetic energy: 9.00 J
2. Moon/Earth period ratio: 2.461
2. Expected ratio: 2.461
3. t=0 s, x=1.0 m
3. t=1 s, x=3.0 m
3. t=2 s, x=5.0 m
3. t=3 s, x=7.0 m
```
