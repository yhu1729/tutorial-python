import math
import sys
import unittest
from decimal import Decimal, localcontext

import numpy as np

from example import measure_convergence_error, exact_temperature, simulate_temperature

EPS = sys.float_info.epsilon


def decimal_reference_pair(initial, ambient, rate, time):
    """Independent one-step Euler and analytic values for the stored inputs."""
    with localcontext() as context:
        context.prec = 100
        initial = Decimal.from_float(float(initial))
        ambient = Decimal.from_float(float(ambient))
        rate_time = Decimal.from_float(float(rate)) * Decimal.from_float(float(time))
        excess = initial - ambient
        euler = ambient + excess * (1 - rate_time)
        analytic = ambient + excess * (-rate_time).exp()
        return float(euler), float(analytic)


def decimal_euler(initial, ambient, rate_step, step_count):
    """Independent n-step Euler values and the largest |temperature| reached."""
    with localcontext() as context:
        context.prec = 100
        temperature = Decimal.from_float(float(initial))
        ambient = Decimal.from_float(float(ambient))
        rate_step = Decimal.from_float(float(rate_step))
        largest = abs(temperature)
        for _ in range(step_count):
            temperature += rate_step * (ambient - temperature)
            largest = max(largest, abs(temperature))
        return float(temperature), float(largest)


