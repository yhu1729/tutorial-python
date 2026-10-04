"""Worked solutions: try exercise.md before reading this file."""

import math

from example import position_at_time, pendulum_period


def kinetic_energy(mass_kg, speed_m_s):
    """Return translational kinetic energy in joules."""
    return 0.5 * mass_kg * speed_m_s ** 2


def main():
    # Exercise 1: the returned value can be used in another calculation.
    energy_j = kinetic_energy(2.0, 3.0)
    print(f"1. Kinetic energy: {energy_j:.2f} J")

    # Exercise 2: a default parameter and an explicit keyword argument.
    earth_s = pendulum_period(1.0)
    moon_s = pendulum_period(1.0, gravity_m_s2=1.62)
    print(f"2. Moon/Earth period ratio: {moon_s / earth_s:.3f}")
    print(f"2. Expected ratio: {math.sqrt(9.81 / 1.62):.3f}")

    # Exercise 3: call an imported function in a loop. Importing example ran
    # its definitions, but its demonstration did not print: during an import
    # __name__ is "example", not "__main__", so the main guard skips main().
    for elapsed_s in range(4):
        position_m = position_at_time(1.0, 2.0, elapsed_s)
        print(f"3. t={elapsed_s} s, x={position_m:.1f} m")


if __name__ == "__main__":
    main()
