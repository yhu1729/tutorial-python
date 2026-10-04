# Exercise 1: sum values, rather than their indices, and divide by the count.
measurement_list_m = [1.0, 1.5, 2.0, 2.5]
total_m = 0.0
for measurement_m in measurement_list_m:
    total_m = total_m + measurement_m
print(f"1. Mean length: {total_m / len(measurement_list_m):.2f} m")
print("1. Middle pair:", measurement_list_m[1:3])

# Exercise 2: tuple positions use integer indices; dictionary fields use keys.
position_m = (2.0, 3.0, 4.0)
record = {"name": "probe B", "temperature_c": 23.0, "unit": "deg C"}
record["temperature_c"] = 24.0
print("2. Vertical coordinate (m):", position_m[2])
print("2. Updated record:", record)

# Exercise 3: assignment creates an alias; copy() creates a separate flat list.
original = [10.0, 20.0, 30.0]
alias = original
independent = original.copy()
alias[1] = 99.0
independent.append(40.0)
print("3. Original:", original)
print("3. Alias:", alias)
print("3. Independent:", independent)
