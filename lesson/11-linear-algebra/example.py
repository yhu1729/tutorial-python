"""Solve a linear system and fit a synthetic force sensor calibration."""

import numpy as np


def solve_system(matrix, right_hand_side):
    """Solve A x = b for finite square A and a one-dimensional b."""
    matrix = np.asarray(matrix, dtype=float)
    right_hand_side = np.asarray(right_hand_side, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError("matrix must be nonempty and square")
    if right_hand_side.shape != (matrix.shape[0],):
        raise ValueError("right_hand_side must be a vector matching the matrix")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(right_hand_side)):
        raise ValueError("system entries must be finite")
    # NumPy raises LinAlgError only for an exactly zero pivot. At cond >= 1/eps,
    # rounding alone can change every digit, so reject instead of guessing.
    if np.linalg.cond(matrix) >= 1.0 / np.finfo(float).eps:
        raise np.linalg.LinAlgError("matrix is singular to working precision")
    solution = np.linalg.solve(matrix, right_hand_side)
    if not np.all(np.isfinite(solution)):
        raise ArithmeticError("computed solution is not finite")
    return solution


def fit_calibration(displacement_array, force_array):
    """Fit force_N = slope_N_per_m * displacement_m + intercept_N."""
    displacement_array = np.asarray(displacement_array, dtype=float)
    force_array = np.asarray(force_array, dtype=float)
    if displacement_array.ndim != 1 or force_array.shape != displacement_array.shape:
        raise ValueError("displacement_array and force_array must be equal-length vectors")
    if displacement_array.size < 2:
        raise ValueError("at least two observations are required")
    if not np.all(np.isfinite(displacement_array)) or not np.all(np.isfinite(force_array)):
        raise ValueError("observations must be finite")
    design = np.column_stack((displacement_array, np.ones(displacement_array.size)))
    coefficient_array, _, rank, _ = np.linalg.lstsq(design, force_array, rcond=None)
    if rank != 2:
        raise ValueError("observations cannot identify both slope and intercept")
    if not np.all(np.isfinite(coefficient_array)):
        raise ArithmeticError("computed coefficients are not finite")
    residual = force_array - design @ coefficient_array
    if not np.all(np.isfinite(residual)):
        raise ArithmeticError("computed residual is not finite")
    return coefficient_array, residual


def main():
    matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
    right_hand_side = np.array([9.0, 8.0])
    solution = solve_system(matrix, right_hand_side)
    print(f"System solution: x={solution[0]:.6f}, y={solution[1]:.6f}")
    print(f"System residual norm: {np.linalg.norm(matrix @ solution - right_hand_side):.3e}")
    displacement_array = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    noise = np.array([0.02, -0.04, 0.04, -0.04, 0.02])
    force_array = 3.0 * displacement_array + 2.0 + noise
    coefficient_array, residual = fit_calibration(displacement_array, force_array)
    print(f"Calibration: slope={coefficient_array[0]:.6f} N/m, "
          f"intercept={coefficient_array[1]:.6f} N")
    print(f"Calibration residual norm: {np.linalg.norm(residual):.6f} N")
    print(f"System condition number: {np.linalg.cond(matrix):.6f}")
    sensitive_matrix = np.array([[1.0, 1.0], [1.0, 1.0 + 1e-8]])
    original = solve_system(sensitive_matrix, [2.0, 2.0 + 1e-8])
    perturbed = solve_system(sensitive_matrix, [2.0, 2.0 + 2e-8])
    print(f"Sensitive condition number: {np.linalg.cond(sensitive_matrix):.3e}")
    print(f"Solution change from a 1e-8 RHS perturbation: {np.linalg.norm(perturbed - original):.6f}")


if __name__ == "__main__":
    main()
