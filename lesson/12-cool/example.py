"""Newton cooling: explicit Euler, analytic verification, CSV and a saved plot."""

import csv
import math
from numbers import Real
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def finite_scalar(value, name):
    """Accept finite real scalar inputs, excluding Boolean values."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def simulate_temperature(initial, ambient, rate, horizon, step_count):
    """Return times and Euler temperatures with monotone relaxation enforced.

    Temperatures are in degrees Celsius, time in minutes and rate in min^-1.
    The educational integrator requires rate * dt <= 1, a stricter restriction
    than absolute stability, to prevent overshooting the ambient temperature.
    """
    initial = finite_scalar(initial, "initial")
    ambient = finite_scalar(ambient, "ambient")
    rate = finite_scalar(rate, "rate")
    horizon = finite_scalar(horizon, "horizon")
    if rate < 0 or horizon < 0:
        raise ValueError("rate and horizon must be nonnegative")
    if isinstance(step_count, bool) or not isinstance(step_count, int):
        raise TypeError("step_count must be a Python int")
    if step_count <= 0:
        raise ValueError("step_count must be positive")
    if not math.isfinite(initial - ambient):
        raise ValueError("initial minus ambient must be representable")
    step = horizon / step_count
    if horizon > 0 and step == 0:
        raise ValueError("time step underflows to zero")
    rate_step = rate * step
    if rate_step > 1:
        raise ValueError("rate * time step must be <= 1 for monotone relaxation")
    time_array = np.linspace(0.0, horizon, step_count + 1)
    temperature_array = np.empty(step_count + 1, dtype=float)
    temperature_array[0] = initial
    if rate_step == 0 or initial == ambient:
        temperature_array.fill(initial)
        return time_array, temperature_array
    for index in range(step_count):
        current = temperature_array[index]
        # Evaluate from the closer endpoint to preserve small changes.
        if rate_step <= 0.5:
            temperature_array[index + 1] = current + rate_step * (ambient - current)
        else:
            temperature_array[index + 1] = ambient + (1.0 - rate_step) * (current - ambient)
    return time_array, temperature_array


def exact_temperature(time_array, initial, ambient, rate):
    """Evaluate the analytic solution on finite nonnegative times."""
    initial = finite_scalar(initial, "initial")
    ambient = finite_scalar(ambient, "ambient")
    rate = finite_scalar(rate, "rate")
    time_array = np.asarray(time_array, dtype=float)
    if rate < 0 or not np.all(np.isfinite(time_array)) or np.any(time_array < 0):
        raise ValueError("rate and times must be finite and nonnegative")
    if not math.isfinite(initial - ambient):
        raise ValueError("initial minus ambient must be representable")
    result = np.empty_like(time_array)
    if rate == 0 or initial == ambient:
        result.fill(initial)
        return result
    half_decay_exponent = math.log(2.0)
    for index in np.ndindex(time_array.shape):
        time = float(time_array[index])
        if time == 0:
            result[index] = initial
            continue
        # A Python scalar product can tend to infinity without a NumPy warning.
        scaled_time = rate * time
        if scaled_time <= half_decay_exponent:
            # expm1 retains the change even when exp(-scaled_time) rounds to 1.
            result[index] = initial + (ambient - initial) * (-math.expm1(-scaled_time))
        else:
            # Retain the decay directly: 1 - exp(-scaled_time) can round to 1.
            result[index] = ambient + (initial - ambient) * math.exp(-scaled_time)
    return result


def measure_convergence_error():
    """Measure terminal error on five independently refined time grids."""
    error_list = []
    for step_count in [20, 40, 80, 160, 320]:
        time_array, temperature_array = simulate_temperature(80.0, 20.0, 0.1, 10.0, step_count)
        exact = exact_temperature(time_array[-1], 80.0, 20.0, 0.1)
        error_list.append((step_count, abs(float(temperature_array[-1] - exact))))
    return error_list


def main():
    output = Path(__file__).resolve().parents[2] / "output" / "12-cool"
    output.mkdir(parents=True, exist_ok=True)
    time_array, temperature_array = simulate_temperature(80.0, 20.0, 0.1, 10.0, 40)
    exact = exact_temperature(time_array, 80.0, 20.0, 0.1)
    with (output / "temperature.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["time_min", "euler_C", "analytic_C", "absolute_error_C"])
        for time, numerical, reference in zip(time_array, temperature_array, exact):
            writer.writerow([time, numerical, reference, abs(numerical - reference)])
    figure, ax = plt.subplots()
    ax.plot(time_array, exact, label="Analytic solution")
    ax.plot(time_array, temperature_array, "o--", markersize=3, label="Euler, dt=0.25 min")
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    figure.tight_layout()
    figure.savefig(output / "temperature.png", dpi=150)
    plt.close(figure)
    print(f"Final Euler temperature: {temperature_array[-1]:.6f} °C")
    print(f"Final analytic temperature: {exact[-1]:.6f} °C")
    print("steps   terminal error (°C)   previous/current   observed order")
    previous_error = None
    for step_count, error in measure_convergence_error():
        if previous_error is None:
            print(f"{step_count:5d}   {error:.6e}          -                  -")
        else:
            ratio = previous_error / error
            print(f"{step_count:5d}   {error:.6e}          {ratio:.4f}"
                  f"             {math.log2(ratio):.4f}")
        previous_error = error
    print("Saved output/12-cool/temperature.csv and output/12-cool/temperature.png")


if __name__ == "__main__":
    main()
