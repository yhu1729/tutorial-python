"""Unit and numerical contract tests for the lesson's calculation."""

import math
import unittest

from example import safe_speed


class SafeSpeedTest(unittest.TestCase):
    def test_known_speed(self):
        self.assertEqual(safe_speed(12.0, 3.0), 4.0)

    def test_zero_distance(self):
        self.assertEqual(safe_speed(0.0, 3.0), 0.0)

    def test_fractional_speed(self):
        # Decimal 0.3 and 0.1 are rounded in binary64, so the computed ratio is
        # 2.9999999999999996, not 3.0: exact equality would fail here.
        self.assertTrue(math.isclose(safe_speed(0.3, 0.1), 3.0, rel_tol=1e-15))

    def test_preserve_speed_under_input_scale(self):
        self.assertEqual(safe_speed(120.0, 30.0), safe_speed(12.0, 3.0))

    def test_invalid_distance(self):
        for distance_m in [-1.0, math.nan, math.inf, -math.inf]:
            with self.subTest(distance_m=distance_m):
                with self.assertRaisesRegex(ValueError, "distance_m"):
                    safe_speed(distance_m, 3.0)

    def test_invalid_time(self):
        for elapsed_s in [0.0, -1.0, math.nan, math.inf, -math.inf]:
            with self.subTest(elapsed_s=elapsed_s):
                with self.assertRaisesRegex(ValueError, "elapsed_s"):
                    safe_speed(12.0, elapsed_s)

    def test_unrepresentable_result(self):
        with self.assertRaisesRegex(OverflowError, "finite float"):
            safe_speed(1e308, 1e-308)


if __name__ == "__main__":
    unittest.main()