class TemperatureTest(unittest.TestCase):
    def assert_within_rounding(self, actual, expected, initial, ambient):
        # Each formula starts from the endpoint nearer the result, so its few
        # rounding errors scale with |result| and with the distance from the
        # result to that endpoint, not with larger cancelled terms. These
        # inputs make rate*time exact whenever the far endpoint is used. A
        # bound of a few units in the last place of the result alone would fail
        # when a result crosses zero.
        distance = min(abs(expected - initial), abs(expected - ambient))
        bound = 4 * EPS * (abs(expected) + distance)
        self.assertLessEqual(abs(float(actual) - expected), bound)

    def test_initial_value_and_monotone_temperature_decay(self):
        time_array, temperature_array = simulate_temperature(80, 20, 0.1, 10, 40)
        self.assertEqual(time_array.shape, (41,))
        self.assertEqual(time_array[0], 0)
        self.assertEqual(time_array[-1], 10)
        self.assertEqual(temperature_array[0], 80)
        self.assertTrue(np.all(np.diff(temperature_array) <= 0))
        self.assertTrue(np.all(temperature_array >= 20))
        # Euler cools faster than the exact solution; allow a few rounding
        # units at the 80 C scale where the two nearly agree.
        exact = exact_temperature(time_array, 80, 20, 0.1)
        self.assertTrue(np.all(temperature_array <= exact + 4 * EPS * 80))

    def test_temperature_rise_and_monotonicity_boundary(self):
        _, temperature_array = simulate_temperature(5, 20, 0.1, 10, 40)
        self.assertTrue(np.all(np.diff(temperature_array) >= 0))
        self.assertTrue(np.all(temperature_array <= 20))
        _, boundary = simulate_temperature(80, 20, 1, 1, 1)
        np.testing.assert_array_equal(boundary, [80, 20])

    def test_equilibrium_zero_rate_and_zero_horizon(self):
        for initial, ambient, rate, horizon in [(20, 20, 0.1, 10),
                                                (80, 20, 0, 10), (80, 20, 0.1, 0)]:
            time_array, temperature_array = simulate_temperature(
                initial, ambient, rate, horizon, 40
            )
            np.testing.assert_array_equal(temperature_array, np.full(41, initial))
            np.testing.assert_array_equal(
                exact_temperature(time_array, initial, ambient, rate), temperature_array
            )

    def test_match_independent_scalar_reference(self):
        result = exact_temperature([0, 1, 10], 80, 20, 0.1)
        expected = [20 + 60 * math.exp(-0.1 * time) for time in [0, 1, 10]]
        np.testing.assert_allclose(result, expected, rtol=1e-15, atol=0)

    def test_small_change_in_euler_branch(self):
        for initial, ambient in [(0.2, 20.0), (-0.2, -20.0), (1.0, 1e16),
                                 (1e16, 1.0), (1e-8, 20.0), (5.0, -10.0)]:
            for rate in [1e-18, 0.25, 1 / 3, 0.5, math.nextafter(0.5, 1.0), 0.75, 1.0]:
                with self.subTest(initial=initial, ambient=ambient, rate=rate):
                    _, temperature_array = simulate_temperature(initial, ambient, rate, 1, 1)
                    expected, _ = decimal_reference_pair(initial, ambient, rate, 1)
                    self.assertEqual(temperature_array[0], initial)
                    self.assert_within_rounding(
                        temperature_array[-1], expected, initial, ambient
                    )
                    self.assertGreaterEqual(temperature_array[-1], min(initial, ambient))
                    self.assertLessEqual(temperature_array[-1], max(initial, ambient))

    def test_analytic_small_change_in_each_branch(self):
        switch = math.log(2.0)
        # At log(1.5), the (5, -10) solution crosses zero.
        time_array = [0.0, 1e-18, 1e-10, 0.25, math.log(1.5), math.nextafter(switch, 0.0),
                 switch, math.nextafter(switch, math.inf), 1.0, 40.0]
        for initial, ambient in [(0.2, 20.0), (-0.2, -20.0), (1.0, 1e16),
                                 (1e16, 1.0), (1e-8, 20.0), (5.0, -10.0)]:
            result = exact_temperature(time_array, initial, ambient, 1.0)
            self.assertEqual(result[0], initial)
            for time, actual in zip(time_array, result):
                with self.subTest(initial=initial, ambient=ambient, time=time):
                    _, expected = decimal_reference_pair(initial, ambient, 1.0, time)
                    self.assert_within_rounding(actual, expected, initial, ambient)
                    self.assertGreaterEqual(actual, min(initial, ambient))
                    self.assertLessEqual(actual, max(initial, ambient))
            direction = 1 if ambient > initial else -1
            self.assertTrue(np.all(direction * np.diff(result) >= 0))

    def test_retain_small_decay_of_large_initial_value(self):
        _, expected = decimal_reference_pair(1e308, 20.0, 1.0, 40.0)
        self.assert_within_rounding(exact_temperature(40.0, 1e308, 20.0, 1.0),
                                    expected, 1e308, 20.0)
        # A rate-time product beyond the float range still tends to ambient.
        self.assertEqual(float(exact_temperature(1e308, 80.0, 20.0, 1e308)), 20.0)

    def test_preserve_scalar_array_and_empty_shape(self):
        for time_array in [np.array(1.0), np.array([[0.0, 1.0], [2.0, 3.0]]),
                      np.empty((0, 2))]:
            result = exact_temperature(time_array, 80.0, 20.0, 0.1)
            self.assertEqual(result.shape, time_array.shape)
            for index in np.ndindex(time_array.shape):
                _, expected = decimal_reference_pair(80.0, 20.0, 0.1, time_array[index])
                self.assert_within_rounding(result[index], expected, 80.0, 20.0)

    def test_accumulate_small_step_correctly(self):
        # 1024 steps make the step 2**-10, so rate*step is exact. Each step
        # rounds by about half a unit in the last place of the current
        # temperature plus a smaller part of its increment; the factor
        # 0 <= 1 - rate*step <= 1 never amplifies earlier errors.
        step_count = 1024
        for initial, ambient in [(0.2, 20.0), (-0.2, -20.0), (1e-8, 20.0)]:
            with self.subTest(initial=initial, ambient=ambient):
                _, temperature_array = simulate_temperature(
                    initial, ambient, 1e-13, 1.0, step_count
                )
                expected, largest = decimal_euler(
                    initial, ambient, 1e-13 / step_count, step_count
                )
                bound = (step_count + 1) * EPS * largest + 2 * EPS * abs(expected - initial)
                self.assertLessEqual(abs(temperature_array[-1] - expected), bound)

    def test_first_order_error_under_mesh_refinement(self):
        error_list = measure_convergence_error()
        # For k*t=1: error=60/e*(1/(2*n)+5/(24*n**2)+O(n**-3)).
        # The leading coefficient gives a much stronger check than agreement
        # with another implementation of the Euler recurrence.
        for step_count, error in error_list:
            leading = 30 / (math.e * step_count)
            self.assertLess(abs(error / leading - 1), 0.5 / step_count)
        for (_, coarse), (_, fine) in zip(error_list, error_list[1:]):
            self.assertGreater(coarse / fine, 2.0)
            self.assertLess(coarse / fine, 2.03)

    def test_invalid_parameter(self):
        for position in range(4):
            for invalid in [math.nan, math.inf, -math.inf]:
                argument_list = [80, 20, 0.1, 10, 40]
                argument_list[position] = invalid
                with self.subTest(position=position, invalid=invalid), self.assertRaises(ValueError):
                    simulate_temperature(*argument_list)
        for argument_list in [(80, 20, -0.1, 10, 40), (80, 20, 0.1, -10, 40),
                          (80, 20, 1, 2, 1), (80, 20, 0.1, 10, 0),
                          (80, 20, 0.1, 10, -1)]:
            with self.subTest(argument_list=argument_list), self.assertRaises(ValueError):
                simulate_temperature(*argument_list)
        for step_count in [True, 4.0, "4"]:
            with self.subTest(step_count=step_count), self.assertRaises(TypeError):
                simulate_temperature(80, 20, 0.1, 10, step_count)
        with self.assertRaises(TypeError):
            simulate_temperature(True, 20, 0.1, 10, 40)
        with self.assertRaises(ValueError):
            exact_temperature([-1], 80, 20, 0.1)


if __name__ == "__main__":
    unittest.main()
