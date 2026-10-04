"""Roundoff and central differences, using an analytic derivative as truth."""

import math


def central_difference_sin(x, step):
    """Approximate d(sin(x))/dx with a finite positive step."""
    if not math.isfinite(x):
        raise ValueError("x must be finite")
    if not math.isfinite(step) or step <= 0:
        raise ValueError("step must be finite and positive")
    if not math.isfinite(x + step) or not math.isfinite(x - step):
        raise ValueError("sample points must be finite")
    if x + step == x or x - step == x:
        raise ValueError("step is too small to change x in floating-point arithmetic")
    denominator = 2 * step
    if not math.isfinite(denominator):
        raise ValueError("twice the step must be representable")
    return (math.sin(x + step) - math.sin(x - step)) / denominator


def main():
    print(f"0.1 + 0.2 == 0.3: {0.1 + 0.2 == 0.3}")
    print(f"isclose: {math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-15)}")
    value_list = [1e16, 1.0, -1e16]
    total = 0.0
    for value in value_list:
        total += value
    print(f"Loop sum: {total:.1f}; fsum: {math.fsum(value_list):.1f}")
    x = 1.0
    exact = math.cos(x)
    previous_error = None
    print("step       absolute error   previous/current")
    for step in [0.2, 0.1, 0.05, 0.025, 0.0125]:
        error = abs(central_difference_sin(x, step) - exact)
        ratio = "-" if previous_error is None else f"{previous_error / error:.3f}"
        print(f"{step:7.4f}    {error:.6e}     {ratio}")
        previous_error = error
    print("Tiny steps: truncation decreases, then roundoff can dominate")
    for step in [1e-4, 1e-6, 1e-8, 1e-10, 1e-12]:
        error = abs(central_difference_sin(x, step) - exact)
        print(f"{step:.0e}    {error:.6e}")


if __name__ == "__main__":
    main()
