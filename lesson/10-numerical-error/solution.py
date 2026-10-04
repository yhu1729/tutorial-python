"""Worked solutions; attempt exercise.md first."""

import math

from example import central_difference_sin


def main():
    # Exercise 1: abs_tol matters when the reference is zero.
    # If the values are temperatures in degrees Celsius, abs_tol is also in
    # degrees Celsius. rel_tol is dimensionless. Near zero it supplies no
    # useful absolute error allowance, hence the two comparisons differ.
    print("1. Near zero:", math.isclose(1e-12, 0.0, rel_tol=1e-9, abs_tol=2e-12))
    print("   Relative only:", math.isclose(1e-12, 0.0, rel_tol=1e-9))

    # Exercise 2: the truncated central-difference error is O(h**2).
    # All four observed orders approach two. The agreement across several
    # refinements supports the Taylor analysis; one ratio alone would not.
    print("2. Derivative of sin at x=0.5")
    previous_error = None
    for step in [0.2, 0.1, 0.05, 0.025, 0.0125]:
        error = abs(central_difference_sin(0.5, step) - math.cos(0.5))
        if previous_error is None:
            print(f"   h={step:.4f}, error={error:.6e}")
        else:
            order = math.log2(previous_error / error)
            print(f"   h={step:.4f}, error={error:.6e}, order={order:.4f}")
        previous_error = error

    # Exercise 3: identity avoids subtracting nearly equal square roots.
    # Multiply numerator and denominator by sqrt(1+x)+1:
    # (sqrt(1+x)-1)*(sqrt(1+x)+1)/(sqrt(1+x)+1) = x/(sqrt(1+x)+1).
    # The Taylor expansion sqrt(1+x)-1 = x/2 - x**2/8 + O(x**3)
    # explains why x/2 is close here, but it is not an exact reference.
    x = 1e-12
    direct = math.sqrt(1.0 + x) - 1.0
    stable = x / (math.sqrt(1.0 + x) + 1.0)
    print(f"3. Direct: {direct:.16e}; rationalized: {stable:.16e}")
    print("   Leading Taylor term:", x / 2)


if __name__ == "__main__":
    main()
