"""Worked solutions for equilibrium, heating and timestep restrictions."""

import numpy as np

from example import exact_temperature, simulate_temperature


def main():
    # Exercise 1: zero excess or zero rate makes the time derivative zero.
    time_array, temperature_array = simulate_temperature(20.0, 20.0, 0.1, 10.0, 40)
    print("1. Equilibrium:", np.all(temperature_array == 20.0))
    _, stationary = simulate_temperature(80.0, 20.0, 0.0, 10.0, 40)
    print("   Zero rate:", np.all(stationary == 80.0))
    time_array, unchanged = simulate_temperature(80.0, 20.0, 0.1, 0.0, 40)
    print("   Zero horizon:", np.all(time_array == 0.0), np.all(unchanged == 80.0))
    # step_count updates plus the initial value always give step_count+1 entries.
    # Here every update has dt=0, so all 41 entries describe the same instant.

    # Exercise 2: for 0<k*dt<1, 1-k*dt < exp(-k*dt). Euler thus
    # reduces the magnitude of the excess faster. A negative heating excess
    # is less negative than the exact excess, giving a higher temperature.
    time_array, temperature_array = simulate_temperature(5.0, 20.0, 0.1, 10.0, 40)
    exact = exact_temperature(time_array, 5.0, 20.0, 0.1)
    print(f"2. Heating: Euler={temperature_array[-1]:.6f} °C, analytic={exact[-1]:.6f} °C")
    print("   Monotone and below ambient:",
          np.all(np.diff(temperature_array) >= 0) and np.all(temperature_array <= 20.0))

    # Exercise 3 intentionally bypasses the integrator to examine amplification.
    # k*dt=1.5 has |1-k*dt|<1, so it is absolutely stable, but its negative
    # factor reverses the excess sign. The integrator rejects this overshoot
    # because its stronger contract is monotone relaxation toward ambient.
    print("3. Amplification of temperature excess")
    case_list = [(0.5, "monotone decay"), (1.0, "one-step decay to zero"),
             (1.5, "damped oscillation"), (2.0, "undamped oscillation"),
             (2.5, "growing oscillation")]
    for rate_step, description in case_list:
        excess = 60.0
        value_list = [excess]
        for _ in range(4):
            excess = (1.0 - rate_step) * excess
            value_list.append(excess)
        print(f"   k*dt={rate_step:.1f}, {description}: {value_list}")


if __name__ == "__main__":
    main()
