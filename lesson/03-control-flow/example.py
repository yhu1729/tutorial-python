# Sample the dimensionless function y = x**2 on the interval [0, 1].
interval_count = 4
left_endpoint = 0.0
right_endpoint = 1.0
step = (right_endpoint - left_endpoint) / interval_count
weighted_sum = 0.0

print("x       y       position")
for index in range(interval_count + 1):
    x = left_endpoint + index * step
    y = x**2
    if index == 0:
        weight = 0.5
        position = "left endpoint"
    elif index == interval_count:
        weight = 0.5
        position = "right endpoint"
    else:
        weight = 1.0
        position = "interior"
    weighted_sum = weighted_sum + weight * y
    print(f"{x:.2f}    {y:.4f}  {position}")

integral_estimate = step * weighted_sum
exact_integral = 1.0 / 3.0
absolute_error = abs(integral_estimate - exact_integral)
print(f"Trapezoidal integral: {integral_estimate:.6f}")
print(f"Analytic integral: {exact_integral:.6f}")
print(f"Absolute error: {absolute_error:.6f}")
