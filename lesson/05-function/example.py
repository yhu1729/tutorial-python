"""Reusable calculations for uniform motion and a pendulum."""

import math


def position_at_time(initial_position_m, velocity_m_s, elapsed_s):
    """Return position in metres for constant velocity."""
    return initial_position_m + velocity_m_s * elapsed_s


def pendulum_period(length_m, gravity_m_s2=9.81):
    """Return the small-angle period in seconds; both inputs must be positive."""
    return 2.0 * math.pi * math.sqrt(length_m / gravity_m_s2)


def main():
    position_m = position_at_time(1.0, 2.0, 3.0)
    print(f"Position after 3.0 s: {position_m:.2f} m")
    print(f"Pendulum period: {pendulum_period(1.0):.3f} s")
    print(f"Lunar pendulum period: {pendulum_period(1.0, gravity_m_s2=1.62):.3f} s")


if __name__ == "__main__":
    main()
