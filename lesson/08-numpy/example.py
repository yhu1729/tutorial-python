"""Vectorized calculations, broadcasting, and explicit array ownership."""

import numpy as np


def main():
    time_s = np.array([0, 1, 2, 3], dtype=float)
    position_m = 2.0 + 3.0 * time_s
    print("Position (m):", position_m)
    print("Shape:", position_m.shape, "dtype:", position_m.dtype)
    print("Positions above 6 m:", position_m[position_m > 6.0])

    acceleration_m_s2 = np.array([1.0, 2.0])
    # Rows are accelerations; columns are sampling times.
    distance_m = 0.5 * acceleration_m_s2[:, None] * time_s[None, :] ** 2
    print("Distance grid (m):")
    print(distance_m)
    print("Mean over time for each acceleration (m):", distance_m.mean(axis=1))

    first_two = position_m[:2]
    independent = position_m.copy()
    first_two[0] = -1.0
    independent[1] = 100.0
    print("Original after editing a view:", position_m)
    print("Independent copy:", independent)


if __name__ == "__main__":
    main()
