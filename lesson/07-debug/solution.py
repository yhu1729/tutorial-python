"""Worked diagnoses and two additional tests."""

import math
import unittest

from example import safe_speed


class ExerciseTest(unittest.TestCase):
    def test_rest(self):
        self.assertEqual(safe_speed(0.0, 5.0), 0.0)

    def test_negative_elapsed_time(self):
        with self.assertRaises(ValueError):
            safe_speed(1.0, -2.0)


def main():
    # Exercise 1: distance/time has units m/s; time/distance has units s/m.
    print(f"Corrected speed: {safe_speed(12.0, 3.0):.2f} m/s")

    # Exercise 2: diagnose each invalid observation without inventing data.
    invalid_input_list = [(-1.0, 3.0), (12.0, 0.0), (12.0, math.nan)]
    for distance_m, elapsed_s in invalid_input_list:
        try:
            safe_speed(distance_m, elapsed_s)
        except ValueError as error:
            print(f"Rejected input: {error}")

    # Exercise 3: unittest discovers the class above and runs its two tests.
    unittest.main()


if __name__ == "__main__":
    main()
