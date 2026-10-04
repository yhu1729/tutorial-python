"""Worked solutions for linear algebra and calibration."""

import numpy as np

from example import fit_calibration, solve_system


def main():
    # Exercise 1: substitution independently verifies the computed solution.
    # The result is x=2, y=3: 2*2-3=1 and 2+3=5. matrix @ result
    # sums row products to implement each equation. matrix * result instead
    # broadcasts the vector and multiplies entries, returning a 2x2 array.
    matrix = np.array([[2.0, -1.0], [1.0, 1.0]])
    rhs = np.array([1.0, 5.0])
    result = solve_system(matrix, rhs)
    print(f"1. x={result[0]:.6f}, y={result[1]:.6f}")
    print("   Substitution:", matrix @ result)

    # Exercise 2: a perfect synthetic model should recover known coefficients.
    # Its tiny residual comes from floating-point arithmetic. The example's
    # nonzero residual contains deliberately added observation offsets; a
    # good fit cannot remove components orthogonal to the design columns.
    displacement_array = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    coefficient_array, residual = fit_calibration(
        displacement_array, 4.0 * displacement_array - 0.5
    )
    print(f"2. slope={coefficient_array[0]:.6f}, intercept={coefficient_array[1]:.6f}")
    print(f"   Residual norm: {np.linalg.norm(residual):.3e}")

    # Exercise 3: centering changes coordinates, not the underlying line.
    # With z=x-mean_x and G=F-mean_F, G=slope*z+centered_intercept becomes
    # F=slope*x+(mean_F+centered_intercept-slope*mean_x). Centering only x
    # would leave force_array near 3e6, and cancellation inside the fit would then
    # cost several digits of the slope.
    position_array = np.array([1e6, 1e6 + 1, 1e6 + 2, 1e6 + 3, 1e6 + 4])
    force_array = 3.0 * position_array + 2.0
    mean_x = np.mean(position_array)
    mean_force = np.mean(force_array)
    centered_fit, _ = fit_calibration(position_array - mean_x, force_array - mean_force)
    intercept_from_centered = mean_force + centered_fit[1] - centered_fit[0] * mean_x
    uncentered, _ = fit_calibration(position_array, force_array)
    original_design = np.column_stack((position_array, np.ones(position_array.size)))
    centered_design = np.column_stack((position_array - mean_x, np.ones(position_array.size)))
    print(f"3. Original design condition: {np.linalg.cond(original_design):.3e}")
    print(f"   Centered design condition: {np.linalg.cond(centered_design):.3e}")
    # The error digits depend on the LAPACK build; compare orders of magnitude.
    # Even the centered result subtracts terms near 3e6 N while converting
    # back, so a few rounding units of 3e6 (about 1e-9 N) remain. The intercept
    # at x=0 also extrapolates 1e6 m beyond the data: with real noise its
    # uncertainty would be far larger than either rounding error.
    print(f"   Uncentered intercept error: {abs(uncentered[1] - 2.0):.1e} N")
    print(f"   Centered intercept error: {abs(intercept_from_centered - 2.0):.1e} N")

if __name__ == "__main__":
    main()
