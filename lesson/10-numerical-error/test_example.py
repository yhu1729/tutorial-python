import math
import unittest

from example import central_difference_sin


class DerivativeTest(unittest.TestCase):
    def test_follow_second_order_error_under_refinement(self):
        # sin's identity gives D_h=cos(x)*sin(h)/h; its leading error is
        # |cos(x)|*h**2/6. The h**4 correction is <= h**2/20 relative.
        for x in [0.0, 0.5, 1.0]:
            error_list = []
            for step in [0.2, 0.1, 0.05, 0.025, 0.0125]:
                error = abs(central_difference_sin(x, step) - math.cos(x))
                leading = abs(math.cos(x)) * step**2 / 6
                self.assertLessEqual(abs(error / leading - 1), step**2 / 20 + 1e-9)
                error_list.append(error)
            for coarse, fine in zip(error_list, error_list[1:]):
                self.assertGreater(coarse / fine, 3.98)
                self.assertLess(coarse / fine, 4.01)

    def test_invalid_sample_and_step(self):
        for step in [0.0, -1.0, math.nan, math.inf, 1e-20, 1e308]:
            with self.subTest(step=step), self.assertRaises(ValueError):
                central_difference_sin(1.0, step)
        for x in [math.nan, math.inf, -math.inf]:
            with self.subTest(x=x), self.assertRaises(ValueError):
                central_difference_sin(x, 0.1)

    def test_report_guard_failure(self):
        case_list = [(1e308, 1e308, "sample points"), (1.0, 1e-20, "too small"),
                 (1.0, 1e308, "twice the step")]
        for x, step, message in case_list:
            with self.subTest(x=x, step=step):
                with self.assertRaisesRegex(ValueError, message):
                    central_difference_sin(x, step)

    def test_keep_small_contribution_in_sum(self):
        self.assertEqual(math.fsum([1e16, 1.0, -1e16]), 1.0)


if __name__ == "__main__":
    unittest.main()
