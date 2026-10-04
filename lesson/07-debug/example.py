"""Calculate mean speed while enforcing the numerical input contract."""

import math


def safe_speed(distance_m, elapsed_s):
    """Return m/s for finite distance >= 0 and finite elapsed time > 0."""
    if not math.isfinite(distance_m) or distance_m < 0.0:
        raise ValueError("distance_m must be finite and nonnegative")
    if not math.isfinite(elapsed_s) or elapsed_s <= 0.0:
        raise ValueError("elapsed_s must be finite and positive")
    speed_m_s = distance_m / elapsed_s
    if not math.isfinite(speed_m_s):
        raise OverflowError("speed cannot be represented as a finite float")
    return speed_m_s


def main():
    print(f"Mean speed: {safe_speed(12.0, 3.0):.2f} m/s")
    try:
        safe_speed(12.0, 0.0)
    except ValueError as error:
        print(f"Rejected input: {error}")


if __name__ == "__main__":
    main()
