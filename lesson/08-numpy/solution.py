"""Worked solutions: vectorized arithmetic, grid axes, and array views."""

import numpy as np


def main():
    time_s = np.array([0, 0.5, 1], dtype=float)
    position_m = 1.0 + 4.0 * time_s
    selected_m = position_m[position_m >= 3.0]
    print("1. Position (m):", position_m)
    print("Selected mean (m):", selected_m.mean())

    density_kg_m3 = np.array([1, 2, 3], dtype=float)
    volume_m3 = np.array([0.1, 0.2])
    mass_kg = density_kg_m3[:, None] * volume_m3[None, :]
    print("2. Mass grid (kg):")
    print(mass_kg)
    print("Shape:", mass_kg.shape)
    # Collapse columns (volumes) while retaining one value for each row (density).
    print("Sum over separate volumes (kg):", mass_kg.sum(axis=1))

    measurement_array = np.array([10, 20, 30, 40], dtype=float)
    view = measurement_array[::2]
    independent = measurement_array.copy()
    view[0] = -10.0
    independent[0] = 999.0
    print("3. Original:", measurement_array)
    print("View:", view)
    print("Copy:", independent)


if __name__ == "__main__":
    main()
