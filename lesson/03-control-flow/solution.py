# Exercise 1: boundaries belong to the middle branch.
temperature_c = 20.0
if temperature_c < 0.0:
    category = "below range"
elif temperature_c <= 100.0:
    category = "within range"
else:
    category = "above range"
print("1. Category:", category)

# Exercise 2: range stops before its endpoint, hence 11 includes the value 10.
# / always returns a float, so the formula prints 55.0; 55 == 55.0 is True.
total = 0
for value in range(1, 11):
    total = total + value
print("2. Sum:", total)
print("2. Formula 10 * 11 / 2:", 10 * 11 / 2)

# Exercise 3: the trapezoidal rule integrates a straight line exactly in real
# arithmetic. Both endpoints count half; all interior points count once.
interval_count = 4
step = 1.0 / interval_count
weighted_sum = 0.0
for index in range(interval_count + 1):
    x = index * step
    y = x
    if index == 0 or index == interval_count:
        weight = 0.5
    else:
        weight = 1.0
    weighted_sum = weighted_sum + weight * y
integral_estimate = step * weighted_sum
print(f"3. Integral of x on [0, 1]: {integral_estimate:.6f}")
print(f"3. Absolute error: {abs(integral_estimate - 0.5):.6f}")
