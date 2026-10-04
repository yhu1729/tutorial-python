import unittest

import numpy as np

from example import fit_calibration, solve_system


class LinearAlgebraTest(unittest.TestCase):
    def test_known_system(self):
        matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
        solution = solve_system(matrix, [9.0, 8.0])
        # This modest-condition 2x2 system should have roundoff-scale error.
        np.testing.assert_allclose(solution, [2.0, 3.0], rtol=1e-14, atol=0)
        np.testing.assert_allclose(matrix @ solution, [9.0, 8.0], rtol=1e-14, atol=0)

    def test_reject_singular_system(self):
        with self.assertRaises(np.linalg.LinAlgError):
            solve_system([[1.0, 2.0], [2.0, 4.0]], [3.0, 6.0])
        # Rank 2, but rounding leaves no exactly zero pivot: np.linalg.solve
        # alone returns entries near 3e15 for this inconsistent system.
        with self.assertRaisesRegex(np.linalg.LinAlgError, "working precision"):
            solve_system([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
                         [1.0, 0.0, 0.0])

    def test_system_shape_and_finiteness(self):
        case_list = [([], []), ([[1, 2]], [1]), ([[1]], [[1]]),
                 ([[float("nan")]], [1]), ([[1]], [float("inf")])]
        for matrix, rhs in case_list:
            with self.subTest(matrix=matrix, rhs=rhs), self.assertRaises(ValueError):
                solve_system(matrix, rhs)

    def test_known_synthetic_calibration(self):
        x = np.arange(5, dtype=float)
        noise = np.array([0.02, -0.04, 0.04, -0.04, 0.02])
        coefficient_array, residual = fit_calibration(x, 3 * x + 2 + noise)
        # Noise is orthogonal to both columns, so exact least squares is [3,2].
        np.testing.assert_allclose(coefficient_array, [3.0, 2.0], rtol=1e-14, atol=0)
        np.testing.assert_allclose(residual, noise, rtol=0, atol=2e-14)
        design = np.column_stack((x, np.ones(x.size)))
        np.testing.assert_allclose(design.T @ residual, 0, rtol=0, atol=1e-13)

    def test_unidentifiable_or_invalid_calibration(self):
        case_list = [([1], [2]), ([1, 1], [2, 3]), ([1, 2], [3]),
                 ([[1, 2]], [[3, 4]]), ([0, float("nan")], [1, 2]),
                 ([0, 1], [1, float("inf")])]
        for x, y in case_list:
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                fit_calibration(x, y)


if __name__ == "__main__":
    unittest.main()
